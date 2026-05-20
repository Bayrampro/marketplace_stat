"""ASGI config for marketplace_stat project."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "marketplace_stat.settings")

application = get_asgi_application()
