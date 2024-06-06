from faker import Faker
from PIL import Image
from io import BytesIO
import uuid
import random
import secrets
import string
from django.core.files.uploadedfile import SimpleUploadedFile
import binascii
import os


def get_login(data: dict):
    return {
        "email": data.get("email"),
        "password": data.get("password"),
    }


def generate_register():
    fake = Faker()

    password = generate_password(100)
    return {
        "name": fake.name(),
        "username": fake.user_name()[:10],
        "email": fake.email(),
        "password": password,
        "password2": password,
    }


def generate_password(length=15):
    """I didn't use Faker to avoid password guessing"""
    alphabet = "#@$#@$#@$#@$#@$#@$" + string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(length))
    return password


def remove_email(email: str):
    return email.split("@")[0] + "_" + generate_code(4)


def generate_image(width=500, height=500, color=None):
    if color is None:
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

    name = uuid.uuid4().hex[:10] + ".png"
    image = Image.new("RGB", (width, height), color)

    byte_io = BytesIO()
    image.save(byte_io, format="PNG")
    byte_io.seek(0)

    return SimpleUploadedFile(name, byte_io.getvalue(), content_type="image/png")


def generate_code(length=6):
    characters = string.ascii_lowercase + string.digits
    code = "".join(secrets.choice(characters) for _ in range(length))
    return code


def generate_key():
    return binascii.hexlify(os.urandom(20)).decode()
