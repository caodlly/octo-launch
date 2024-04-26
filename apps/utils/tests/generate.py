from faker import Faker
from PIL import Image
import random
import secrets
import string


class Generate:
    fake = Faker()

    def __init__(self):
        self.data_register = self.register()
        self.data_login = self.login()

    def login(self):
        return {
            "email": self.data_register.get("email"),
            "password": self.data_register.get("password"),
        }

    def register(self):
        password = self.password()

        return {
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "username": self.fake.user_name()[0:10],
            "email": self.fake.email(),
            "password": password,
            "password2": password,
        }

    @staticmethod
    def password():
        alphabet = string.ascii_letters + string.digits
        password = "".join(secrets.choice(alphabet) for i in range(30))
        return password

    @staticmethod
    def image(width=500, height=500, color=None):
        if color is None:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

        return Image.new("RGB", (width, height), color)
