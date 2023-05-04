from django.shortcuts import render
from rest_framework import generics
from users.serializers import UserSignUpSerializer


class UserSignUpView(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer
