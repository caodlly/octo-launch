import pytest
from django.urls import reverse
from rest_framework import status
from apps.users.factories import password as get_password
from django.conf import settings


# === fixture ======================================
@pytest.fixture()
def login_provide():
    settings.LOGIN_THROTTLING = 100000


# === test ======================================
@pytest.mark.django_db
def test_login_session_200(client, user, login_provide):
    data_login = {
        "email": user.email,
        "password": get_password,
    }
    response = client.post(reverse("login_session"), data_login)
    assert response.status_code == status.HTTP_200_OK
    me_session_POST(client)


def me_session_POST(client):
    response = client.post(reverse("user_me"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] is True


@pytest.mark.django_db
def test_login_refresh_jwt_200_200(client, user, login_provide):
    data_login = {
        "email": user.email,
        "password": get_password,
    }

    response = client.post(reverse("token_obtain_pair"), data_login)

    assert response.status_code == status.HTTP_200_OK

    access = response.data["access"]
    refresh = response.data["refresh"]

    assert isinstance(refresh, str) is True
    assert isinstance(access, str) is True

    me_jwt_200(client, access)
    refresh_jwt_200(client, refresh)
    verify_jwt_200(client, refresh)


def me_jwt_200(client, access):
    response = client.post(
        reverse("user_me"), headers={"Authorization": f"bearer {access}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] is True


def refresh_jwt_200(client, refresh):
    response = client.post(
        reverse("token_refresh"),
        {
            "refresh": refresh,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data["access"], str) is True


def verify_jwt_200(client, token):
    response = client.post(reverse("token_verify"), {"token": token})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_login_jwt_en_401(client, user, lang_en, login_provide):
    data_login = {
        "email": user.email,
        "password": "foo",
    }

    response = client.post(reverse("token_obtain_pair"), data_login)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["detail"] == "Email or password is incorrect."


@pytest.mark.django_db
def test_login_jwt_ar_401(client, user, lang_ar, login_provide):
    data_login = {
        "email": user.email,
        "password": "foo",
    }

    response = client.post(reverse("token_obtain_pair"), data_login)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["detail"] == "البريد الالكتروني او كلمة المرور غير صحيحة"


@pytest.mark.django_db
def test_login_session_en_401(client, user, lang_en, login_provide):
    data_login = {
        "email": user.email,
        "password": "foo",
    }
    response = client.post(reverse("login_session"), data_login)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["detail"] == "Email or password is incorrect."


@pytest.mark.django_db
def test_login_session_ar_401(client, user, lang_ar, login_provide):
    data_login = {
        "email": user.email,
        "password": "foo",
    }
    response = client.post(reverse("login_session"), data_login)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["detail"] == "البريد الالكتروني او كلمة المرور غير صحيحة"
