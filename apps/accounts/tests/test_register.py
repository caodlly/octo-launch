import pytest
from django.urls import reverse
from apps.utils.generate import generate_register
from rest_framework import status


@pytest.mark.django_db
def test_register_200(client):
    data_register = generate_register()
    response = client.post(reverse("register"), data_register)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == data_register["name"]
    assert response.data["email"]["value"] == data_register["email"]
    assert response.data["username"] == data_register["username"]


@pytest.mark.django_db
def test_register_400(client):
    data_register = generate_register()
    data_register["email"] = "foo"
    data_register["username"] = "test*()"
    response = client.post(reverse("register"), data_register)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"][0].code == "invalid"
    assert response.data["username"][0].code == "invalid"
