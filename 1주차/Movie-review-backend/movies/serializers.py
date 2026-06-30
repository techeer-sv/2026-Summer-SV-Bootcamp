"""
movies/serializers.py - 직렬화/역직렬화 담당.

화면 구성에 맞춰 시리얼라이저를 '목록용 / 상세용'으로 나눈다 ★
- 게시판 목록 → 이미지 + 제목만 보여주면 됨  → MovieListSerializer (가볍게)
- 글 클릭(상세) → 제목·사진·글·댓글 전부      → MovieDetailSerializer (무겁게, 댓글 nested)
- 등록/수정 입력 → MovieSerializer

용어:
- 직렬화(serialize)    = 객체 → JSON
- 역직렬화(deserialize) = JSON → 객체 (장고가 알아서)
- read_only_fields     = 입력으로는 안 받고 읽기 전용 (id는 ORM이 생성)
- poster(ImageField)   = 응답 시 전체 URL로 나간다 (뷰에서 request context 전달 시)
"""
from rest_framework import serializers

from .models import Comment, Movie


class MovieListSerializer(serializers.ModelSerializer):
    """게시판 목록용 — 이미지 + 제목만 (가볍게)."""

    class Meta:
        model = Movie
        fields = ["id", "title", "poster"]


class MovieSerializer(serializers.ModelSerializer):
    """등록/수정 입력용."""

    class Meta:
        model = Movie
        fields = ["id", "user_id", "title", "content", "poster", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class CommentSerializer(serializers.ModelSerializer):
    """댓글 생성/조회용. movie 는 URL에서 정해지므로 read_only."""

    class Meta:
        model = Comment
        fields = ["id", "user_id", "movie", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "movie", "created_at", "updated_at"]


class MovieDetailSerializer(serializers.ModelSerializer):
    """상세용 — 제목·사진·글 + 댓글(자식)까지 함께 (1:N nested)."""

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id", "user_id", "title", "content", "poster",
            "comments", "created_at", "updated_at",
        ]
