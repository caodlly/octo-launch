import pytest
from django.urls import reverse
from octo.utils.generate import generate_register
from rest_framework import status
from app.account.models import VerificationCode
from app.account.tasks import remove_verification_code


@pytest.mark.django_db
def test_register_200(client, mocker):
    data_register = generate_register()
    mocker.patch("app.account.tasks.remove_verification_code.apply_async")
    response = client.post(reverse("register"), data_register)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == data_register["name"]
    assert response.data["email"]["value"] == data_register["email"]
    assert response.data["username"] == data_register["username"]

    try:
        code_obj = VerificationCode.objects.get(user__email=data_register["email"])
    except VerificationCode.DoesNotExist:
        assert False

    assert remove_verification_code(code_obj.id)


@pytest.mark.django_db
def test_register_400(client):
    data_register = generate_register()
    data_register["email"] = "foo"
    data_register["username"] = "test*()"
    response = client.post(reverse("register"), data_register)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"][0].code == "invalid"
    assert response.data["username"][0].code == "invalid"
