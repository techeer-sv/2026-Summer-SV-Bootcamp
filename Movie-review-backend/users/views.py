"""
users/views.py - 회원가입/로그인.

- 클래스형(APIView). 메서드명이 곧 HTTP 메서드 (둘 다 POST).
- 응답은 Response(dict) → DRF가 자동으로 JSON으로 내려준다. (JsonResponse 안 써도 됨)
- DB 접근은 ORM(User.objects...).
- @extend_schema + inline_serializer : Swagger에 email/password 입력칸이 뜨도록 형식 명시.
"""
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User

# Swagger 입력칸용 — 문서에 보일 요청 형식.
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

        if not email or not password:
            return Response({"message": "이메일과 비밀번호를 입력해주세요."}, status=400)

        if User.objects.filter(email=email).exists():       # 중복 확인 (ORM)
            return Response({"message": "이미 가입된 이메일입니다."}, status=400)

        user = User.objects.create(email=email, password=password)
        return Response(
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
            return Response({"message": "이메일과 비밀번호를 입력해주세요."}, status=400)

        try:
            user = User.objects.filter(email=email, password=password).get()
        except User.DoesNotExist:
            return Response({"message": "이메일 또는 비밀번호가 올바르지 않습니다."}, status=401)

        return Response(
            {"message": "로그인 성공", "user_id": user.id, "user_email": user.email},
            status=200,
        )
