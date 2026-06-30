# 영화 게시판 백엔드 핸즈온 (Django REST API)

> "백엔드 기초 & API 설계" 세션의 후속 실습. 회원가입부터 **영화 글(사진 포함)·댓글**까지 REST API 한 바퀴.

## 📑 목차

**🟢 1층 — 핵심 실습 (Minimal Path)**
- [0. 실행](#0-실행) · [1. User API](#1-user-api--회원가입로그인) · [2. Movie API](#2-movie-api--영화-글포스터) · [3. Comment API](#3-comment-api--댓글) · [4. 테스트](#4-테스트-swagger--curl)

**🟡 2층 — 이해 & 확장**
- [왜 Serializer를 3개로 나눔](#왜-serializer를-3개로-나눔) · [왜 ImageField는 파일로 저장](#왜-imagefield는-파일로-저장하나) · [FK vs IntegerField](#작성자-fk-vs-integerfield) · [settings 분리 이유](#settings-분리-basedevprod-이유) · [WSGI vs ASGI](#wsgi-vs-asgi) · [REST URI·APPEND_SLASH](#rest-uri--append_slash) · [왜 APIView](#왜-apiview) · [확장](#확장-실무로-가면)

**부록** — [치트시트](#부록-a-명령어-치트시트) · [자주 나는 에러](#부록-b-자주-나는-에러)

## 📂 파일 구조 — "어느 파일에 쓰나요?"

```
django-board-handson/
├── manage.py                 # 장고 명령 입구
├── requirements.txt          # 패키지 목록
├── docker-compose.yml        # MySQL (도커)
├── config/                   # 프로젝트 설정·진입점
│   ├── settings/             #   base.py · dev.py · prod.py
│   └── urls.py               #   최상위 URL → 각 앱 연결
├── users/                    # 회원 앱  (models · views · urls)
└── movies/                   # 영화 게시판 앱
    ├── models.py             #   Movie · Comment (테이블)
    ├── serializers.py        #   목록/상세/생성 변환·검증
    ├── views.py              #   요청 처리 (제일 많이 만짐)
    └── urls.py               #   /api/v1/movies …
```

## 데이터 구조 (ERD)

```
User                Movie(제목 + 포스터이미지 + 리뷰글) 1 ──< N Comment
```
영화 한 편(Movie)에 댓글(Comment) 여러 개. `movies` 앱 하나에 `movies`·`comments` 두 테이블.

---

# 🟢 1층 — 핵심 실습 (Minimal Path)

> 여기만 순서대로 따라 하면 API가 돌아갑니다. 코드 위주, **"왜?"는 [🟡 2층](#-2층--이해--확장-읽으면-좋은)** 에서.

## 0. 실행

```bash
# 1) 가상환경 + 패키지
python -m venv venv
source venv/bin/activate            # 윈도우: venv\Scripts\activate
pip install -r requirements.txt

# 2) MySQL (도커)
docker compose up -d                # 포트 3306

# 3) 테이블 생성 + 서버
python manage.py migrate
python manage.py runserver          # http://127.0.0.1:8000/swagger
```
> ⚠️ **초보 주의**: `makemigrations`(모델 바꿨을 때) → `migrate`(DB 반영) **둘 다** 해야 테이블이 생겨요.
> ⚠️ `Access denied` → 로컬 MySQL이 3306 점유 중. 맥 `brew services stop mysql` / 윈도우 `net stop MySQL80`.

## 1. User API — 회원가입/로그인

**`users/models.py`**
```python
class User(models.Model):
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)          # 학습용 평문
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "users"
```

**`users/views.py`** — 클래스형(APIView), 응답은 `Response(dict)` → JSON 자동 변환
```python
class SignupView(APIView):
    def post(self, request):
        email = request.data.get("email"); password = request.data.get("password")
        if not email or not password:
            return Response({"message": "이메일/비번을 입력하세요."}, status=400)
        if User.objects.filter(email=email).exists():        # 중복 확인 (ORM)
            return Response({"message": "이미 가입된 이메일."}, status=400)
        user = User.objects.create(email=email, password=password)
        return Response({"message": "회원가입 성공", "user_id": user.id}, status=201)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email"); password = request.data.get("password")
        try:
            user = User.objects.filter(email=email, password=password).get()
        except User.DoesNotExist:
            return Response({"message": "이메일/비번 불일치"}, status=401)
        return Response({"message": "로그인 성공", "user_id": user.id}, status=200)
```

**`users/urls.py`**
```python
urlpatterns = [
    path("users/signup", SignupView.as_view()),
    path("users/login", LoginView.as_view()),
]
```
> signup/login은 둘 다 POST라 URL로 구분이 안 돼서 예외적으로 동사를 씀 → [REST URI 설명](#rest-uri--append_slash)

**`config/urls.py`** (진입점에서 앱 연결)
```python
urlpatterns = [
    path("api/v1/", include("users.urls")),
    path("api/v1/", include("movies.urls")),
    path("swagger", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
]
```

## 2. Movie API — 영화 글(+포스터)

**`movies/models.py`**
```python
class Movie(models.Model):                       # 게시판 한 건 = 영화 한 편
    user_id = models.IntegerField()              # 작성자 (간단히 정수 → 2층 설명)
    title = models.CharField(max_length=200)     # 영화 제목
    content = models.TextField()                 # 리뷰 내용
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)  # 이미지
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "movies"; ordering = ["-created_at"]

class Comment(models.Model):
    user_id = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")  # 1:N
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "comments"; ordering = ["created_at"]
```

**이미지 업로드 세팅 (3곳)**
```python
# requirements.txt → Pillow 포함 (이미 들어있음)

# config/settings/base.py
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# config/urls.py (개발 중 사진 서빙)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
> 사진은 JSON이 아니라 **multipart/form-data** 로 보냄 → [왜 파일로 저장하나](#왜-imagefield는-파일로-저장하나)

**`movies/serializers.py`** — 화면에 맞춰 목록/상세/생성 분리 ([왜?](#왜-serializer를-3개로-나눔))
```python
class MovieListSerializer(serializers.ModelSerializer):      # 목록 = 이미지+제목만
    class Meta: model = Movie; fields = ["id", "title", "poster"]

class MovieSerializer(serializers.ModelSerializer):          # 생성 입력용
    class Meta:
        model = Movie
        fields = ["id", "user_id", "title", "content", "poster", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user_id", "movie", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "movie", "created_at", "updated_at"]

class MovieDetailSerializer(serializers.ModelSerializer):    # 상세 = 전부 + 댓글
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ["id", "user_id", "title", "content", "poster", "comments", "created_at", "updated_at"]
```

**`movies/views.py`**
```python
class MovieView(APIView):
    parser_classes = [MultiPartParser]           # multipart 전용 → Swagger에 파일선택 칸
    def get(self, request):                       # 목록
        movies = Movie.objects.all()
        return Response(MovieListSerializer(movies, many=True, context={"request": request}).data)
    def post(self, request):                      # 생성 (+포스터)
        s = MovieSerializer(data=request.data, context={"request": request})
        s.is_valid(raise_exception=True); s.save()
        return Response(s.data, status=201)

class MovieDetailView(APIView):
    def get(self, request, movie_id):             # 상세 (제목·사진·글·댓글)
        movie = get_object_or_404(Movie, id=movie_id)
        return Response(MovieDetailSerializer(movie, context={"request": request}).data)
```
> 왜 가장 단순한 `APIView`? → [여기](#왜-apiview)

**`movies/urls.py`**
```python
urlpatterns = [
    path("movies", MovieView.as_view()),                                 # GET 목록 · POST 생성
    path("movies/<int:movie_id>", MovieDetailView.as_view()),            # GET 상세
    path("movies/<int:movie_id>/comments", CommentCreateView.as_view()), # POST 댓글
]
```

## 3. Comment API — 댓글

**`movies/views.py`** (이어서)
```python
class CommentCreateView(APIView):
    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        s = CommentSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        s.save(movie=movie)                       # URL의 영화에 댓글 연결
        return Response(s.data, status=201)
```
댓글은 상세 조회 시 `comments` 로 함께 내려와요(nested).

## 4. 테스트 (Swagger / curl)

**Swagger** — http://127.0.0.1:8000/swagger → API 클릭 → **Try it out** → 값 입력 → **Execute**
(영화 등록은 `poster`가 **파일 선택** 칸. 안 보이면 브라우저 하드 새로고침 `Cmd/Ctrl+Shift+R`)

**curl**
```bash
B=http://127.0.0.1:8000/api/v1
curl -X POST $B/users/signup -H "Content-Type: application/json" -d '{"email":"a@b.com","password":"1"}'
curl -X POST $B/movies -F "user_id=1" -F "title=인터스텔라" -F "content=인생영화" -F "poster=@poster.jpg"
curl $B/movies            # 목록(이미지+제목)
curl $B/movies/1          # 상세(글·댓글 포함)
curl -X POST $B/movies/1/comments -H "Content-Type: application/json" -d '{"user_id":1,"content":"동의"}'
```

**데이터 확인** — 가장 쉬운 건 위 `GET`. DB로 직접 보려면:
```bash
docker exec -it mysqldb mysql --default-character-set=utf8mb4 -uroot -p1234 mydatabase
#  SELECT id,title FROM movies;
```
(또는 `python manage.py createsuperuser` 후 `/admin`)

---

# 🟡 2층 — 이해 & 확장 (읽으면 좋은)

> 1층으로 API는 이미 돌아요. 여기는 "왜 이렇게 짰나"를 이해하는 영역.

## 왜 Serializer를 3개로 나눔

같은 영화라도 화면마다 필요한 게 달라요.

| 상황 | 시리얼라이저 | fields | 이유 |
|---|---|---|---|
| 목록 | `MovieListSerializer` | id·title·poster | 카드엔 이미지+제목만. content·댓글까지 보내면 **payload↑·쿼리↑·렌더링 느림** |
| 생성 | `MovieSerializer` | 입력 필드 | **검증이 핵심**(required·길이·이미지 형식) = write용 |
| 상세 | `MovieDetailSerializer` | 전부 + comments | 정보가 많이 필요 = 가장 무거움 |

- **꼭 3개?** 작으면 하나로도 OK. 하지만 댓글 500개 글 20개 목록 조회 시 `20×500` nested 직렬화로 **API가 터져요.** 그래서 분리.
- **직렬화** = 객체→JSON / **역직렬화** = JSON→객체. Serializer는 단순 변환기가 아니라 **검증(validation) 레이어**예요.

## 왜 ImageField는 파일로 저장하나

```
업로드한 poster.png
 ├─ 실제 파일  → media/posters/poster.png     (디스크에 저장)
 └─ DB movies.poster → "posters/poster.png"   (경로 문자열만!)
```
- 사진 자체를 DB에 넣으면 무거워지고 느려져요. **파일은 파일시스템(또는 S3), DB는 경로만.**
- `ImageField` = `FileField` + "진짜 이미지인지 검증"(Pillow가 함) → 그래서 Pillow 필요.
- 응답의 `poster`는 뷰에서 `context={"request": request}` 를 줘서 **전체 URL**(`http://.../media/...`)로 나가요. (프론트가 다른 포트에서 바로 `<img>`에 꽂게)
- **왜 multipart/form-data?** JSON은 글자용, 이미지는 바이너리라 안 맞음. 그래서 `MovieView`에 `parser_classes=[MultiPartParser]`.
- 운영(prod)에선 Django가 아니라 nginx/S3가 이미지를 서빙해요(그래서 `static(...)`이 `if DEBUG` 안에).

## 작성자: FK vs IntegerField

지금 `Movie.user_id = IntegerField()` 는 **학습 단순화용**이에요.

> ⚠️ **실무에서는 거의 안 씁니다.** 보통 `ForeignKey(User)` 를 써요.

| | ① ForeignKey (실무 정석) | ② IntegerField (지금) |
|---|---|---|
| 코드 | `user = models.ForeignKey('users.User', on_delete=CASCADE)` | `user_id = models.IntegerField()` |
| `movie.user.email` | **객체로 바로 접근** (ORM) | 불가 (그냥 숫자) |
| 무결성 | 존재하는 유저만 | 없는 id도 그냥 저장됨 |

- 처음엔 FK를 걸면 글 만들 때 그 유저가 꼭 있어야 해서 테스트가 번거로워 정수로 단순화.
- 인증을 붙이면 보통 `user_id`를 클라가 안 보내고 뷰에서 `serializer.save(user=request.user)`, `read_only_fields=["user_id"]`.

## settings 분리 (base/dev/prod) 이유

`settings.py` 한 파일을 셋으로 쪼갬 — 개발과 배포는 값이 다르니까.

| 항목 | dev | prod |
|---|---|---|
| `DEBUG` | True | False (보안) |
| DB `HOST` | `127.0.0.1` | `mysqldb`(컨테이너 이름) |
| 비밀값 | 코드에 둬도 OK | `.env`로 숨김(깃 제외) |

- `dev`/`prod` 는 `from .base import *` 로 공통을 가져오고 다른 값만 덮어씀.
- **HOST 갈리는 지점**: 백엔드를 로컬 실행하면 도커 MySQL에 `127.0.0.1`로, 백엔드도 도커면 컨테이너 이름 `mysqldb`로 접속.
- `manage.py`→기본 dev, `wsgi/asgi`→기본 prod.

## WSGI vs ASGI

- **WSGI(동기)** = 요청 하나 끝날 때까지 일꾼이 묶임. 일반 CRUD엔 충분(지금 우리).
- **ASGI(비동기)** = 기다리는 동안 다른 요청도 처리, **웹소켓 등 실시간** 가능.
- FastAPI는 ASGI 전용, Django는 원래 WSGI지만 ASGI도 지원(그래서 `wsgi.py`/`asgi.py` 둘 다 있음).

## REST URI · APPEND_SLASH

- **URI는 동사 말고 명사·복수형**: ✅ `/movies`, `/movies/1` · ❌ `/createMovie`, `/movies/1/delete`. 행동은 HTTP 메서드(POST/GET/DELETE)가 표현.
- 그래서 `POST /movies` = 메서드 POST(행동) + 명사 movies(자원). (signup/login은 둘 다 POST라 예외적으로 동사)
- `APPEND_SLASH = False`: 장고 기본(True)은 URL 끝에 `/`를 붙임. 끝 슬래시 없이 설계하려고 끔 → `/movies/1`✅ `/movies/1/`❌

## 왜 APIView

DRF엔 `APIView` / `GenericAPIView` / `ViewSet` 이 있어요. 지금은 GET/POST 흐름을 **직접 눈으로 보려고 가장 단순한 `APIView`**. 실무 반복 CRUD엔 `ViewSet`을 많이 써요.
(회원가입에 장고 기본 `auth`를 안 쓴 것도 같은 맥락 — 처음엔 단순하게.)

## 확장 (실무로 가면)

| 확장 | 무엇을 |
|---|---|
| 별점 | `rating`(1~5) 필드 + 평균 |
| 작성자 FK | `user_id` 정수 → `ForeignKey(User)` |
| 인증 | 간단 로그인 → **JWT 토큰** |
| 조회 편의 | 페이지네이션·검색(`?keyword=`)·정렬 |
| 프론트 | React(Vite)+axios, 사진은 `FormData`, CORS 풀기 |

> 💡 React 프론트 연동까지 동작하는 참고 구현: `~/Downloads/movie-review-handson/`

---

# 부록 A. 명령어 치트시트

```bash
source venv/bin/activate             # 가상환경 (윈도우: venv\Scripts\activate)
pip install -r requirements.txt      # 패키지 (Pillow·mysqlclient 포함)
docker compose up -d                 # MySQL (내리기: down)
python manage.py makemigrations      # 모델 변경 기록
python manage.py migrate             # DB 반영
python manage.py runserver           # 서버 (포트: runserver 8080)
python manage.py createsuperuser     # 관리자 → /admin
```

# 부록 B. 자주 나는 에러

| 증상 | 해결 |
|---|---|
| `ModuleNotFoundError: django` | 가상환경 안 켬 → `source venv/bin/activate` (윈도우 `venv\Scripts\activate`) |
| `Error loading MySQLdb module` | `pip install -r requirements.txt`. 맥 빌드 실패 시 `brew install mysql-client pkg-config` · 윈도우는 보통 바로 설치 |
| MySQL `Access denied for user 'root'` | 로컬 MySQL이 3306 점유 → 맥 `brew services stop mysql` · 윈도우 `net stop MySQL80` |
| `Can't connect to MySQL (2003)` | 도커 안 뜸 → `docker compose up -d` |
| 모델 바꿨는데 반영 안 됨 | `makemigrations` → `migrate` 다시 |
| 맞는 주소인데 404 | URL 끝 슬래시 (`/movies/1/`❌ → `/movies/1`✅) |
| Swagger 입력칸/파일선택 안 뜸 | 브라우저 하드 새로고침 `Cmd/Ctrl+Shift+R` |
| 사진이 안 보임 | 응답 `poster`가 전체 URL인지, `DEBUG=True`에서 media 서빙 중인지 |
