# from faker import Faker
# from . import generate_data_category


# class DataUserFaker():
#     FIRST_NAME_TEST = generate_data_category().get("name")
#     LAST_NAME_TEST = generate_data_category().get("name")
#     USERNAME_TEST = Faker().user_name()[0:10]
#     EMAIL_TEST = Faker().email()
#     PASSWORD_TEST = Faker().password(12)


# def get_data_login(data):
#     email = data.get("email")
#     password = data.get("password")

#     return {"email": email, "password": password}


# def get_data_register():
#     return {
#         "first_name": FIRST_NAME_TEST,
#         "last_name": LAST_NAME_TEST,
#         "username": USERNAME_TEST,
#         "email": EMAIL_TEST,
#         "password": PASSWORD_TEST,
#         "password2": PASSWORD_TEST,
#     }


# def get_invalid_username():
#     return ["te", "test!@#$", "T@", "$#!@$#", "本に", "اختبار"]


# def remove_password2(value):
#     del value["password2"]
#     return value
