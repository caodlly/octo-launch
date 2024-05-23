import pytest
from django.urls import reverse
from apps.users.models import User
from apps.users.factories import password
from rest_framework import status
from apps.accounts.models import VerificationCode
from apps.utils.generate import generate_code


# === fixture ======================================
@pytest.fixture
def user_not_verified(user) -> User:
    _user = User.objects.get(email=user.email)
    _user.email_verified = False
    _user.save()
    return _user


@pytest.fixture
def verification_code(user_not_verified) -> VerificationCode:
    obj_code = VerificationCode.objects.create(
        user_id=user_not_verified.id, code=generate_code()
    )
    obj_code.save()
    return obj_code


# === Tests =====================================
@pytest.mark.django_db
def test_send_email_200(client, user_not_verified):
    user = user_not_verified
    assert user.email_verified is False
    client.login(email=user.email, password=password)
    response = client.post(reverse("send_email_verify"))
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] is True


@pytest.mark.django_db
def test_send_email_403(client, user):
    client.login(email=user.email, password=password)
    response = client.post(reverse("send_email_verify"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_verify_code_200(client, verification_code):
    user = verification_code.user
    assert user.email_verified is False
    client.login(email=user.email, password=password)

    code = verification_code.code
    response = client.post(reverse("email_code_verify"), {"code": code})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    _user = User.objects.get(email=user.email)
    assert _user.email_verified is True
