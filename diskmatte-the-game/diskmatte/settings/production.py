"""Settings for the deployed (production) environment.

Selected by setting DJANGO_SETTINGS_MODULE=diskmatte.settings.production,
which is done in docker-compose.yaml for containerized deployments.
"""

import os

from .base import *  # noqa: F401,F403

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS: list[str] = ["shinobu.lysator.liu.se", "diskmatte-the-game.lisam.nu"]

# Required in addition to ALLOWED_HOSTS for CSRF checks on cross-origin POSTs (e.g. HTTPS behind a proxy).
CSRF_TRUSTED_ORIGINS: list[str] = [
    "https://shinobu.lysator.liu.se",
    "https://diskmatte-the-game.lisam.nu",
]
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

#SECURE_SSL_REDIRECT = True
