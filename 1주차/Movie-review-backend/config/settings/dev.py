"""
dev.py — 로컬 개발용 설정.

base 공통 설정을 가져오고(`from .base import *`), '개발일 때만 다른 값'만 덮어쓴다.
DB는 설치가 필요 없는 SQLite 파일(db.sqlite3) 하나를 쓴다 → 도커·MySQL 없이 바로 실행.
(배포용 실제 DB 설정은 prod.py 에서 .env 로 지정)
"""
from .base import *  # noqa  (base의 모든 공통 설정을 가져온다)

# 개발 중엔 에러를 자세히 보여줘야 디버깅이 쉽다. (배포 prod 에서는 보안 때문에 False)
DEBUG = True
ALLOWED_HOSTS = ["*"]

# SQLite: 별도 DB 서버나 도커 없이, 프로젝트 폴더의 db.sqlite3 파일을 그대로 쓴다.
# migrate 하면 이 파일이 자동으로 만들어진다.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
