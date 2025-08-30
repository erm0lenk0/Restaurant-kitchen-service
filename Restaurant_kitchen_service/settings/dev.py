from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = env("DEBUG")
# DEBUG = os.environ.get("DJANGO_DEBUG", "") != "False"

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False