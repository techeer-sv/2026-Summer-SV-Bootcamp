# 백엔드 기초 핸즈온 — 영화 리뷰 게시판 만들기 (Django REST API)

> "백엔드 기초 & API 설계" 세션의 후속 실습 자료입니다.
> 세션이 **요청 → 처리 → 응답** 이라는 백엔드의 "숲"을 다뤘다면,
> 이 자료는 그 숲을 **직접 손으로** 걸어보는 가이드예요. 회원가입부터 **영화 글(사진 포함)·댓글**까지,
> REST API를 한 바퀴 굴려봅니다.

---

## 만들 결과물 (화면 구성)

영화 게시판입니다. 게시판에 올라가는 한 건이 곧 **영화 한 편**이라 모델 이름은 `Movie`.


| 화면 | 보여주는 것 | 쓰는 시리얼라이저 |
|---|---|---|
| **게시판 목록** | 영화 **이미지 + 제목** | `MovieListSerializer` (가벼움) |
| **상세(클릭)** | 제목 + 사진 + 리뷰 글 + **댓글** | `MovieDetailSerializer` (전부) |

> 같은 데이터라도 **목록은 가볍게, 상세는 전부** — 화면에 맞춰 시리얼라이저를 나누는 게 핵심 포인트.

## 📑 목차 (이 자료는 어떻게 펴볼까요)

> 실습 중엔 필요한 데로 바로 점프하세요. 제목 클릭 = 해당 섹션 이동.

| 파트 | 무엇을 하나요 |
| --- | --- |
| [0. 환경 세팅](#0-환경-세팅) | 가상환경, 프로젝트 생성, **settings 분리**, 앱 나누기. |
| [1. 회원(User)](#1-user-앱--회원가입로그인-먼저) | 가장 단순한 기능으로 API 한 바퀴 먼저. (회원가입·로그인) |
| [2. 실행 & 테스트](#2-실행--테스트) | 서버 띄우고 **Swagger·Postman·curl** 로 눌러보기. |
| [3. 영화 게시판(Movie/Comment)](#3-영화-게시판--movie--comment) | 모델 → **이미지 업로드** → 목록/상세 시리얼라이저 + 댓글. |
| [4. 확장하기](#4-확장하기-실무로-가면) | 별점·인증·검색으로 키우기. |
| [후속](#후속-실습--프론트엔드-연동) | **프론트엔드 연동**(React) — 다음 차시. |
| [부록](#부록-a-명령어-치트시트) | 명령어 치트시트, 자주 나는 에러. |

> 각 단계마다 **무엇을 / 왜** 를 같이 적어 뒀어요.

## 왜 Django로 하나요

FastAPI, Flask도 있지만 Django가 가장 **규격화**되어 있어 큰 틀을 이해하기 좋고,
다른 프레임워크로 넘어가기도 수월해요. 그래서 Django 하나로 진행합니다.

## 데이터 구조 (ERD)

```
회원가입 / 로그인  +  영화 글 / 댓글
User                Movie(제목 + 포스터이미지 + 리뷰글) 1 ──< N Comment
```

| 도메인 | 앱 | 모델 → 테이블 | 기능 |
|---|---|---|---|
| 회원 | `users` | `User` → `users` | 회원가입, 로그인 |
| 영화 | `movies` | `Movie` → `movies`, `Comment` → `comments` | 영화 글 목록·생성·상세 (**포스터 업로드**) + 댓글 |

> **앱 ≠ 테이블.** 앱은 코드 묶음(폴더), 테이블은 그 안 모델이 만든다.
> `movies` 앱 하나에 `movies`·`comments` **두 테이블**이 들어 있어요.

## 📂 파일 구조 — "어느 파일에 쓰나요?"

```
django-board-handson/
├── manage.py                 # 장고 명령 입구
├── requirements.txt          # 패키지 목록
├── docker-compose.yml        # MySQL (도커)
├── config/                   # 프로젝트 설정·진입점
│   ├── settings/             #   base.py · dev.py · prod.py (환경 분리)
│   └── urls.py               #   최상위 URL → 각 앱으로 연결
├── users/                    # 회원 앱
│   ├── models.py  views.py  urls.py
└── movies/                   # 영화 게시판 앱
    ├── models.py             #   Movie · Comment (테이블)
    ├── serializers.py        #   목록/상세/생성 변환·검증
    ├── views.py              #   요청 처리 (제일 많이 만짐)
    └── urls.py               #   /api/v1/movies …
```

> 💡 각 단계 **제목 옆 `(파일명)`** 이 곧 **그 단계에서 만지는 파일**이에요. 길 잃으면 여기로.

---

# 0. 환경 세팅

## 0-1. 가상환경 만들고 장고 설치

처음부터 직접 만든다면 이 순서예요.
(이미 받은 레포로 시작하면 4번 대신 `pip install -r requirements.txt` 한 줄)

```bash
# 1. 작업 폴더 만들고 이동
mkdir django-board-handson && cd django-board-handson

# 2. 가상환경 생성  (venv 라는 폴더가 생김)
python3 -m venv venv

# 3. 가상환경 활성화 (맥/리눅스)   ── 윈도우: venv\Scripts\activate
source venv/bin/activate

# 4. 장고 설치
pip install django
```
> **왜** 가상환경? 프로젝트마다 패키지 버전이 안 섞이게 격리하려고.
> 활성화되면 프롬프트 앞에 `(venv)` 가 붙어요.

## 0-2. 프로젝트 생성 — `startproject` 하면 뼈대가 생긴다

```bash
# 5. 장고 프로젝트 생성 (현재 폴더에)  ── 끝의 점(.) = '바로 여기에'
django-admin startproject config .
```

위 명령을 **처음에 한 번** 치면, 아래 구조가 **자동으로 생겨요**:

```
django-board-handson/
├── manage.py            # 장고 명령 실행 입구 (runserver, migrate …)
└── config/              # 프로젝트 설정 묶음
    ├── __init__.py
    ├── settings.py      # ← 설정 한 파일. 우리는 이걸 settings/ 폴더로 쪼갬 (0-3)
    ├── urls.py          # 최상위 URL 진입점
    ├── wsgi.py          # 배포(동기) 실행 진입점
    └── asgi.py          # 배포(비동기) 실행 진입점
```

- **프로젝트(`config`)** = 전체 설정·진입점 한 덩어리.
  (끝의 `.` 을 빼면 `config` 폴더가 한 겹 더 깊게 생기니 주의)
- 그다음 **앱(app)** 을 만들어 붙여요. 이것도 명령 한 번이면 폴더가 생겨요:
  ```bash
  python manage.py startapp users      # users/ 앱 생성 (models.py, views.py … 자동)
  python manage.py startapp movies     # movies/ 앱 생성
  ```

## 0-3. settings 분리 (base / dev / prod) ★핵심

`startproject` 는 `settings.py` 한 파일을 만들어요. 그런데 개발과 배포는 값이 달라요.
한 파일에서 `if` 로 분기하면 금방 지저분해져서 **셋으로 쪼갭니다.**

```
config/settings/
├── base.py   # 항상 같은 공통 설정 (앱 목록, 미들웨어, 언어, MEDIA…)
├── dev.py    # 로컬 개발에서만 다른 값
└── prod.py   # 배포(도커)에서만 다른 값
```

`dev.py`/`prod.py` 는 맨 위에서 `from .base import *` 로 공통을 가져오고, **다른 부분만** 덮어써요.

| 항목 | dev (개발) | prod (배포) | 왜 다른가 |
|---|---|---|---|
| `DEBUG` | `True` | `False` | 개발은 에러를 자세히 / 운영은 노출되면 보안사고 |
| DB `HOST` | `127.0.0.1` | `mysqldb` | 백엔드를 **로컬 실행 vs 도커 실행** (아래) |
| `ALLOWED_HOSTS` | `*` | 운영 도메인만 | 개발 편의 / 운영 보안 |
| 비밀값 | 코드에 둬도 OK | `.env` 로 숨김 | 깃에 비번 올리면 유출 |

**DB HOST가 갈리는 지점**:
```
[dev]  내 PC에서 runserver  ──▶ 도커 MySQL   HOST = 127.0.0.1  (localhost = 내 컴퓨터)
[prod] 백엔드도 도커 컨테이너 ──▶ 도커 MySQL   HOST = mysqldb    (컨테이너끼리는 '이름'으로 찾음)
```

**`.env` 를 쓰는 이유(prod)**: `SECRET_KEY`·DB 비번 같은 민감값을 코드에 적어 깃에 올리면 유출돼요.
그래서 `.env` 에 적고 읽어오며, `.env` 는 `.gitignore` 로 제외합니다. (`.env.example` 만 공유)

> 어떤 설정으로 도는지는 `DJANGO_SETTINGS_MODULE` 이 정해요:
> `manage.py` → 기본 `config.settings.dev`, `wsgi.py`/`asgi.py` → 기본 `config.settings.prod`.

## 0-4. `APPEND_SLASH = False`

장고 기본값은 `True` 라 URL 끝에 `/`가 강제로 붙어요(`/movies` → `/movies/`).
끝 슬래시가 싫어서 `False` 로 끕니다. → **URL은 끝 슬래시 없이 설계.**

## 0-5. 앱을 도메인별로 나눠요

- `users`/`movies`는 **장고 규칙이 아니라 우리가 만든 앱**이고 이름도 우리가 붙였어요.
- 장고는 "프로젝트를 여러 앱으로 나눠 써라"까지만 정하고, **몇 개로·무슨 이름인지는 자유.**
- 기준 = **비즈니스 도메인.** (배민이면 `users`·`restaurants`·`orders`·`delivery` …)
- **왜 나누나** : 응집도·유지보수(고칠 때 그 앱만)·협업·재사용. 작으면 한 앱에 다 넣어도 OK.

**프로젝트/앱 구조** (점프 투 장고의 `mysite`/`pybo` 와 같은 구성):

```
config/             # 프로젝트 (= 책의 mysite) — 설정·진입점
users/              # 앱: 회원
movies/             # 앱: 영화 게시판 (= 책의 pybo 자리)
 ├─ models.py       # class Movie, class Comment   → DB 테이블 (모델 = 테이블)
 ├─ views.py        # 기능 구현 (제일 많이 씀)
 ├─ serializers.py  # 목록용/상세용 JSON 변환   (startapp엔 없음 · 우리가 추가)
 ├─ urls.py         # /api/v1/movies …          (startapp엔 없음 · 우리가 추가)
 ├─ admin.py        # 관리자 화면 등록
 ├─ apps.py         # 앱 구성 정보 (보통 안 건드림)
 └─ migrations/     # 테이블 생성·수정 기록
```

> `python manage.py startapp movies` 를 치면 `models.py`·`views.py`·`admin.py`·`apps.py`·`migrations/`
> 까지는 **자동 생성**돼요. `serializers.py`·`urls.py` 두 개만 우리가 직접 추가합니다.

## 0-6. Swagger 세팅 (API 자동 문서)

`drf-spectacular` 로 API 문서를 자동 생성해요. `config/urls.py` 에
`/swagger`(사람용 화면)와 `/api/schema`(기계용 원본)를 연결해 뒀어요.

---

# 1. User 앱 — 회원가입/로그인 먼저

회원가입 로직부터 짜요 (서비스 만들 때 가장 흔한 출발점).

> **왜 장고 기본 auth 를 안 쓰나?** 처음부터 빡빡하게 만들면 뒤 기능 테스트가 힘들어져요.
> 그래서 이메일/비번 아무거나 넣으면 가입되게 **아주 간단히** 시작.

## 1-1. 모델 (`users/models.py`)

```python
class User(models.Model):
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)   # 학습용 평문 (실무는 해시!)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시점 자동
    updated_at = models.DateTimeField(auto_now=True)      # 수정 시점 자동

    class Meta:
        db_table = "users"   # 테이블 이름 (복수형)
```
- `auto_now_add`/`auto_now` → 값을 안 넣어도 시간이 **자동**으로 채워져요.
- **`class Meta` = 그 테이블에 대한 추가 설정**(메타데이터). 필드가 아니라 데이터에 대한 정보.

## 1-2. 뷰 (`users/views.py`) — 클래스형 + JsonResponse + ORM

```python
class SignupView(APIView):          # 클래스형이 가독성 좋음
    def post(self, request):        # 메서드명 = HTTP 메서드 (회원가입은 POST)
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:                       # 기초 예외처리
            return JsonResponse({"message": "..."}, status=400)
        if User.objects.filter(email=email).exists():       # 중복 확인 (ORM)
            return JsonResponse({"message": "..."}, status=400)
        user = User.objects.create(email=email, password=password)  # 생성
        return JsonResponse({"message": "회원가입 성공",
                             "user_id": user.id, "user_email": user.email}, status=201)
```
- **ORM** = `User.objects.filter()/create()` 처럼 SQL을 직접 안 짜도 DB에 접근하게 해주는 것.
- **로그인도 POST** 로 해요. 이메일/비번을 URL에 실으면 노출되니까 body로. 실패 시 401.

## 1-3. URL (`users/urls.py`) — 동사형 예외

```python
urlpatterns = [
    path("users/signup", SignupView.as_view()),
    path("users/login", LoginView.as_view()),
]
```
> REST 원칙은 '동사 말고 명사'지만, signup/login 은 **둘 다 POST라 URL로 구분이 안 돼요.**
> 이럴 때는 **예외적으로 동사**를 씁니다. (URI 원칙은 [3-7 박스](#rest-uri-동사-말고-명사--movies-는-써도-되나) 참고)

## 1-4. 진입점 연결 (`config/urls.py`)

요청은 `config/urls.py`(기본 진입점)로 먼저 들어와 각 앱 urls 로 위임돼요.
```python
path("api/v1/", include("users.urls")),   # api/v1 접두사는 버전관리용 (선택)
```

> 📚 **더 깊이 보기** — 점프 투 장고(wikidocs)의 "모델/뷰/URL" 장, Django 공식 튜토리얼 1~3부.

---

# 2. 실행 & 테스트

## 2-1. DB 준비 (도커 MySQL)

```bash
docker compose up -d             # MySQL 컨테이너 띄우기 (포트 3306)
pip install -r requirements.txt  # (STEP 1에서 했으면 생략) mysqlclient 포함
```
> ⚠️ `Access denied for user 'root'` 가 나면 — 로컬에 이미 MySQL이 3306을 쓰는 중이에요. 로컬 MySQL을 잠깐 끄세요:
> - **맥**: `brew services stop mysql` (끝나면 `brew services start mysql`)
> - **윈도우**(관리자 cmd): `net stop MySQL80` (서비스명은 MySQL80/MySQL84 등) — 또는 `services.msc`에서 MySQL 중지

## 2-2. 마이그레이션 → 서버 실행

```bash
python manage.py makemigrations   # 모델 변경을 '마이그레이션 파일'로 기록
python manage.py migrate          # 그 파일을 실제 DB에 반영 (테이블 생성)
python manage.py runserver        # http://127.0.0.1:8000  (끄기: Ctrl+C)
```
> 모델(`models.py`)을 고칠 때마다 `makemigrations` → `migrate` 를 다시 해요.

> ⚠️ **초보 주의** — `makemigrations` 만 하고 `migrate` 를 **안 하는** 경우가 정말 많아요.
> `makemigrations`(설계도 파일 만들기) → `migrate`(DB에 실제 반영) **둘 다** 해야 테이블이 생깁니다.

## 2-3. Swagger 보는 법

브라우저: **http://127.0.0.1:8000/swagger**
1. 내가 만든 API 목록이 자동으로 떠요.
2. 테스트할 API 클릭 → **`Try it out`** → 값 입력 → **`Execute`**
3. 아래 **Response** 에 상태코드(201)·응답 확인.

## 2-4. 다른 테스트 방법

- **Postman**: Method/URL 지정, Body raw JSON (사진 업로드는 `form-data`). **끝 슬래시 X.**
- **curl**:
  ```bash
  curl -X POST http://127.0.0.1:8000/api/v1/users/signup \
    -H "Content-Type: application/json" \
    -d '{"email":"test@gmail.com","password":"123"}'
  ```

## 2-5. DB에 들어갔는지 확인

- MySQL: DataGrip/DBeaver → host `127.0.0.1`, port `3306`, user `root`, pw `1234`, db `mydatabase`.

---

# 3. 영화 게시판 — Movie / Comment

## 3-1. 모델부터 짜요 (왜?)

ERD를 **먼저** 그리고, 거기에 맞게 클래스를 설계해 들어가요.
> 로직 짜다가 즉흥적으로 컬럼을 추가하면 설계가 엉켜요. 그래서 **ERD → 모델 → 로직** 순서.

## 3-2. Movie 모델 (`movies/models.py`) — 제목 + 포스터 이미지 + 리뷰 글

```python
class Movie(models.Model):                      # 게시판 한 건 = 영화 한 편
    user_id = models.IntegerField()             # 작성자 (간단히 정수로)
    title = models.CharField(max_length=200)    # 영화 제목
    content = models.TextField()                # 리뷰 내용 (영화에 대한 글)
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)  # 영화 이미지
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "movies"
        ordering = ["-created_at"]              # 최신순 ('-' = 내림차순)
```

> **모델 이름 `Movie` vs HTTP 메서드 `POST`?** 둘은 다른 거예요. `Movie`는 데이터(클래스) 이름,
> `POST`는 보내는 방식. 게시판에 올라가는 게 영화라서 모델을 `Movie`로 지었어요.

**작성자(`user_id`)를 받는 두 방법** — 지금은 ②:

| | ① ForeignKey | ② IntegerField (지금) |
|---|---|---|
| 코드 | `user = models.ForeignKey('users.User', on_delete=CASCADE)` | `user_id = models.IntegerField()` |
| `movie.user` | User **객체** 바로 접근 | 불가 (그냥 숫자 `1`) |
| 무결성 | 존재하는 유저만 | 없는 id도 그냥 저장됨 |
> **왜 정수?** 처음엔 단순하게. 실무 정석은 FK. (→ [4. 확장](#4-확장하기-실무로-가면)에서 FK로 강화)

**`poster` 가 이미지 필드 ★** — 실제 파일은 `media/posters/` 에 저장, **DB엔 경로만** 들어가요.

## 3-3. 이미지 업로드 세팅 — 사진은 텍스트와 처리가 달라요

- **🎯 목표** : `poster` 사진을 올리고·저장하고·보여줄 수 있게
- **✏️ 수정 파일** : `requirements.txt` · `config/settings/base.py` · `config/urls.py`
- **✅ 해야 할 것** : ① Pillow 설치 ② MEDIA 설정 ③ media 서빙 ④ 요청을 form-data로

아래가 그 네 군데예요. (각 단계의 *왜* 는 설명 참고)

**① 패키지** (`requirements.txt` 에 포함)
```bash
pip install Pillow
```
**② 저장 위치 (`config/settings/base.py`)**
```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```
**③ 개발 중 사진 서빙 (`config/urls.py`)**
```python
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
**④ 요청 형식이 JSON → multipart/form-data** (사진이 끼면 JSON으로 못 보냄)
```bash
curl -X POST http://127.0.0.1:8000/api/v1/movies \
  -F "user_id=1" -F "title=인터스텔라" -F "content=인생영화" -F "poster=@./poster.jpg"
```
> 세션 슬라이드의 *"사진·파일 보낼 땐 form-data"* 와 같은 이야기.

### 이미지, 더 자세히 — 저장부터 화면까지

**1) 저장: 파일은 디스크에, DB엔 "경로"만**
```
업로드한 poster.png
 ├─ 실제 파일  → media/posters/poster.png        (디스크에 저장)
 └─ DB movies.poster 칼럼 → "posters/poster.png"  (경로 문자열만!)
```
- `ImageField` = `FileField`(파일 저장) + "진짜 이미지인지 검증". 그 검증을 **Pillow**가 해서 Pillow가 필요해요.
- `upload_to="posters/"` = `MEDIA_ROOT` 아래 `posters/` 폴더에 저장하라는 뜻.
- **왜 경로만 DB에 넣나?** 사진 자체를 DB에 통째로 넣으면 DB가 무거워지고 느려져요.
  파일은 파일시스템(또는 S3)에 두고, DB는 "어디 있는지(경로)"만 가리키는 게 정석.

**2) 업로드 흐름 (요청 → 저장)**
```
[프론트] 파일을 multipart/form-data 로 POST /movies
  → [DRF] MultiPartParser가 파일을 꺼냄 (request.FILES)
  → serializer.is_valid()  : 진짜 이미지인지 검증
  → serializer.save()      : media/posters/ 에 파일 쓰고, DB엔 경로 저장
  → 응답 poster: "http://localhost:8000/media/posters/poster.png"
```

**3) 보여주는 흐름 (저장 → 브라우저)**
```
브라우저가 그 URL 요청 → http://localhost:8000/media/posters/poster.png
  → (DEBUG=True) Django가 MEDIA_ROOT 에서 파일을 찾아 돌려줌
  → <img src="...poster.png"> 로 화면에 뜸
```

**MEDIA_URL vs MEDIA_ROOT** (이름이 비슷해 헷갈림)

| | 뜻 | 예 |
|---|---|---|
| `MEDIA_ROOT` | **디스크** 어디에 저장하나 | `.../django-board-handson/media` |
| `MEDIA_URL` | **웹 주소** 접두사 | `/media/` |

→ 파일 `media/posters/x.png` ↔ 주소 `/media/posters/x.png` 가 1:1로 짝지어져요.

**자잘하지만 중요한 것들**
- **왜 JSON 말고 form-data?** JSON은 글자(텍스트)용. 이미지는 바이너리라 안 맞아서 `multipart/form-data` 로 보내요.
- **절대 URL** : 뷰에서 `context={"request": request}` 를 안 주면 poster가 `/media/...`(상대경로)로 나와요.
  프론트가 다른 포트(5173)에서 부르면 **절대 URL**이라야 `<img>` 에 바로 꽂혀요.
- **파일명 충돌** : 같은 이름을 또 올리면 장고가 알아서 `poster_aB3xK.png` 처럼 뒤에 랜덤을 붙여 **덮어쓰기를 막아요.**
- **`blank=True, null=True`** : 포스터 없이도 등록 가능. `null`=DB가 빈 값 허용, `blank`=검증(폼)에서 빈 값 허용.
- **운영(prod)에선** : Django가 직접 이미지를 서빙하지 않아요. **nginx나 S3**가 맡습니다.
  `static(settings.MEDIA_URL, ...)` 줄이 `if settings.DEBUG:` 안에 있는 이유예요(개발 전용).

## 3-4. Comment 모델 — FK (1:N)

```python
class Comment(models.Model):
    user_id = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    ...
    class Meta:
        db_table = "comments"
        ordering = ["created_at"]
```
- 댓글은 **FK로 영화(Movie)에 연결** → Movie 1 : Comment N (1:N).

## 3-5. Serializer (`movies/serializers.py`) — 화면에 맞춰 목록용 / 상세용 분리 ★

이 실습의 핵심 포인트. **같은 영화라도** 목록과 상세에서 보여줄 게 달라요.

```python
# 목록용 — 게시판엔 이미지 + 제목만
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "poster"]

# 생성(입력)용 — write serializer
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "user_id", "title", "content", "poster", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

# 상세용 — 제목·사진·글 + 댓글(nested)까지 전부
class MovieDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ["id", "user_id", "title", "content", "poster", "comments", "created_at", "updated_at"]
```
- **직렬화** = 객체 → JSON / **역직렬화** = JSON → 객체.
- `poster` 는 응답 시 **전체 URL**(`http://.../media/posters/xxx.jpg`)로 나가요 (뷰에서 request context 전달).

**왜 셋으로 나누나** — 같은 영화라도 상황마다 필요한 게 달라요:

| 상황 | 시리얼라이저 | fields | 이유 |
|---|---|---|---|
| 목록(게시판) | `MovieListSerializer` | id·title·poster | 카드엔 포스터+제목만. content·comments까지 보내면 **payload↑·DB쿼리↑·렌더링 느려짐** |
| 생성(입력) | `MovieSerializer` | 입력 필드 | **검증이 핵심**(required·길이·이미지 형식) = write용 |
| 상세(클릭) | `MovieDetailSerializer` | 전부 + comments | 정보가 많이 필요 = 가장 무거움 |

- **댓글은 nested** : `comments = CommentSerializer(many=True, read_only=True)` → Movie 1 : Comment N 을 응답에 함께.
- **꼭 3개로 나눠야 하나?** 작은 프로젝트는 하나로도 OK. 하지만 커지면 — 댓글 500개 달린 글 20개를
  목록 조회하면 `20 × 500` nested 직렬화로 **API가 터져요.** 그래서 분리.
- **user_id 참고** : 지금은 인증이 없어 클라이언트가 `user_id` 를 직접 보내요. 실무에선 보통 안 보내고
  뷰에서 `serializer.save(user=request.user)` 로 채우고 `read_only_fields=["user_id"]` 로 둬요.
  (→ [4. 확장: 인증](#4-확장하기-실무로-가면))

## 3-6. 뷰 (`movies/views.py` · `movies/urls.py`) — 화면별로 시리얼라이저를 골라 씀 (미니멀 3기능)

```python
class MovieView(APIView):
    def get(self, request):                      # 게시판 목록 → 이미지+제목
        movies = Movie.objects.all()
        return Response(MovieListSerializer(movies, many=True, context={"request": request}).data)
    def post(self, request):                     # 카드 생성 (+포스터)
        serializer = MovieSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class MovieDetailView(APIView):
    def get(self, request, movie_id):            # 상세 → 제목·사진·글·댓글 전부
        movie = get_object_or_404(Movie, id=movie_id)
        return Response(MovieDetailSerializer(movie, context={"request": request}).data)

class CommentCreateView(APIView):
    def post(self, request, movie_id):           # 상세에 보여줄 댓글 작성
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(movie=movie)
        return Response(serializer.data, status=201)
```
- 포스터 업로드는 `MovieView`에 `parser_classes=[MultiPartParser]` 로 **multipart 전용** 지정 (Swagger에 파일선택 칸이 떠요).
- 수정·삭제 기능은 미니멀하게 뺐어요 (목록·생성·상세 + 댓글만). 필요하면 [4. 확장](#4-확장하기-실무로-가면)에서 추가.

> **왜 `APIView`?** DRF엔 `APIView` / `GenericAPIView` / `ViewSet` 이 있어요. 지금은 GET/POST 흐름을
> 직접 눈으로 보려고 **가장 단순한 `APIView`** 를 써요. 실무에선 반복 CRUD에 `ViewSet` 을 많이 씁니다.

**URL 연결 (`movies/urls.py`)** — 뷰를 만들었으면 URL에 연결해야 동작해요:
```python
# movies/urls.py
urlpatterns = [
    path("movies", MovieView.as_view()),                                 # GET 목록 · POST 생성
    path("movies/<int:movie_id>", MovieDetailView.as_view()),            # GET 상세
    path("movies/<int:movie_id>/comments", CommentCreateView.as_view()), # POST 댓글
]
# config/urls.py 에서 연결:  path("api/v1/", include("movies.urls"))
```

## 3-7. API 명세 (영화 게시판 — 미니멀)

| 기능 | Method | URL | Body | 응답 |
|---|---|---|---|---|
| 회원가입 | POST | `/api/v1/users/signup` | `{email, password}` | 201 |
| 로그인 | POST | `/api/v1/users/login` | `{email, password}` | 200 |
| 게시판 목록(이미지+제목) | GET | `/api/v1/movies` | — | `[{id, title, poster}]` |
| 카드 생성 | POST | `/api/v1/movies` | **form-data** `user_id, title, content, poster(파일)` | 201 전체 |
| 상세(제목·사진·글·댓글) | GET | `/api/v1/movies/{id}` | — | 전체 + `comments` |
| 댓글 작성 | POST | `/api/v1/movies/{id}/comments` | `{user_id, content}` | 201 |



---

# 4. 확장하기 (실무로 가면)

| 확장 | 무엇을 | 비고 |
|---|---|---|
| **별점** | 영화에 `rating`(1~5) 필드 + 평균 별점 | 리뷰다움 ↑ |
| **작성자 FK** | `Movie.user_id` 정수 → `ForeignKey(User)` | 무결성·`movie.user` 접근 |
| **인증** | 간단 로그인 → **JWT 토큰** | 처음엔 일부러 미룸 |
| **조회 편의** | 페이지네이션·검색(`?keyword=`)·필터·정렬 | 목록이 커지면 |
| **실시간** | 채팅/알림 → **WSGI → ASGI**(+Channels) | 아래 참고 |

### (참고) WSGI vs ASGI
- **WSGI(동기)** = 일반 CRUD엔 충분(지금 우리). **ASGI(비동기)** = 웹소켓 등 실시간.
- FastAPI는 ASGI 전용, Django는 원래 WSGI지만 ASGI도 지원(그래서 `wsgi.py`/`asgi.py` 둘 다 있음).

---

# 후속 실습 — 프론트엔드 연동

> 백엔드 API는 완성됐어요. **다음 차시**는 화면을 붙이는 일입니다.

화면 흐름은 위 [만들 결과물](#만들-결과물-화면-구성) 그대로예요:
- **목록 화면** → `GET /movies` 로 받은 `{title, poster}` 를 카드로 (이미지+제목)
- **상세 화면** → 카드 클릭 시 `GET /movies/{id}` 로 제목·사진·글·댓글 전부
- **등록 화면** → 사진은 JSON이 아니라 **FormData** 로 업로드 (백엔드와 짝)
```js
const form = new FormData();
form.append("title", title);
form.append("content", content);
form.append("poster", file);     // <input type="file"> 에서 고른 파일
await axios.post("http://localhost:8000/api/v1/movies", form);
```
- 프론트(5173) → 백엔드(8000)는 출처가 달라서 **CORS** 를 풀어줘야 해요
  → `pip install django-cors-headers` 후 settings 등록.


### 정리
```
이번 차시:  회원 + 영화 글(사진 포함) + 댓글 — 백엔드 REST API 완성 ✅
다음 차시:  React 프론트 (목록=이미지+제목 / 상세=전부 + FormData 업로드 + CORS)
```

---

# 세션 슬라이드 ↔ 이 가이드 매핑

| 슬라이드 주제 | 식당 비유 | 이 가이드 |
| --- | --- | --- |
| API — 요청 받기 | 메뉴판 | [1. User 앱](#1-user-앱--회원가입로그인-먼저) |
| REST · 메소드 · 설계 | 주문서 양식 | [3-7 API 명세 + URI 원칙](#3-7-api-명세-영화-게시판), [0-4 URL 설계](#0-4-append_slash--false) |
| HTTP Method / 상태코드 | 주문이 도는 길 | [3. 영화 목록·생성·상세](#3-영화-게시판--movie--comment) (200/201/400/404) |
| JSON / form-data | 주문서 양식 | [3-3 이미지 업로드](#3-3-이미지-업로드--사진은-텍스트와-처리가-달라요) |
| DB · ORM | 냉장고 | [1-1 모델](#1-1-모델-usersmodelspy), [2-2 마이그레이션](#2-2-마이그레이션--서버-실행) |
| 로그인 · 토큰 | 단골 도장 | [1-2 로그인](#1-2-뷰-usersviewspy--클래스형--jsonresponse--orm), [4. 확장](#4-확장하기-실무로-가면) |
| 테스트 | 시식·검수 | [2. 실행 & 테스트](#2-실행--테스트) |

---

# 더 깊이 보기 — 외부 레퍼런스

| 자료 | 특징 |
| --- | --- |
| **점프 투 장고** (wikidocs) | 한국어 입문 정석. 모델·뷰·URL 단계별. |
| **Django 공식 문서** — docs.djangoproject.com | "왜 이렇게 동작하는가"가 단단함. |
| **DRF 공식 문서** — django-rest-framework.org | Serializer·View·파일 업로드의 출처. |
| **FastAPI 공식 문서** (비교용) | 같은 API를 다른 프레임워크로 보면 개념이 또렷해져요. |

---

# 검증 환경

- macOS (Apple Silicon), Python 3.12 · Django 5.1 · DRF 3.15 · Pillow 에서 전 과정 동작 확인.
- DB는 **MySQL(도커)** 사용.
- 회원가입·로그인·영화 글 목록·생성·상세·**포스터 이미지 업로드**·목록(이미지+제목)/상세(전부)·댓글·Swagger 통과.

# ⚠️ 이 자료에서 안 다루는 것

- **비밀번호 해시·세션·JWT** — 회원가입을 평문으로 단순화. 인증은 [4. 확장](#4-확장하기-실무로-가면)에서.
- **작성자 권한 체크** — 지금은 누구나 수정/삭제 가능.
- **이미지 리사이즈·용량 제한·썸네일** — 업로드 자체만.
- **프론트엔드** — [후속 차시](#후속-실습--프론트엔드-연동).

---

# 부록 A. 명령어 치트시트

```bash
source venv/bin/activate             # 가상환경 켜기 (윈도우: venv\Scripts\activate)
pip install -r requirements.txt      # 패키지 설치 (Pillow·mysqlclient 포함)
docker compose up -d                 # MySQL 띄우기 (내리기: down)
python manage.py makemigrations      # 모델 변경 기록
python manage.py migrate             # DB에 반영
python manage.py runserver           # 서버 (포트: runserver 8080)
python manage.py createsuperuser     # 관리자 계정 → /admin
docker compose up -d                 # (MySQL) 띄우기 / down 내리기
```

# 부록 B. 자주 나는 에러

| 증상 | 해결 |
|---|---|
| `ModuleNotFoundError: django` | 가상환경 안 켬 → `source venv/bin/activate` (윈도우 `venv\Scripts\activate`) 후 설치 |
| `Cannot use ImageField because Pillow is not installed` | `pip install Pillow` (requirements에 포함) |
| `Error loading MySQLdb module` | `pip install -r requirements.txt` (mysqlclient 포함). 맥 빌드 실패 시 `brew install mysql-client pkg-config` · 윈도우는 보통 바로 설치(실패 시 MS C++ Build Tools 설치) |
| MySQL 도커인데 `Access denied for user 'root'` | 로컬 MySQL이 3306 점유 → 맥 `brew services stop mysql` · 윈도우 `net stop MySQL80`(관리자) 또는 services.msc에서 중지 |
| `Can't connect to MySQL (2003)` | 도커 안 뜸 → `docker compose up -d` |
| 사진이 안 보임 | 응답 `poster` 가 전체 URL인지, `DEBUG=True` 에서 media 서빙 중인지 확인 |
| 맞는 주소인데 404 | **URL 끝 슬래시** (`/movies/1/`❌ → `/movies/1`✅) |
| 모델 바꿨는데 반영 안 됨 | `makemigrations` → `migrate` 다시 |
