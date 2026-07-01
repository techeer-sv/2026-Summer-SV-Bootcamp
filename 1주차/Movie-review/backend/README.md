# 영화 게시판 백엔드 핸즈온 (Django REST API)

> 회원가입부터 **영화 글(사진 포함)·댓글**까지 REST API를 손으로 만들어보는 실습.
> **이 문서는 "따라하기"** — 위에서 아래로 그대로 따라 치면 API가 돕니다.
> "왜 이렇게 짰나"가 궁금하면 곳곳의 **`→ 자세히`** 링크(→ [CONCEPTS.md](CONCEPTS.md))를 보세요.

## 만들 결과물

| 화면 | 보여주는 것 | 쓰는 시리얼라이저 |
|---|---|---|
| **게시판 목록** | 영화 **이미지 + 제목** | `MovieListSerializer` (가벼움) |
| **상세(클릭)** | 제목 + 사진 + 리뷰 글 + **댓글** | `MovieDetailSerializer` (전부) |

## 📑 목차

[0. 환경 세팅](#0-환경-세팅) · [1. User API](#1-user-api--회원가입로그인) · [2. 실행 & 테스트](#2-실행--테스트) · [3. 영화·댓글 API](#3-영화-게시판--movie--comment) · [4. 확장](#4-확장하기) · [부록](#부록-a-명령어-치트시트)
→ 개념·"왜" 모음: **[CONCEPTS.md](CONCEPTS.md)**

## 📂 파일 구조

이 저장소는 **backend(Django) + frontend(React)** 가 함께 있는 모노레포예요.
아래는 **backend/** 안쪽 구조입니다. (프론트는 → [../frontend](../frontend))

```
django-board-handson/
├── backend/                  # ← 지금 이 문서(Django REST API)
│   ├── manage.py
│   ├── requirements.txt      #   Django · DRF · Pillow · django-cors-headers
│   ├── db.sqlite3            #   개발용 DB (migrate 시 생성)
│   ├── config/               #   프로젝트 설정·진입점
│   │   ├── settings/         #     base.py · dev.py · prod.py  (CORS는 base)
│   │   └── urls.py
│   ├── users/                #   회원 앱 (models · views · urls)
│   └── movies/               #   영화 게시판 앱
│       ├── models.py         #     Movie · Comment
│       ├── serializers.py    #     목록/상세/생성
│       ├── views.py
│       └── urls.py
└── frontend/                 # React + Vite + axios (게시판·상세·작성 화면)
```
> 단계 제목 옆 `(파일명)` = 그 단계에서 만지는 파일. 경로는 `backend/` 기준.

## 데이터 구조 (ERD)

```
User                Movie(제목 + 포스터이미지 + 리뷰글) 1 ──< N Comment
```
영화 한 편(Movie)에 댓글(Comment) 여러 개. `movies` 앱에 `movies`·`comments` 두 테이블.

---

# 0. 환경 세팅

## 0-1. 가상환경 + 장고 설치

```bash
mkdir django-board-handson && cd django-board-handson
python -m venv venv
source venv/bin/activate            # 윈도우: venv\Scripts\activate
pip install django
```

## 0-2. 프로젝트 생성

```bash
django-admin startproject config .  # 끝의 점(.) = 바로 여기에
```
이러면 `manage.py` + `config/`(설정·urls·wsgi·asgi)가 생겨요. 그다음 앱을 만들어 붙여요:
```bash
python manage.py startapp users
python manage.py startapp movies
```

## 0-3. settings 분리 (base / dev / prod)

`settings.py` 한 파일을 셋으로 쪼개요. 개발/배포는 값(DEBUG, DB 등)이 다르니까.
```
config/settings/
├── base.py   # 공통 (앱·미들웨어·언어 …)
├── dev.py    # 개발 = SQLite
└── prod.py   # 배포 = 실제 DB(.env)
```
> → 왜·어떻게 다른지 자세히: [CONCEPTS.md # settings 분리](CONCEPTS.md#settings-분리)

## 0-4. `APPEND_SLASH = False`

URL 끝 슬래시를 안 붙이려고 끔 → `/movies/1`✅ `/movies/1/`❌
> → REST URI 원칙(동사 말고 명사): [CONCEPTS.md # REST URI](CONCEPTS.md#rest-uri)

## 0-5. 앱을 도메인별로 나눠요

`users`/`movies`는 우리가 만든 앱이고 이름도 자유. 기준은 **비즈니스 도메인**.
> → 왜 나누나: [CONCEPTS.md # 앱 분리](CONCEPTS.md#앱-분리)

## 0-6. Swagger (API 자동 문서)

`drf-spectacular` 로 자동 생성. `config/urls.py` 에 `/swagger`(화면)·`/api/schema`(원본) 연결돼 있어요.

## 0-7. CORS (프론트 연동 준비) 🌐

프론트(React/Vite, 5173)와 백엔드(Django, 8000)는 **포트가 달라요.** 브라우저는 보안상
"다른 출처(origin)"로 가는 요청을 기본적으로 막습니다(**동일 출처 정책, SOP**). 그래서
서버가 "이 출처는 허용한다"는 응답 헤더를 붙여줘야 하는데, 그게 **CORS** 예요.

```bash
pip install django-cors-headers      # requirements.txt 에 포함됨
```
```python
# config/settings/base.py
INSTALLED_APPS = [ ..., "corsheaders" ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",   # ★ CommonMiddleware '위'에!
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...
]

CORS_ALLOWED_ORIGINS = [                 # 허용할 프론트 주소
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
CORS_ALLOW_CREDENTIALS = True            # 쿠키/인증정보 포함 요청 허용 (axios withCredentials와 짝)
```
> ⚠️ `CorsMiddleware` 는 **`CommonMiddleware` 보다 위**에 둬야 헤더가 제대로 붙어요.
> → 왜 필요한지·프론트와 어떻게 짝이 맞는지: [CONCEPTS.md # CORS](CONCEPTS.md#cors)

---

# 1. User API — 회원가입/로그인

가장 먼저 **회원(User)** 부터 만들어요. 서비스를 만들면 회원가입/로그인을 제일 먼저 짜게 되거든요.
그리고 **모델(DB 설계)부터** 짜고 시작해요 — 데이터 구조가 모든 것의 토대라, 뷰(로직)는 그 위에 얹는 거예요.

> 장고엔 기본 회원 기능(`auth`)이 있지만 **일부러 안 써요.** 처음부터 로그인을 빡빡하게 만들면
> 뒤 기능 테스트가 힘들어져서, 여기선 이메일/비번만 받는 **아주 단순한** User를 직접 만듭니다.

## 1-1. 모델 (`users/models.py`)

DB에 들어갈 "표(테이블)"를 설계하는 곳. **필드 하나 = 컬럼 하나** 예요.
```python
class User(models.Model):
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)          # 학습용 평문 (실무는 해시)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시각 자동
    updated_at = models.DateTimeField(auto_now=True)      # 수정 시각 자동
    class Meta:
        db_table = "users"                                # 테이블 이름 (복수형)
```
- `auto_now_add` / `auto_now` → 내가 값을 안 넣어도 시각이 **자동으로** 채워져요.
- `class Meta` 는 그 테이블에 대한 설정(이름 등). 모델을 만들었으면 나중에 `migrate` 로 DB에 반영해요(→ 2번).

## 1-2. 뷰 (`users/views.py`) — 로직을 여기서 처리

뷰는 "요청을 받아서 처리하는" 곳이에요. 장고는 함수형·클래스형 둘 다 되는데, 여기선 **클래스형(APIView)** 을
써요(가독성이 좋아요). **메서드 이름이 곧 HTTP 메서드** — 회원가입은 `POST` 라 `def post` 안에 로직을 넣어요.
```python
class SignupView(APIView):
    def post(self, request):
        email = request.data.get("email"); password = request.data.get("password")   # ① 값 꺼내기
        if not email or not password:                                                  # ② 빈값 막기
            return Response({"message": "이메일/비번을 입력하세요."}, status=400)
        if User.objects.filter(email=email).exists():                                  # ③ 중복 확인 (ORM)
            return Response({"message": "이미 가입된 이메일."}, status=400)
        user = User.objects.create(email=email, password=password)                     # ④ 생성
        return Response({"message": "회원가입 성공", "user_id": user.id}, status=201)
```
- **①** `request.data` = 요청 body로 들어온 값. `.get()` 으로 email/password를 꺼내요.
- **②** 사용자가 안 넣을 수도 있으니 기초 예외처리 → **400(잘못된 요청)**.
- **③** `User.objects.filter(...)` 는 **ORM** — SQL을 직접 안 짜도 장고가 DB 조회를 대신 해줘요. (장고 내장)
- **④** `User.objects.create(...)` 로 한 줄에 저장. 응답은 `Response(dict)` → DRF가 알아서 **JSON**으로 내려줘요.

```python
class LoginView(APIView):
    def post(self, request):                                                           # 로그인도 POST!
        email = request.data.get("email"); password = request.data.get("password")
        try:
            user = User.objects.filter(email=email, password=password).get()           # 맞으면 그 유저 반환
        except User.DoesNotExist:
            return Response({"message": "이메일/비번 불일치"}, status=401)             # 사용자 잘못 = 401
        return Response({"message": "로그인 성공", "user_id": user.id}, status=200)
```
- **로그인도 POST 예요.** 조회 같지만, 이메일/비번을 URL에 실으면 노출되니까 body(POST)로 보내요.
- 없는 계정이면 `DoesNotExist` 예외 → 서버 잘못이 아니라 **사용자 입력 잘못이라 401**.

## 1-3. URL (`users/urls.py`) — 뷰를 주소에 연결

```python
urlpatterns = [
    path("users/signup", SignupView.as_view()),
    path("users/login", LoginView.as_view()),
]
```
> REST 원칙은 '동사 말고 명사'지만, signup/login은 **둘 다 POST라 주소로 구분이 안 돼서** 예외로 동사를 써요. → [CONCEPTS.md # REST URI](CONCEPTS.md#rest-uri)

## 1-4. 진입점 연결 (`config/urls.py`)

요청은 `config/urls.py`(맨 앞 진입점)로 먼저 들어와서, 각 앱의 urls로 넘어가요.
```python
urlpatterns = [
    path("api/v1/", include("users.urls")),    # /api/v1/users/... → users 앱이 처리
    path("api/v1/", include("movies.urls")),
    path("swagger", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
]
```

> ✅ **여기까지** — 회원(User) API 완성. 다음 2번에서 서버 띄우고 회원가입을 눌러보세요.

---

# 2. 실행 & 테스트

## 2-1. DB 준비 (SQLite — 설치·도커 불필요)
따로 할 게 없어요. 아래 `migrate` 만 하면 `db.sqlite3` 파일이 자동 생성됩니다.

## 2-2. 마이그레이션 → 서버 실행
```bash
python manage.py makemigrations   # 모델 변경 → 설계도 파일
python manage.py migrate          # 설계도 → 실제 DB 테이블
python manage.py runserver        # http://127.0.0.1:8000/swagger
```
> ⚠️ **초보 주의**: `makemigrations`(설계도) → `migrate`(DB 반영) **둘 다** 해야 테이블이 생겨요.
> → 이 두 명령이 실제로 뭘 하는지: [CONCEPTS.md # 마이그레이션](CONCEPTS.md#마이그레이션)

## 2-3. Swagger 보는 법
브라우저: **http://127.0.0.1:8000/swagger** → API 클릭 → **Try it out** → 값 입력 → **Execute**

## 2-4. curl
```bash
curl -X POST http://127.0.0.1:8000/api/v1/users/signup \
  -H "Content-Type: application/json" -d '{"email":"a@b.com","password":"1"}'
```

## 2-5. DB에 들어갔는지 확인
- **가장 쉬움** — `GET /api/v1/movies` (Swagger/curl). 등록한 게 보이면 OK.
- **파일로** — `db.sqlite3` 를 DB 뷰어(VS Code SQLite 확장, DB Browser for SQLite)로 열기.
- **관리자** — `python manage.py createsuperuser` 후 `/admin`.

---

# 3. 영화 게시판 — Movie / Comment

## 3-1. 모델부터 짜요
ERD를 먼저 그리고 거기에 맞게 클래스를 짜요. (로직 짜다 즉흥적으로 컬럼 추가하면 설계가 엉켜요)

## 3-2. Movie 모델 (`movies/models.py`)
```python
class Movie(models.Model):
    user_id = models.IntegerField()             # 작성자 (간단히 정수)
    title = models.CharField(max_length=200)
    content = models.TextField()
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "movies"; ordering = ["-created_at"]
```
> `user_id` 를 정수로 둔 건 학습 단순화. 실무 정석은 `ForeignKey` → [CONCEPTS.md # FK vs IntegerField](CONCEPTS.md#fk-vs-integerfield)

## 3-3. 이미지 업로드 세팅 (3곳)
```python
# requirements.txt → Pillow (포함됨)
# config/settings/base.py
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# config/urls.py
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
- 사진은 JSON이 아니라 **multipart/form-data** 로 보냄. 파일은 `media/`에 저장되고 DB엔 경로만.
> → 저장~화면 전체 흐름·MEDIA·파일명 충돌 등: [CONCEPTS.md # 이미지](CONCEPTS.md#이미지)

## 3-4. Comment 모델 (`movies/models.py`)
```python
class Comment(models.Model):
    user_id = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")  # 1:N
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "comments"; ordering = ["created_at"]
```

## 3-5. Serializer (`movies/serializers.py`) — 목록/상세/생성 분리
```python
class MovieListSerializer(serializers.ModelSerializer):       # 목록 = 이미지+제목만
    class Meta: model = Movie; fields = ["id", "title", "poster"]

class MovieSerializer(serializers.ModelSerializer):           # 생성 입력용
    class Meta:
        model = Movie
        fields = ["id", "user_id", "title", "content", "poster", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user_id", "movie", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "movie", "created_at", "updated_at"]

class MovieDetailSerializer(serializers.ModelSerializer):     # 상세 = 전부 + 댓글
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ["id", "user_id", "title", "content", "poster", "comments", "created_at", "updated_at"]
```
**왜 나눠?** 같은 영화라도 목록/상세에서 보여줄 양이 달라요:
```jsonc
// GET /movies   (목록) — 카드에 필요한 3개만
[ { "id": 1, "title": "인터스텔라", "poster": "http://.../poster.png" } ]
// GET /movies/1 (상세) — 글·댓글까지 전부
{ "id": 1, "title": "인터스텔라", "content": "인생영화",
  "poster": "http://.../poster.png", "comments": [ { "id": 1, "content": "동의" } ] }
```
> → 더 깊이(검증 레이어·성능 이유): [CONCEPTS.md # Serializer 분리](CONCEPTS.md#serializer-분리)

## 3-6. 뷰 (`movies/views.py` · `movies/urls.py`)
```python
class MovieView(APIView):
    parser_classes = [MultiPartParser]            # multipart 전용 → Swagger에 파일선택 칸
    def get(self, request):                        # 목록
        movies = Movie.objects.all()
        return Response(MovieListSerializer(movies, many=True, context={"request": request}).data)
    def post(self, request):                       # 생성 (+포스터)
        s = MovieSerializer(data=request.data, context={"request": request})
        s.is_valid(raise_exception=True); s.save()
        return Response(s.data, status=201)

class MovieDetailView(APIView):
    def get(self, request, movie_id):              # 상세
        movie = get_object_or_404(Movie, id=movie_id)
        return Response(MovieDetailSerializer(movie, context={"request": request}).data)

class CommentCreateView(APIView):
    def post(self, request, movie_id):             # 댓글
        movie = get_object_or_404(Movie, id=movie_id)
        s = CommentSerializer(data=request.data)
        s.is_valid(raise_exception=True); s.save(movie=movie)
        return Response(s.data, status=201)
```
```python
# movies/urls.py
urlpatterns = [
    path("movies", MovieView.as_view()),                                 # GET 목록 · POST 생성
    path("movies/<int:movie_id>", MovieDetailView.as_view()),            # GET 상세
    path("movies/<int:movie_id>/comments", CommentCreateView.as_view()), # POST 댓글
]
```
> 가장 단순한 `APIView` 를 쓴 이유 → [CONCEPTS.md # 왜 APIView](CONCEPTS.md#왜-apiview)

## 3-7. API 명세

| 기능 | Method | URL | Body |
|---|---|---|---|
| 회원가입 | POST | `/api/v1/users/signup` | `{email, password}` |
| 로그인 | POST | `/api/v1/users/login` | `{email, password}` |
| 영화 목록 | GET | `/api/v1/movies` | — |
| 영화 등록 | POST | `/api/v1/movies` | **form-data** `user_id, title, content, poster(파일)` |
| 영화 상세 | GET | `/api/v1/movies/{id}` | — |
| 댓글 작성 | POST | `/api/v1/movies/{id}/comments` | `{user_id, content}` |

> ✅ **여기까지** — 영화 등록(사진)·목록·상세·댓글 API 완성! Swagger나 curl로
> ① 영화 등록(poster 파일) → ② 목록 GET → ③ 상세 GET(댓글 포함) 순으로 확인하세요.

---

# 4. 확장하기

| 확장 | 무엇을 |
|---|---|
| 별점 | `rating`(1~5) 필드 + 평균 |
| 작성자 FK | `user_id` 정수 → `ForeignKey(User)` |
| 인증 | 간단 로그인 → JWT 토큰 |
| 조회 편의 | 페이지네이션·검색·정렬 |
| 실시간 | WSGI → ASGI(+Channels) → [CONCEPTS.md # WSGI vs ASGI](CONCEPTS.md#wsgi-vs-asgi) |
| 프론트 | React(Vite)+axios, 사진은 FormData, CORS |

> 💡 React 프론트 연동 구현이 이 저장소에 **함께** 있어요 → [../frontend](../frontend) (게시판·상세·작성 화면 + jsonAxios/formAxios)

---

# 부록 A. 명령어 치트시트
```bash
source venv/bin/activate             # 가상환경 (윈도우: venv\Scripts\activate)
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver           # 포트: runserver 8080
python manage.py createsuperuser     # /admin
```

# 부록 B. 자주 나는 에러

| 증상 | 해결 |
|---|---|
| `ModuleNotFoundError: django` | 가상환경 안 켬 → `source venv/bin/activate` (윈도우 `venv\Scripts\activate`) |
| `Cannot use ImageField ... Pillow` | `pip install Pillow` (requirements에 포함) |
| 모델 바꿨는데 반영 안 됨 | `makemigrations` → `migrate` 다시 |
| 맞는 주소인데 404 | URL 끝 슬래시 (`/movies/1/`❌ → `/movies/1`✅) |
| Swagger 입력칸/파일선택 안 뜸 | 브라우저 하드 새로고침 `Cmd/Ctrl+Shift+R` |
| 사진이 안 보임 | 응답 `poster`가 전체 URL인지, `DEBUG=True`에서 media 서빙 중인지 |
| 프론트에서 `CORS policy ... blocked` | `corsheaders` 설치·`INSTALLED_APPS`·미들웨어 위치 확인, `CORS_ALLOWED_ORIGINS` 에 프론트 주소(5173) 있는지 |

---

> 📘 **개념·"왜"가 더 궁금하면 → [CONCEPTS.md](CONCEPTS.md)** (settings 분리, 이미지 저장 흐름, serializer 분리, FK vs Int, WSGI/ASGI 등)
