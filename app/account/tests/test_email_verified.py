import pytest
from django.urls import reverse
from app.user.models import User
from app.user.factories import password
from rest_framework import status
from app.account.models import VerificationCode
from app.account.tasks import remove_verification_code


# === fixture ======================================
@pytest.fixture
def user_not_verified(user) -> User:
    user.email_verified = False
    user.save()
    return user


@pytest.fixture
def verification_code(user_not_verified) -> VerificationCode:
    obj_code = VerificationCode.objects.create(user_id=user_not_verified.id)
    obj_code.save()
    return obj_code


# === Tests =====================================
@pytest.mark.django_db
def test_send_email_200(client, user_not_verified, mocker):
    mocker.patch("app.account.tasks.remove_verification_code.apply_async")
    user = user_not_verified
    assert not user.email_verified
    client.login(email=user.email, password=password)
    response = client.post(reverse("send_email_verify"))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    try:
        code_obj = VerificationCode.objects.get(user=user)
    except VerificationCode.DoesNotExist:
        assert False

    assert remove_verification_code(code_obj.id)


@pytest.mark.django_db
def test_send_email_403(client, user):
    client.login(email=user.email, password=password)
    response = client.post(reverse("send_email_verify"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_verify_code_200(client, verification_code):
    user = verification_code.user
    assert not user.email_verified
    client.login(email=user.email, password=password)

    code = verification_code.code
    response = client.post(reverse("email_code_verify"), {"code": code})
    assert response.status_code == status.HTTP_204_NO_CONTENT

    _user = User.objects.get(email=user.email)
    assert _user.email_verified
