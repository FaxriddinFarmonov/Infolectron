from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from app.users.serializers import RegisterSerializer, LoginSerializer
from app.users.services import AuthService


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):

    @method_decorator(ratelimit(key="ip", rate="5/m", block=True))
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = AuthService.login(
            username=serializer.validated_data["username "
                                               ""],
            password=serializer.validated_data["password"],
        )

        return Response(tokens, status=status.HTTP_200_OK)


class LogoutView(APIView):

    def post(self, request):
        refresh_token = request.data.get("refresh")
        AuthService.logout(refresh_token)

        return Response(
            {"detail": "Logged out successfully"},
            status=status.HTTP_200_OK
        )
