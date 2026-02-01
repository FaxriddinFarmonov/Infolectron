from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class AuthService:

    @staticmethod
    def login(email: str, password: str) -> dict:
        user = authenticate(
            email=email,
            password=password
        )

        if not user:
            raise ValueError("Invalid credentials")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @staticmethod
    def logout(refresh_token: str):
        token = RefreshToken(refresh_token)
        token.blacklist()
