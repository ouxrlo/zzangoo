from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ProfileEditForm
from posts.serializers import UserSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver

User = get_user_model()


# 홈 페이지 뷰
class IndexView(APIView):
    def get(self, request):
        return Response(
            {"message": "Welcome to the Home page!"}, status=status.HTTP_200_OK
        )


# 회원가입 뷰
class SignupView(APIView):
    def post(self, request):
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 로그인 후 세션에 사용자 저장
            return Response(
                {
                    "message": "User created and logged in",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        form = CustomUserCreationForm()
        return Response({"form": form.as_p}, status=status.HTTP_200_OK)


# 로그인 뷰
class LoginView(APIView):
    def post(self, request):
        form = AuthenticationForm(request, data=request.data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return Response(
                {
                    "message": "Logged in successfully",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


# 사용자 프로필 뷰 (로그인한 사용자만 접근 가능)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


# 프로필 수정 뷰 (로그인한 사용자만 접근 가능)
class ProfileEditView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        form = ProfileEditForm(request.data, instance=user)
        if form.is_valid():
            form.save()
            return Response(
                {
                    "message": "Profile updated successfully",
                    "user": UserSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그아웃 뷰
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )


# 로그아웃 후 처리
@receiver(user_logged_out)
def handle_user_logged_out(sender, request, user, **kwargs):
    return Response(
        {"message": "User logged out successfully"}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
