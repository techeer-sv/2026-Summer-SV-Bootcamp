"""
users/models.py - 회원 모델.

전사 흐름:
- 장고 기본 auth(User)는 처음엔 너무 복잡하고 테스트가 빡빡해진다.
  그래서 회원가입을 '아무 이메일/비번이나 넣으면 가입'되게 아주 간단히 만든다.
- created_at(auto_now_add): 생성 시점 자동 기록
  updated_at(auto_now):     수정 시점 자동 갱신
  → 값을 입력받지 않아도 자동 설정된다.
- Meta.db_table: 테이블 이름은 복수형 's'. 'user'는 기본 예약과 헷갈릴 수 있어 'users'.
"""
from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)  # 학습용 평문. 실무는 해시 필수.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
