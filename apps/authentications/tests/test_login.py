import pytest
from django.urls import reverse

# from apps.utils import Generate
from rest_framework import status
from apps.users.factories import password as get_password


@pytest.mark.django_db
def test_login_session_200(client, user, factory, lang_en, clear_cache):
    data_login = {
        "email": user.email,
        "password": get_password,
    }
    response = client.post(reverse("login_session"), data_login)
    assert response.status_code == status.HTTP_200_OK

    response = client.post(reverse("user_me"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("status") is True


@pytest.mark.django_db
def test_login_jwt_200(client, user, factory, lang_en, clear_cache):
    data_login = {
        "email": user.email,
        "password": get_password,
    }

    response = client.post(reverse("token_obtain_pair"), data_login)

    assert response.status_code == status.HTTP_200_OK

    access = response.data.get("access")
    refresh = response.data.get("refresh")

    assert isinstance(refresh, str) is True
    assert isinstance(access, str) is True

    response = client.post(
        reverse("user_me"), headers={"Authorization": f"bearer {access}"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("status") is True
