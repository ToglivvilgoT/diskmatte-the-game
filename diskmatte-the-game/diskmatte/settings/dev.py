"""Settings for local development.

Activated by default (see manage.py / wsgi.py / asgi.py). Not suitable for
production use: DEBUG is on and the secret key has an insecure fallback.
"""

import os

from .base import *  # noqa: F401,F403

# SECURITY WARNING: keep the secret key used in production secret!
# Falls back to a fixed, insecure value so development works without extra setup.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-dev-key-not-for-production")

DEBUG = True

ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]
