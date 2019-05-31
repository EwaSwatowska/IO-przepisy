# Django settings for IO project
from __future__ import unicode_literals

import configparser
import io
import os
from os.path import join

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_env_variable(var_name, default=False):
    """
    Get the environment variable or return exception
    :param default: 
    :param var_name: Environment Variable to lookup
    adapted rh0dium code https://stackoverflow.com/a/21619127/9929776
    (python 2.* -> python 3.*; taken care of special characters errors)
    """
    try:
        return os.environ[var_name]
    except KeyError:
        env_file = os.environ.get('PROJECT_ENV_FILE', os.path.join(BASE_DIR, "static") + "/.env")
        try:
            config = io.StringIO()
            config.write("[DATA]\n")
            config.write(open(env_file).read())
            config.seek(0, os.SEEK_SET)
            # without environment variable substitution; no need to escape special characters
            cp = configparser.RawConfigParser()
            cp.readfp(config)
            value = dict(cp.items('DATA'))[var_name.lower()]
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            os.environ.setdefault(var_name, value)
            return value
        except (KeyError, IOError):
            if default is not False:
                return default
            from django.core.exceptions import ImproperlyConfigured
            error_msg = "Either set the env variable '{var}' or place it in your " \
                        "{env_file} file as '{var} = VALUE'"
            raise ImproperlyConfigured(error_msg.format(var=var_name, env_file=env_file))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('SECRET_KEY')

# SECRET_KEY = os.getenv('SECRET_KEY', 'Not Set')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# allowing anonymous rating
STAR_RATINGS_ANONYMOUS = True

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 30
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',  # The admin site.
    'django.contrib.auth',  # An authentication system.
    'django.contrib.contenttypes',  # A framework for content types.
    'django.contrib.sessions',  # A session framework.
    'django.contrib.messages',  # A messaging framework.
    'django.contrib.staticfiles',  # A framework for managing static files.
    'search4recipes',
    'autoslug',
    'rest_framework',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'io_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'io_site.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'CookBook',
        'USER': 'postgres',
        # 'PASSWORD': get_env_variable('PASSWORD'),
        'PASSWORD': 'io-przepisy',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/


LANGUAGE_CODE = 'pl'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = False

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


BASE_PATH = os.path.dirname(os.path.abspath(__file__))

CACHE_BACKEND = "file://" + os.path.join(BASE_PATH, 'cache')

MEDIA_ROOT = join(BASE_PATH, 'media')
MEDIA_URL = '/media/'

PHOTO_MEDIA_URL = 'photos/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

AUTH_PROFILE_MODULE = 'accounts.UserProfiles'

FS_IMAGE_UPLOADS = os.path.join(MEDIA_ROOT, 'photos/')
FS_IMAGE_URL = os.path.join(MEDIA_URL, 'photos/')
