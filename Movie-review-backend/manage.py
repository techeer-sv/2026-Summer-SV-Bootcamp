#!/usr/bin/env python
"""Django 관리 명령 진입점.

기본 설정은 dev. 즉 로컬 개발 환경으로 동작한다.
( config/settings/{base,dev,prod}.py 로 환경을 쪼개 둔 구조 )
"""
import os
import sys


def main():
    # 환경마다 통합 사용이 불편해서 settings를 base/dev/prod로 분리했다.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django를 import 할 수 없습니다. 가상환경을 켜고 "
            "pip install -r requirements.txt 를 했는지 확인하세요."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
