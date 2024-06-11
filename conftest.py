import pytest
from rest_framework.test import APIClient, APIRequestFactory
from app.user.factories import UserFactory, AdminFactory
from pytest_factoryboy import register
from app.user.models import User

# === register =====================================
register(UserFactory)
register(AdminFactory)


# === fixture ======================================
@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def factory() -> APIRequestFactory:
    return APIRequestFactory()


@pytest.fixture
def user(db, user_factory) -> User:
    user_factory.build().save()
    _user = User.objects.get(email=user_factory.email)
    return _user


@pytest.fixture
def admin(db, admin_factory) -> User:
    admin_factory.build().save()
    _user = User.objects.get(email=admin_factory.email)
    return _user
