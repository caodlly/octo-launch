from django.urls import path
from . import views


urlpatterns = [
    # =======
    path("auth/session/", views.LoginSession.as_view(), name="login_session"),
    path("auth/register/", views.Register.as_view(), name="register"),
    # =======
    path("auth/jwt/token/", views.LoginJWT.as_view(), name="token_obtain_pair"),
    path("auth/jwt/token/refresh/", views.RefreshJWT.as_view(), name="token_refresh"),
    path("auth/jwt/token/verify/", views.VerifyJWT.as_view(), name="token_verify"),
    # =======
    path("user/me/", views.Me.as_view(), name="user_me"),
    path("user/update/", views.UpdateProfile.as_view(), name="user_update"),
    # =======
    # path(
    #     "user/email/verified/",
    #     views.SendCodeEmailVerified.as_view(),
    #     name="email_verified",
    # ),
    # path("user/email/code/", views.CodeEmailVerified.as_view(), name="email_code"),
]
