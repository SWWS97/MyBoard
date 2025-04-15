from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from users.models import Profile
from users.serializers import RegisterSerializer, LoginSerializer, ProfileSerializer


# 회원가입 뷰
class RegisterView(CreateAPIView): # CreateAPIView(generics) 사용 구현
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# 로그인 뷰
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data # validate()의 리턴값인 Token을 받아옴.
        return Response({"token" : token.key}, status=status.HTTP_200_OK)

# 프로필 뷰
class ProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer