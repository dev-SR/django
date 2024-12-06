from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework import serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        User = get_user_model()
        username_field = User.USERNAME_FIELD
        user = User.objects.filter(email=attrs[username_field]).first()
        # print(user)
        if not user:
            raise AuthenticationFailed(
                {"error": "Email or password is incorrect."},  # message}
                "no_active_account",  # code used by djoser
            )
        if not user.is_active:
            raise AuthenticationFailed(
                "Please activate your account first",
                "no_active_account",
            )
        data = super().validate(attrs)
        # user: UserAccount = self.user
        # data["user"] = {
        #     "id": str(user.id),
        #     "email": user.email,
        #     "role": "superuser"
        #     if user.is_superuser
        #     else "staff"
        #     if user.is_staff
        #     else "general",
        #     "is_activated": user.is_active,
        # }
        return data


class UserSerializer(DjoserUserSerializer):
    role = serializers.SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):  # <----vvi
        fields = ["id", "email", "first_name", "last_name", "role"]

    def get_role(self, obj):
        is_staff = obj.is_staff
        is_superuser = obj.is_superuser
        return "superuser" if is_superuser else "staff" if is_staff else "general"
