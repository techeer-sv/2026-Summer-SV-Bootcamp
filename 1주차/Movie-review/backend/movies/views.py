"""
movies/views.py - 영화 게시판 로직 (미니멀 3기능 + 댓글).

기능을 셋으로 좁힌다:
- 게시판 목록 (GET /movies)        → MovieListSerializer  (이미지+제목만, 가볍게)
- 영화 카드 생성 (POST /movies)    → MovieSerializer       (입력 검증 = write용)
- 상세 조회 (GET /movies/{id})     → MovieDetailSerializer (제목·사진·글·댓글 전부)
+ 상세에 보여줄 댓글 작성 (POST /movies/{id}/comments)

@extend_schema : APIView는 Swagger가 입력/출력 형식을 자동으로 못 알아낸다.
  그래서 어떤 serializer를 받고/돌려주는지 직접 알려줘야 Swagger에 입력칸이 뜬다.
  (poster 같은 ImageField가 있으면 Swagger가 자동으로 '파일 업로드' 칸으로 그려줌)

포스터 업로드(multipart/form-data)는 DRF 기본 파서가 처리하므로 추가 설정 불필요.
"""
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import (
    CommentSerializer,
    MovieDetailSerializer,
    MovieListSerializer,
    MovieSerializer,
)


class MovieView(APIView):
    """GET /api/v1/movies  목록(이미지+제목)  ·  POST /api/v1/movies  카드 생성(+포스터)"""

    # 등록은 사진을 같이 받으니 multipart/form-data 하나로 고정.
    # → Swagger가 드롭다운 없이 '텍스트칸 + 파일 선택' 폼을 한 번에 보여준다.
    parser_classes = [MultiPartParser]

    @extend_schema(responses=MovieListSerializer(many=True))
    def get(self, request):
        movies = Movie.objects.all()  # Meta.ordering 으로 최신순
        serializer = MovieListSerializer(movies, many=True, context={"request": request})
        return Response(serializer.data)

    @extend_schema(request=MovieSerializer, responses=MovieSerializer)
    def post(self, request):
        # 지금은 인증이 없어 클라이언트가 user_id를 직접 보낸다.
        # (실무: serializer.save(user=request.user) + user_id read_only — 4. 확장 참고)
        if not request.data.get("user_id"):
            return Response({"message": "user_id는 필수입니다."}, status=400)

        serializer = MovieSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)  # 역직렬화 + 검증
        serializer.save()                          # 객체 생성 + 포스터 파일 저장
        return Response(serializer.data, status=201)


class MovieDetailView(APIView):
    """GET /api/v1/movies/<movie_id>  상세 — 제목·사진·글·댓글 전부"""

    @extend_schema(responses=MovieDetailSerializer)
    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        return Response(MovieDetailSerializer(movie, context={"request": request}).data)


class CommentCreateView(APIView):
    """POST /api/v1/movies/<movie_id>/comments  댓글 작성 (상세에 nested로 보임)"""

    @extend_schema(request=CommentSerializer, responses=CommentSerializer)
    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        if not request.data.get("user_id"):
            return Response({"message": "user_id는 필수입니다."}, status=400)

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(movie=movie)  # URL의 영화에 댓글을 연결
        return Response(serializer.data, status=201)
