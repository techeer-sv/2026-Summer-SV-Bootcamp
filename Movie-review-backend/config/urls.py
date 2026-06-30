"""
config/urls.py - 진입점(기본 URL).

요청은 여기로 먼저 들어와서 각 앱(users, movies)의 urls 로 연결된다.
api/v1 접두사는 붙여도 되고 안 붙여도 된다(버전 관리용).
Swagger(스키마 문서)도 여기서 연결한다.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    # 각 앱으로 위임 (진입점 → 앱 URL)
    path("api/v1/", include("users.urls")),
    path("api/v1/", include("movies.urls")),

    # Swagger
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("swagger", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
]

# 개발 중에는 장고가 업로드된 사진(포스터)을 직접 서빙해준다. (실무는 nginx/S3)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
