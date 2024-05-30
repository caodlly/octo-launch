from .development import *  # noqa: F403


# === CELERY ======================================================
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
# === THROTTLING ======================================================
LOGIN_THROTTLING = 1000000
LOGIN_THROTTLING_IN = "hour"
RESETPASSWORD_THROTTLING = 1000000
RESETPASSWORD_THROTTLING_IN = "hour"
