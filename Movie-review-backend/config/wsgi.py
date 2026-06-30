import os

from django.core.wsgi import get_wsgi_application

# 배포(WSGI)는 prod 설정으로 동작.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
application = get_wsgi_application()
