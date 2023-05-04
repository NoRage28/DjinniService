from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import NewUser


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = NewUser
        fields = ("email", "password", "user_type")

    def create(self, validated_data):
        user = NewUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            user_type=validated_data["user_type"],
        )

        return user
