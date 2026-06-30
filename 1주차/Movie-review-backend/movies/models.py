"""
movies/models.py - 영화 리뷰 게시판 모델.

게시판에 올라가는 한 건 = '영화'. 그래서 모델 이름이 Movie.
  Movie   = 영화 한 편 (제목 + 포스터 이미지 + 리뷰 내용)
  Comment = 그 영화 글에 달리는 댓글  ─< Movie (1:N)

전사 흐름: '모델부터' 짠다. ERD로 DB 스키마를 먼저 설계하고, 거기서 벗어나지
않게 클래스를 짠다. (로직 짜다 필요할 때 컬럼 추가 X)
"""
from django.db import models


class Movie(models.Model):
    # 작성자 — 전사처럼 간단히 정수 user_id로 (FK 대신).
    user_id = models.IntegerField()
    title = models.CharField(max_length=200)   # 영화 제목
    content = models.TextField()               # 리뷰 내용 (영화에 대한 글)
    # 영화 포스터 이미지. 실제 파일은 media/posters/ 에 저장되고 DB엔 경로만 들어간다.
    poster = models.ImageField(upload_to="posters/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "movies"         # 테이블 이름 (복수형)
        ordering = ["-created_at"]  # 조회 시 최신순

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_id = models.IntegerField()
    # 댓글은 외래키(FK)로 어떤 영화의 댓글인지 연결.
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.movie_id}번 영화의 댓글"
