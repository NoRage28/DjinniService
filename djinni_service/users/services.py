from rest_framework.request import Request
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from users.tokens import get_access_token
from users.models import NewUser
from django.urls import reverse
from typing import Dict, Any


class VerificationLetterSender:
    def send_verification_letter(self, request: Request, data: Dict[str, Any]):
        letter_data = self._get_letter_data(request=request, data=data)
        email = EmailMessage(
            subject=letter_data["subject"],
            body=letter_data["body"],
            to=[letter_data["to_email"]],
        )
        email.send()

    def _get_letter_data(self, request: Request, data: Dict[str, Any]) -> Dict[str, str]:
        user = NewUser.objects.get(email=data["email"])
        domain = get_current_site(request).domain
        token = get_access_token(user=user)
        activate_url_path = reverse("activate")
        activation_link = f"http://{domain}{activate_url_path}?token={token}"
        letter_body = f"Hi. \nUse link below to verify your email. \n{activation_link}"
        letter_subject = "Verify your email"
        letter_data = {
            "subject": letter_subject,
            "body": letter_body,
            "to_email": user.email,
        }

        return letter_data
