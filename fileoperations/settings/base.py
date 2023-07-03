import os
import json
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

try:
    from fileoperations.settings.select import SETTINGS_NAME as SN
except ImportError as e:
    err = ("There was error in importing fileoperations/settings/select.py module. "
           "If it does not exist create one, it should have one line: "
           "i.e. SETTINGS_NAME = 'local'  # or 'production' etc.")
    raise ImproperlyConfigured(err)

try:
    # from ataac part is required because of absolute_import
    local_settings = getattr(__import__(
        'fileoperations.settings', fromlist=[SN, ]), SN)
except ImportError as e:
    err = ("There was error '%s' in importing fileoperations.settings.%s module. "
           "Please check if module exists or modify fileoperations/settings/select.py. "
           "SETTINGS_NAME should be name of existing settings file." % (e, SN))
    raise ImproperlyConfigured(err)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

with open(os.path.join(PROJECT_DIR, "settings", "secrets.json")) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        err = "Set the %s in fileoperations/settings/secrets.json file." % setting
        raise ImproperlyConfigured(err)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getattr(local_settings, "DEBUG", True)

ALLOWED_HOSTS = getattr(local_settings, "ALLOWED_HOSTS", [])
CSRF_COOKIE_SECURE = getattr(local_settings, "CSRF_COOKIE_SECURE", True)
CSRF_TRUSTED_ORIGINS = getattr(local_settings, "CSRF_TRUSTED_ORIGINS", '')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'basic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fileoperations.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'fileoperations.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Project specific settings

# Absolute path to the main folder for this project
BASE_FILE_OPERATIONS_FOLDER = getattr(
    local_settings, "BASE_FILE_OPERATIONS_FOLDER", None)