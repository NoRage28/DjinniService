from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from django.conf import settings
from users.serializers import UserSignUpSerializer
from users.services import VerificationLetterSender
from users.models import NewUser
import jwt


@api_view(["GET"])
def activate(request: Request) -> Response:
    token = request.GET.get("token")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        user = NewUser.objects.get(id=payload.get("user_id"))
        user.is_active = True
        user.save()
        return Response({"email": "Successfully activated"}, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError:
        return Response(
            {"error": "Activation inspired"}, status=status.HTTP_400_BAD_REQUEST
        )
    except jwt.exceptions.DecodeError:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class UserSignUpView(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        VerificationLetterSender().send_verification_letter(
            request=request, data=serializer.data
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
