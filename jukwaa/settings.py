"""
Django settings for jukwaa project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path
from datetime import datetime, timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-!e5m9+1doxh(n_s^vo@ndal$@ua7ol&0(jrkg)u+*kc_h*wx0j"
API_KEY = "6e45a45800b3fd96346d789e128f020d-2cb61693-cffd-4c4e-8eab-caac0eac2f51"
BASE_URL = "https://2vjejl.api.infobip.com"

OTP_SECRET_KEY = "NzkyNDE0NDRiZDA3NmJmMDgwOGU0M2MzNzYzNzIyZDM3ZDk2YzBlZTMwNDkwMTkxYjYxYjllMWIxMWYwY2Q2Mw=="
OTP_API_KEY = "68c9d2854d3ffcbb"
MAINTENANCE_MODE = None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
PRODUCTION = False
# HOST_IP = "109.199.108.165"
HOST_IP = "172.23.176.1"
FRONT_END_ADD = "172.23.176.1"

# print empty
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True

# email configuration setup 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'sharifumajid3@gmail.com'
EMAIL_HOST_PASSWORD = 'kmdv lbzm upio nnik'

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "drf_yasg",
    "djoser",
    "phonenumbers",
    "django_otp",
    # "django_otp.plugins.otp_totp",
    "base",
    "backend",
    "blog",
    "rest_framework",
    "django_extensions",
    "rest_framework.authtoken",
    "easyaudit"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "easyaudit.middleware.easyaudit.EasyAuditMiddleware"
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Adjust port as necessary
]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

ROOT_URLCONF = "jukwaa.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "jukwaa.wsgi.application"
# AUTHENTICATION_BACKENDS = [
#     "staff.views.UserAuthentication"
# ]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if PRODUCTION == True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "jukwaa",
            "USER": "jukwaa",
            "PASSWORD": "jukwaa%100",
            "HOST": "db",
            "PORT": "5432",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "jukwaa",
            "USER": "jukwaa",
            "PASSWORD": "jukwaa%100",
            "HOST": HOST_IP,
            "PORT": "5432",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"


# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

if DEBUG:
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "..", "jukwaa/static").replace(
        "\\", "/"
    )
else:
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), "static").replace("\\", "/")


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
