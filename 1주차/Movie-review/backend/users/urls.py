"""
users/urls.py - 회원 URL.

전사 흐름: REST 원칙은 '동사 말고 명사'지만, signup/login 은 둘 다 POST라
URL만으로 구분이 안 된다. 이럴 때는 예외적으로 동사를 쓴다.
(끝 슬래시는 APPEND_SLASH=False 라 붙이지 않는다.)
"""
from django.urls import path

from .views import LoginView, SignupView

urlpatterns = [
    path("users/signup", SignupView.as_view()),
    path("users/login", LoginView.as_view()),
]
