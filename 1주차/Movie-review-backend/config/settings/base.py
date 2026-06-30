"""
========================================================================
 base.py  —  모든 환경(dev/prod)이 공통으로 쓰는 설정
========================================================================

[왜 settings를 쪼갰나]
 django-admin startproject 를 하면 settings.py 가 '한 파일'로 생긴다.
 그런데 로컬 개발(dev)과 배포(prod)는 값이 다르다. 예를 들어
   - DEBUG: 개발은 True, 배포는 False(보안)
   - DB 접속: 개발은 내 PC의 MySQL, 배포는 도커 컨테이너의 MySQL
   - 비밀키/비밀번호: 배포는 .env 로 숨김
 이걸 한 파일에서 if 문으로 분기하면 금방 지저분해지고 실수가 난다.
 그래서 settings/ 폴더로 만들고 세 개로 나눈다:
   - base.py : 환경과 무관하게 '항상 같은' 공통 설정      ← 지금 이 파일
   - dev.py  : 로컬 개발에서만 다른 값 (DEBUG, 로컬 DB)
   - prod.py : 배포(도커)에서만 다른 값 (.env, 운영 DB)
 dev/prod 는 맨 위에서 `from .base import *` 로 공통을 가져온 뒤,
 자기 환경에서 다른 부분만 덮어쓴다. → 중복 제거 + 실수 방지.
"""
from pathlib import Path

# [왜 parents[2] 인가]
# 이 파일 위치가 config/settings/base.py 라서, 두 단계 위(parents[2])가
# manage.py 가 있는 '프로젝트 루트'다. (settings.py 한 파일일 때는 parent.parent)
BASE_DIR = Path(__file__).resolve().parents[2]

# [왜 여기 그냥 적나]
# 학습용이라 코드에 박아 둔다. 실무/배포(prod)에서는 .env 로 빼서 깃에 안 올린다.
SECRET_KEY = "django-insecure-handson-only-change-in-prod"

# [왜 base에 두나] 어떤 앱을 쓸지는 환경이 달라도 동일 → 공통.
INSTALLED_APPS = [
    # 장고 기본 제공 앱
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 외부 라이브러리
    "rest_framework",     # DRF: API를 쉽게 만들게 해줌
    "drf_spectacular",    # Swagger(API 문서) 자동 생성
    # 우리가 만든 앱 — 비즈니스 도메인마다 나눈다.
    # (배달 서비스라면 orders, deliveries 처럼. 지금은 users, movies)
    "users",
    "movies",
]

# [왜 base에 두나] 요청이 거치는 공통 처리 단계 → 환경 무관.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"   # URL 진입점이 어디인지 (config/urls.py)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# 서버 실행 진입점. wsgi/asgi 는 기본적으로 prod 설정으로 동작하게 해뒀다.
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# [왜 비웠나] 학습용. 비밀번호 규칙(8자 이상 등)을 켜두면 회원가입 테스트가
# 빡빡해진다. 처음엔 아무 값이나 통과되게 비워 두고, 큰 틀부터 확인한다.
AUTH_PASSWORD_VALIDATORS = []

# [공통 지역/시간 설정] 환경 무관 → base.
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

# [이미지 업로드] 영화 포스터 같은 업로드 파일이 저장/제공되는 경로.
#   업로드된 사진은 media/posters/xxx.jpg 로 저장되고, /media/... 주소로 제공된다.
#   (실무는 nginx/S3가 서빙. 개발 중엔 장고가 직접 — config/urls.py 참고)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# [왜] PK(id) 기본 타입을 BigAutoField(큰 정수)로. 데이터 많아질 때 안전.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# [왜 False 인가  ★전사 포인트]
# 장고 기본값은 APPEND_SLASH=True 라서 URL 끝에 '/'가 강제로 붙는다.
#   예) /api/v1/movies  로 요청해도 /api/v1/movies/ 로 리다이렉트.
# 끝 슬래시가 붙는 게 싫어서 False 로 끈다. → URL은 끝 슬래시 없이 설계한다.
APPEND_SLASH = False

# DRF가 API 문서를 만들 때 drf-spectacular 스키마를 쓰도록 지정.
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Swagger 화면에 보일 제목/설명/버전.
SPECTACULAR_SETTINGS = {
    "TITLE": "게시판 API",
    "DESCRIPTION": "회원가입/로그인 + 영화 리뷰(Movie)/댓글(Comment) 실습용 API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # 요청/응답 스키마를 분리 → 업로드(poster) 필드가 Swagger에서 '파일 선택' 칸으로 뜸.
    "COMPONENT_SPLIT_REQUEST": True,
}
