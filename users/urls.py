from django.urls import path

from users.views import RegisterView, LoginView, ProfileView

urlpatterns=[
    path('register/', RegisterView.as_view()), # 회원가입 뷰 url
    path('login/', LoginView.as_view()), # 로그인 뷰 url
    path('profile/<int:pk>/', ProfileView.as_view()), # 프로필 뷰 url
]