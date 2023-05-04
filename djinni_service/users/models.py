from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        email = self.normalize_email(email=email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **other_fields):
        user = self.create_user(email, password, **other_fields)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        user.save()

        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ("employer", "I'm hiring"),
        ("employee", "I'm looking for a job"),
    ]

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        return ""
