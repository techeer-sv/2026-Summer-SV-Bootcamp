"""
movies/urls.py - 영화/댓글 URL (REST 원칙: 명사·복수형, 끝 슬래시 없음).

미니멀 구성: 목록 / 생성 / 상세 + 댓글 작성.
"""
from django.urls import path

from .views import CommentCreateView, MovieDetailView, MovieView

urlpatterns = [
    path("movies", MovieView.as_view()),                                  # GET(목록), POST(생성)
    path("movies/<int:movie_id>", MovieDetailView.as_view()),             # GET(상세)
    path("movies/<int:movie_id>/comments", CommentCreateView.as_view()),  # POST(댓글)
]
