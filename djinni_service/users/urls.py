from django.urls import path
from users.views import UserSignUpView, activate


urlpatterns = [
    path("sign_up/", UserSignUpView.as_view(), name="sign_up"),
    path("activate/", activate, name="activate"),
]
