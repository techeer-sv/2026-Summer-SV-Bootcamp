"""
========================================================================
 dev.py  —  로컬 개발용 설정 (내 PC에서 개발할 때)
========================================================================

[이 파일의 역할]
 base 의 공통 설정을 그대로 가져오고(`from .base import *`),
 '개발일 때만 다른 값'만 여기서 덮어쓴다.

[전사 흐름 — DB 접속이 환경마다 다른 이유]
 백엔드 서버를 어디서 돌리느냐에 따라 DB '주소(HOST)'가 달라진다.
   - 백엔드를 '로컬(내 PC)'에서 실행  → DB는 도커 MySQL, 주소는 127.0.0.1
   - 백엔드까지 '도커'로 실행        → DB 주소는 컨테이너 이름 mysqldb (그건 prod.py)
 dev 는 '로컬에서 개발'하는 경우라 HOST = 127.0.0.1 이다.
 (127.0.0.1 = localhost = 내 컴퓨터 자신)
"""
import os

from .base import *  # noqa  (base의 모든 공통 설정을 가져온다)

# [왜 True]
# 개발 중엔 에러가 나면 원인을 자세히 보여줘야 디버깅이 쉽다.
# (배포 prod 에서는 보안 때문에 False)
DEBUG = True

# [왜 *]
# 개발용이라 어떤 호스트로 접속하든 다 허용. 배포에서는 좁혀야 한다.
ALLOWED_HOSTS = ["*"]

# 도커로 띄운 MySQL에 로컬에서 접속한다.
# 값들은 환경변수로 덮어쓸 수 있고, 없으면 아래 기본값(도커 compose와 일치)을 쓴다.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "mydatabase"),      # 데이터베이스 이름
        "USER": os.getenv("DB_USER", "root"),            # 접속 계정
        "PASSWORD": os.getenv("DB_PASSWORD", "1234"),    # 비밀번호
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),       # ★로컬 실행이라 127.0.0.1
        "PORT": os.getenv("DB_PORT", "3306"),            # MySQL 기본 포트
    }
}
