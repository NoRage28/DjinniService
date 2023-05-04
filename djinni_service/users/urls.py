from django.urls import path
from users.views import UserSignUpView


urlpatterns = [
    path('sign_up/', UserSignUpView.as_view(), name='sign_up')
]