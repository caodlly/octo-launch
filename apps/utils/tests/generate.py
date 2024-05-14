from faker import Faker
from PIL import Image
import uuid
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
            "name": self.fake.name(),
            "username": self.fake.user_name()[0:10],
            "email": self.fake.email(),
            "password": password,
            "password2": password,
        }

    @staticmethod
    def password():
        """I didn't use Faker to avoid password guessing"""
        alphabet = "#@$#@$#@$#@$#@$#@$" + string.ascii_letters + string.digits
        password = "".join(secrets.choice(alphabet) for i in range(25))
        return password

    @staticmethod
    def remove_email(email):
        return email.split("@")[0] + "_" + uuid.uuid4().hex[:4]

    @staticmethod
    def image(width=500, height=500, color=None):
        if color is None:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )

        return Image.new("RGB", (width, height), color)
