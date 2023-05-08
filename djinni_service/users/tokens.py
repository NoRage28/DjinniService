from rest_framework_simplejwt.tokens import RefreshToken
from users.models import NewUser


def get_access_token(user: NewUser) -> RefreshToken.access_token:
    token = RefreshToken.for_user(user).access_token
    return token
