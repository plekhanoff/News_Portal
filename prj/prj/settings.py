from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-coa=xz#s##)4j7stc+#njt-^y!_ozf9ja&8ne^c=^0%%@-a00e'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news.apps.NewsConfig',
    'news.signals',
    'django_filters',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django_apscheduler',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]


ROOT_URLCONF = 'prj.urls'

import os

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'news/templates/news'), ],
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

WSGI_APPLICATION = 'prj.wsgi.application'
SITE_ID = 1
SITE_URL = 'HTTP://127.0.0.1:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

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

TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = "/news/news_list"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "example@yandex.ru"
EMAIL_HOST_PASSWORD = "iliezvcovrxqizez"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = {}
DEFAULT_FROM_EMAIL = "example@yandex.ru"
SERVER_EMAIL = "example@yandex.ru"
APSCHEDULER_DATETIME_FORMAT = 'N j, y, f:s a'
APSCHEDULER_RUN_NOW_TIMEOUT = 25

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
    }
}


LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters': {
        'format_debug': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },

        'format_warning_mail': {
            'format': '{asctime} {levelname} {message} {pathname} ',
            'style': '{',
        },

        'format_general_security_info': {
            'format': '{asctime} {levelname} {message} {module} ',
            'style': '{',
        },

        'format_error_critical': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info} ',
            'style': '{',
        },
    },

   'handlers': {
        'console_debug': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'format_debug',
        },

        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'format_warning_mail',
        },

        'console_gen_sec_info': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'formatter': 'format_general_security_info',
            'filename': 'general.log',
        },

        'console_error_critical': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'format_error_critical',
        },

        'errors_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'format_error_critical',
            'filename': 'errors.log',
        },

        'security_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'format_general_security_info',
            'filename': 'security.log',
        },

        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'format_warning_mail',
        },
    },

   'filters': {
        'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'},
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'},
    },

   'loggers': {
        'django': {
            'handlers': ['console_debug', 'console_warning', 'console_gen_sec_info', 'console_error_critical'],
            'level': 'DEBUG',
            'propagate': True,
        },

        'django.request': {
            'handlers': ['errors_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },

        'django.server': {
            'handlers': ['errors_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },

        'django.template': {
            'handlers': ['errors_file'],
            'level': 'INFO',
            'propagate': True,
        },

        'django.db.backends': {
            'handlers': ['errors_file'],
            'level': 'INFO',
            'propagate': True,
        },

        'django.security': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
