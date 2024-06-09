import pytest
from apps.users.factories import password  # noqa
from apps.accounts.models import VerificationCode
from apps.users.models import User
from django.urls import reverse
from rest_framework import status
from apps.accounts.tasks import remove_verification_code
from apps.utils.generate import generate_password
from django.contrib.auth.hashers import check_password


# === fixture ======================================
@pytest.fixture
@pytest.mark.django_db
def verification_code(user) -> VerificationCode:
    obj_code = VerificationCode.objects.create(user=user)
    obj_code.save()
    return obj_code


# === Tests =====================================
@pytest.mark.django_db
def test_send_reset_password_200(client, user, mocker):
    mocker.patch("apps.accounts.tasks.remove_verification_code.apply_async")
    data = {"email": user.email}
    response = client.post(reverse("send_code_reset_password"), data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    try:
        code_obj = VerificationCode.objects.get(user=user)
    except VerificationCode.DoesNotExist:
        assert False

    assert remove_verification_code(code_obj.id)


@pytest.mark.django_db
def test_send_reset_password_400(client):
    data = {"email": "testemail.com"}
    response = client.post(reverse("send_code_reset_password"), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"][0].code == "invalid"


@pytest.mark.django_db
def test_send_reset_password_404(client, mocker):
    data = {"email": "test@email.com"}
    mocker.patch("apps.accounts.tasks.remove_verification_code.apply_async")
    response = client.post(reverse("send_code_reset_password"), data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    with pytest.raises(VerificationCode.DoesNotExist):
        VerificationCode.objects.get(user__email=data["email"])


def test_verify_code_reset_passowrd_200(client, verification_code):
    data = {"code": verification_code.code, "email": verification_code.user.email}
    response = client.post(reverse("verify_code_reset_password"), data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["key"] == verification_code.key


def test_verify_code_reset_passowrd_400(client):
    response = client.post(reverse("verify_code_reset_password"))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"][0].code == "required"
    assert response.data["code"][0].code == "required"


def test_reset_password_200(client, verification_code):
    _password = generate_password(100)
    data = {
        "key": verification_code.key,
        "email": verification_code.user.email,
        "password": _password,
        "password2": _password,
    }
    response = client.post(reverse("reset_password"), data)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    try:
        user = User.objects.get(email=verification_code.user.email)
        assert check_password(_password, user.password)
    except User.DoesNotExist:
        assert False


def test_reset_password_400(client, verification_code):
    response = client.post(reverse("reset_password"))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"][0].code == "required"
    assert response.data["key"][0].code == "required"
    assert response.data["password"][0].code == "required"
    assert response.data["password2"][0].code == "required"


def test_reset_password_400_1(client, verification_code):
    data = {
        "email": verification_code.user.email,
        "key": verification_code.key,
        "password": generate_password(100),
        "password2": generate_password(100),
    }
    response = client.post(reverse("reset_password"), data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["password"][0].code == "invalid"
