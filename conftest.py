import pytest
from rest_framework.test import APIClient, APIRequestFactory
from apps.users.factories import UserFactory, AdminFactory
from pytest_factoryboy import register

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
def user(db, user_factory):
    user_factory.build().save()
    return user_factory


@pytest.fixture
def admin(admin_factory):
    admin_factory.build().save()
    return admin_factory
