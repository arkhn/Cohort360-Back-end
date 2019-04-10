"""
Django settings for cohort_back project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import ssl
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from ldap3 import Server, IP_V4_PREFERRED, ROUND_ROBIN, ServerPool, Tls, NTLM, RESTARTABLE, Connection, SUBTREE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_filters',

    'rest_framework',
    'rest_framework_swagger',

    'cohort.apps.CohortConfig',

    'explorations',
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

ROOT_URLCONF = 'cohort_back.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'cohort_back.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'cohort.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


COHORT_CONF = {
    "AUTH_METHODS": {
        "SIMPLE": {
        },
        "LDAP": {
            "USERNAME_REGEX": "user[2-9].*"
        }
    },
    "REFRESH_REQUESTS": {
        "MIN_DELAY_SEC": 60 * 60 * 2  # Every two hours
    }
}

SWAGGER_SETTINGS = {
    "LOGOUT_URL": "/accounts/logout",
}


# LDAP AD

QUAL_URLS = [
    "ldaps://{}.qual.domain.com".format(i)
    for i in range(1, 5)
]
QUAL_DOMAIN = "qual"

PROD_URLS = [
    "ldaps://{}.prod.domain.com".format(i)
    for i in range(1, 15)
]
PROD_DOMAIN = "prod"

DOMAIN = QUAL_DOMAIN if DEBUG else PROD_DOMAIN
prod = not DEBUG

LDAP_BASE_DN = "DC={},DC=domain,DC=com".format(DOMAIN)

tls = Tls(
    version=ssl.PROTOCOL_SSLv23,
    ca_certs_file='/path/to/ldap.crt',
)

servers = [
    Server(url, port=636, use_ssl=True, tls=tls, mode=IP_V4_PREFERRED)
    for url in (PROD_URLS if prod else QUAL_URLS)
]

LDAP_SERVER_POOL = ServerPool(servers, ROUND_ROBIN, active=True, exhaust=True)

LDAP_CONNECTION_PARAMETERS = {
    "server": LDAP_SERVER_POOL,
    "authentication": NTLM,
    "client_strategy": RESTARTABLE,
}

LDAP_CONNECTION = Connection(
    user=DOMAIN.upper() + '\\' + 'bind_account',
    password="bind_password",
    **LDAP_CONNECTION_PARAMETERS
)

if LDAP_CONNECTION.bind() is False:
    print("Bind operation failed: ", LDAP_CONNECTION.result)
    exit(1)

LDAP_SEARCH_FILTER = '(&(objectClass=inetOrgPerson)(sAMAccountName={}))'
LDAP_SEARCH_SCOPE = SUBTREE

LDAP_AUTH_USERNAME = DOMAIN.upper() + '\\' + '{}'

LDAP_DISPLAY_NAME_ATTR = "displayName"
LDAP_USERNAME_ATTR = "cn"
LDAP_FIRSTNAME_ATTR = "givenName"
LDAP_LASTNAME_ATTR = "sn"
LDAP_EMAIL_ATTR = "mail"
