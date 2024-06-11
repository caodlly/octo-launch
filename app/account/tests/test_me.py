import pytest
from django.urls import reverse
from app.user.factories import password
from rest_framework import status
from app.account.serializers import UserSerializer


@pytest.mark.django_db
def test_me_get_200(client, user, factory):
    client.login(email=user.email, password=password)
    response = client.get(reverse("user_me"))

    serializer = UserSerializer(
        user, context={"request": factory.get(reverse("user_me"))}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == serializer.data["id"]
    assert response.data["username"] == serializer.data["username"]
    assert response.data["avatar"] == serializer.data["avatar"]
    assert response.data["name"] == serializer.data["name"]
    assert response.data["email"] == serializer.data["email"]


@pytest.mark.django_db
def test_me_get_403(client, factory):
    response = client.get(reverse("user_me"))
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_me_post_200(client, user, factory):
    client.login(email=user.email, password=password)
    response = client.post(reverse("user_me"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] is True


@pytest.mark.django_db
def test_me_post_200_1(client, user, factory):
    response = client.post(reverse("user_me"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] is False
