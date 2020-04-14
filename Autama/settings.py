"""
Django settings for Autama project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0jx6nply=59sv85ii0*r9abdg$sf+awn1vjwelfzc7pxfaek-3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['73.164.205.208']  ##
ALLOWED_HOSTS = ['34.221.163.101', '127.0.0.1']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Autama',
    'api',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders'
]


# Dev Only, need to configure for production
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'Autama.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [''],
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

WSGI_APPLICATION = 'Autama.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# TODO: Check path
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # <- absolute path to dir to collect static files for deployment
# '/var/www/example.com/static/'
# STATIC_URL = '/static/'  # <- has to end in a / if set to non-empty value
STATIC_ROOT = os.path.join(BASE_DIR, "Webapp/")  # idk if Webapp or static for these
STATIC_URL = '/Webapp/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'Images'),
]

# Media
MEDIA_URL = '/Images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'Images')

# TODO: Do we need this?
# URL REDIRECTS
# LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL = '/FindMatches/'
# LOGOUT_REDIRECT_URL = '/login/'

# Authentication
# AUTHENTICATION_BACKENDS = ('user_profile.views.CustomBackend',)

# User Model
AUTH_USER_MODEL = 'api.UserInfo'


# Rest Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',  # Remove to allow logout on rest framework GUI.
        'rest_framework.authentication.TokenAuthentication'
    ]
}

CORS_ORIGIN_ALLOW_ALL = True


