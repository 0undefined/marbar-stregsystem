import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-oj8bf8u330!3j@5f0vn(k(9v&(3z00*)*u2plj7&hds-syv*ue'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('VIRTUAL_ENV', None) is not None or os.getenv('DEBUG', "false").lower() == "true"

ALLOWED_HOSTS = [] if DEBUG else ['*']


# Application definition

INSTALLED_APPS = [
    # Django built-ins
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Extra packages
    'bootstrapform', # Nice forms and other styling stuffs
    'channels', # For async websocket IO

    # Custom apps
    'cms.apps.CmsConfig',
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

ROOT_URLCONF = 'stregsystem.urls'

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

WSGI_APPLICATION = 'stregsystem.wsgi.application'
ASGI_APPLICATION = 'stregsystem.asgi.application'

REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            # We use `redis` here since using ip's in containers is a no-no
            'hosts': [(REDIS_HOST, REDIS_PORT)],
        }
    }
}


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {}

if os.getenv('DB_TYPE', None) is None:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.' + os.getenv('DB_TYPE', 'sqlite3'),
        'NAME': 'stregsystem',
        'USER': os.getenv('DB_USER', 'marbar'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Copenhagen'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_global'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_CONSUMERS = [
    '1A', '2A', '3A', '4A', '5A', '6A', '7A',
    '1B', '2B', '3B', '4B', '5B', '6B', '7B',
    '1C', '2C', '3C', '4C', '5C', '6C', '7C',
    '1D', '2D', '3D', '4D', '5D', '6D', '7D',
    'Aspiranter', 'Crew', 'Marbarudvalget',
]
