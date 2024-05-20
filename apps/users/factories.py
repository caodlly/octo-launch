import factory
from .models import User
from faker import Faker
from django.contrib.auth.hashers import make_password

password = Faker().password()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = Faker().name()
    email = Faker().email()
    username = Faker().user_name()[0:10]
    password = make_password(password)
    email_verified = True


class AdminFactory(factory.Factory):
    class Meta:
        model = User

    name = Faker().name()
    email = Faker().email()
    username = Faker().user_name()[0:10]
    password = make_password(password)
    is_staff = True
    is_superuser = True
    email_verified = True
