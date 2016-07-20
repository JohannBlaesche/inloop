"""
INLOOP base settings module

NOTE: This is not intended to be used directly. INLOOP ships with two default
settings modules (development.py and production.py) for different environments,
which both build upon this module and provide sane defaults which should work
out of the box.
"""
import sys
from os import environ
from os.path import dirname, join

if sys.version_info[0] < 3:
    raise RuntimeError("INLOOP must be run with Python 3.x")

if sys.getfilesystemencoding().lower() != "utf-8":
    raise RuntimeError("Invalid (non UTF-8) locale settings detected.")

PROJECT_ROOT = dirname(dirname(dirname(__file__)))
INLOOP_ROOT = join(PROJECT_ROOT, 'inloop')

AUTH_USER_MODEL = 'accounts.UserProfile'

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django_extensions',
    'huey.contrib.djhuey',
    'inloop.core',
    'inloop.accounts',
    'inloop.tasks',
    'inloop.gh_import',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'
ROOT_URLCONF = 'inloop.urls'
WSGI_APPLICATION = 'inloop.wsgi.application'
FILE_UPLOAD_HANDLERS = ("django.core.files.uploadhandler.TemporaryFileUploadHandler", )

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True
FIRST_DAY_OF_WEEK = 1

# URL prefixes for static and media files
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(INLOOP_ROOT, 'templates'),
            # otherwise django.contrib.auth won't find the custom templates:
            join(INLOOP_ROOT, 'accounts', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# setup for the asynchronous task queue
HUEY = {
    'name': 'inloop-task-queue',
    'always_eager': False,
}

# checker setup
CHECKER = {
    "timeout": 120,
}

# Docker image to be used by the DockerSubProcessChecker
DOCKER_IMAGE = "inloop-java-checker"

# which sendfile() implementation should be used ("django" or "nginx")
SENDFILE_METHOD = "django"

# Use the environment var INLOOP_LOG_LEVEL to adjust INLOOP logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'inloop': {
            'handlers': ['console'],
            'level': environ.get('INLOOP_LOG_LEVEL', 'INFO'),
        },
    },
}

# TODO: investigate a better method to align Bootstrap alerts and contrib.messages
MESSAGE_TAGS = {10: "info", 40: "danger"}
