from faker import Faker
from PIL import Image
import random
import uuid


def generate_data_category():
    faker = Faker()
    name = faker.user_name()[0:10]
    uuid_str = str(uuid.uuid4())[:3]
    return {'name': name + '_' + uuid_str}


def generate_data_login(seed=None):
    fake = Faker()

    if isinstance(seed, int):
        Faker.seed(seed)

    return {'email': fake.email(), 'password': fake.password(20)}


def generate_data_register(seed=None):
    fake = Faker()

    if isinstance(seed, int):
        Faker.seed(seed)

    password = fake.password(20)

    return {
        'first_name': generate_data_category().get('name'),
        'last_name': generate_data_category().get('name'),
        'username': fake.user_name()[0:10],
        'email': fake.email(),
        'password': password,
        'password2': password,
    }


def generate_fake_image(width=500, height=500, color=None):
    if color is None:
        color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))

    return Image.new("RGB", (width, height), color)
