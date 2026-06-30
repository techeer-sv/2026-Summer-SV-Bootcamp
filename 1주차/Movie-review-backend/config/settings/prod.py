"""
========================================================================
 prod.py  —  배포(운영)용 설정. 전부 도커로 띄울 때.
========================================================================

[이 파일의 역할]
 base 공통을 가져오고, '배포일 때만 다른 값'만 덮어쓴다.
 핵심 차이는 두 가지: (1) 보안 강화, (2) 비밀값을 .env 로 숨김.

[전사 흐름 — 왜 HOST가 mysqldb 인가]
 배포에서는 백엔드 서버도 도커 컨테이너로 띄운다. 컨테이너끼리는 IP가 아니라
 '서비스(컨테이너) 이름'으로 서로를 찾는다. docker-compose 의 MySQL 서비스
 이름이 mysqldb 라서 DB_HOST = mysqldb.
 (dev 는 로컬 실행이라 127.0.0.1, prod 는 도커라 mysqldb — 여기가 갈리는 지점)

[왜 .env 인가]
 SECRET_KEY, DB 비밀번호 같은 민감한 값을 코드에 적어 깃에 올리면 유출된다.
 그래서 .env 파일에 적어두고 읽어 오며, .env 는 .gitignore 로 깃에서 제외한다.
 (.env.example 만 공유해서 '무슨 값이 필요한지'만 알려준다)
"""
import os

from dotenv import load_dotenv

from .base import *  # noqa

# 프로젝트 루트의 .env 파일을 읽어 환경변수로 로드.
load_dotenv(BASE_DIR / ".env")

# [왜 False  ★중요]
# 운영에서 DEBUG=True 면 에러 화면에 코드/설정/쿼리가 그대로 노출된다(보안 사고).
# 그래서 반드시 False.
DEBUG = False

# [왜 .env에서]
# 운영 도메인만 허용해야 안전. 콤마로 여러 개 받는다. 예: "api.example.com,example.com"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# 비밀키도 운영에서는 .env 값으로 교체(없으면 base 기본값).
SECRET_KEY = os.getenv("SECRET_KEY", SECRET_KEY)

# 운영 DB. 값은 전부 .env 에서. HOST 기본값이 컨테이너 이름 mysqldb.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "mydatabase"),
        "USER": os.getenv("DB_USER", "root"),
        "PASSWORD": os.getenv("DB_PASSWORD", "1234"),
        "HOST": os.getenv("DB_HOST", "mysqldb"),   # ★도커 컨테이너 이름
        "PORT": os.getenv("DB_PORT", "3306"),
    }
}
