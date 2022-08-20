import json
import logging
import os

from celery.schedules import crontab
from django.core.management.utils import get_random_secret_key

from core.helpers.apps import APPS
from core.helpers.middleware import DEFAULT_MIDDLEWARE
from core.helpers.rest_framework import DEFAULT_REST_FRAMEWORK_SETTINGS
from core.helpers.templates import DEFAULT_TEMPLATES
from core.helpers.validators import DEFAULT_AUTH_PASSWORD_VALIDATORS


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def parse_json_config(content):
    configs = json.load(content)
    for key, value in configs.items():
        os.environ[key] = str(value)
    return True


def loading_file(filename):
    try:
        with open(os.path.join(BASE_DIR, "config", filename)) as json_file:
            return parse_json_config(json_file)
    except FileNotFoundError as err:
        logger.error("FileNotFoundError", exc_info=err)


if not loading_file("config.json"):
    if not loading_file("config.dev.json"):
        logger.error("Errors! loading config project")
else:
    logger.debug("File Config Loaded")

MASTER_BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = os.getenv("SECRET_KEY",  default=get_random_secret_key())
if not SECRET_KEY:
    SECRET_KEY = get_random_secret_key()

DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = ('*',)
CORS_ORIGIN_ALLOW_ALL = True
INSTALLED_APPS = APPS
MIDDLEWARE = DEFAULT_MIDDLEWARE
ROOT_URLCONF = 'core.urls'
TEMPLATES = DEFAULT_TEMPLATES
WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}
AUTH_PASSWORD_VALIDATORS = DEFAULT_AUTH_PASSWORD_VALIDATORS
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=%s'
                       % os.environ.get("DB_SCHEME", "public")
        },
        'NAME': os.environ.get("DB_NAME"),
        'USER': os.environ.get("DB_USER"),
        'PASSWORD': os.environ.get("DB_PASSWORD"),
        'HOST': os.environ.get("DB_HOST"),
        'PORT': os.environ.get("DB_PORT"),
    },
}

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = os.environ.get("TIME_ZONE")

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

REST_FRAMEWORK = DEFAULT_REST_FRAMEWORK_SETTINGS
AUTH_USER_MODEL = "user.User"
CSRF_TRUSTED_ORIGINS = ['https://backend.sulaksi.kz']

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"

CELERY_BEAT_SCHEDULE = {
    "send_order_to_robot": {
        "task": "order.tasks.send_order_to_robot",
        "schedule": crontab(minute="*/1"),
    },
    "auto_deliver_orders": {
        "task": "order.tasks.auto_deliver_orders",
        "schedule": crontab(minute="*/1"),
    },
}
