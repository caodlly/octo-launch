from django.urls import path
from django.conf import settings
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
    path(
        "user/email/code/send",
        views.SendEmailCodeVerify.as_view(),
        name="send_email_verify",
    ),
    path("user/email/code/", views.EmailCodeVerify.as_view(), name="email_code_verify"),
    # =======
    path(
        "user/reset_password/code/send/",
        views.SendCodeRestPassword.as_view(),
        name="send_code_reset_password",
    ),
    path(
        "user/reset_password/code/",
        views.VerifyCodeResetPassowrd.as_view(),
        name="verify_code_reset_password",
    ),
    path(
        "user/reset_password/",
        views.ResetPassowrd.as_view(),
        name="reset_password",
    ),
]

if settings.ENABLE_SOCIAL_LOGIN:
    urlpatterns += [
        path(
            "auth/social/<str:provider>/",
            views.OAuthLoginView.as_view(),
            name="oauth_login",
        ),
    ]
