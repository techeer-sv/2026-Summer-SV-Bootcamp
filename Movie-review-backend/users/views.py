"""
users/views.py - 회원가입/로그인 메인 로직.

전사 흐름:
- 클래스형(APIView)으로 작성 (함수형보다 가독성이 좋다고 봄).
- 메서드 이름이 곧 HTTP 메서드. 회원가입/로그인 모두 POST.
  (로그인은 조회 같지만, URL로 정보를 노출하면 안 되므로 POST로 보낸다.)
- 응답은 우선 JsonResponse 로 (가장 기본적인 장고 응답). Response는 게시판에서 사용.
- DB 접근은 ORM(User.objects...)으로. SQL을 직접 안 짜도 쿼리가 나간다.

@extend_schema + inline_serializer : 이 뷰는 JsonResponse라 Swagger가 입력 형식을
  모른다. 그래서 email/password 입력칸이 뜨도록 요청 형식을 직접 알려준다(문서용).
"""
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.views import APIView

from .models import User

# Swagger 입력칸용 — 실제 검증이 아니라 '문서에 보일 형식' 정의.
AuthRequest = inline_serializer(
    name="AuthRequest",
    fields={
        "email": serializers.EmailField(),
        "password": serializers.CharField(),
    },
)


class SignupView(APIView):
    """회원가입 - POST /api/v1/users/signup"""

    @extend_schema(request=AuthRequest, responses={201: None})
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # 1) 기초 예외처리: 안 넣으면 400 (네가 잘못 보냈다 = 클라이언트 잘못)
        if not email or not password:
            return JsonResponse(
                {"message": "이메일과 비밀번호를 입력해주세요."}, status=400
            )

        # 2) 이미 가입된 이메일인지 ORM filter 로 확인 (중복 가입 방지)
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"message": "이미 가입된 이메일입니다."}, status=400
            )

        # 3) 생성. created_at / updated_at 은 자동으로 채워진다.
        user = User.objects.create(email=email, password=password)

        return JsonResponse(
            {"message": "회원가입 성공", "user_id": user.id, "user_email": user.email},
            status=201,
        )


class LoginView(APIView):
    """로그인 - POST /api/v1/users/login"""

    @extend_schema(request=AuthRequest, responses={200: None})
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return JsonResponse(
                {"message": "이메일과 비밀번호를 입력해주세요."}, status=400
            )

        # 이메일+비번이 맞는지 확인. 없으면 예외 → 사용자 잘못(401)
        try:
            user = User.objects.filter(email=email, password=password).get()
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "이메일 또는 비밀번호가 올바르지 않습니다."}, status=401
            )

        return JsonResponse(
            {"message": "로그인 성공", "user_id": user.id, "user_email": user.email},
            status=200,
        )
