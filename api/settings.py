import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h#v#*68y)bfb2ylvy^f-tksars9-k1#8lejxo==_3hsnu2ek!h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# CSRF_TRUSTED_ORIGINS = ['https://*.smarthydro.cl','https://*.127.0.0.1']
ALLOWED_HOSTS = ['*']

# Security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'


# Application definition
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters'
]

LOCAL_APPS = [
    'api.crm.apps.CrmAppConfig',
    'django_crontab'
]

CRONJOBS = [
    # monitoreo smart hydro
    ('0 * * * *', 'api.crm.cron.main',  '>> ' + os.path.join(BASE_DIR,'api/log/debug7.log' + ' 2>&1 ')),
    # dga antiguo
    #('10 * * * *', 'api.crm.cronjobs_dga.cron_dga_old.main',  '>> ' + os.path.join(BASE_DIR,'api/log/debug_crondgaold.log' + ' 2>&1 ')),
    # estandar mayor
    #('10 * * * *', 'api.crm.cronjobs_dga.cron_dga.main',  '>> ' + os.path.join(BASE_DIR,'api/log/debug_crondga.log' + ' 2>&1 ')),
    # estandar medio
    #('20 12 * * *', 'api.crm.cronjobs_dga.cron_dga_medio.main',  '>> ' + os.path.join(BASE_DIR,'api/log/debug_crondgamedio.log' + ' 2>&1 ')),
    # estandar menor
    #('30 13 1 * *', 'api.crm.cronjobs_dga.cron_dgamenor.main',  '>> ' + os.path.join(BASE_DIR,'api/log/debug_crondgamedio.log' + ' 2>&1 ')),
    # estandar caudales muy pequenos
    #('40 14 * 12 *', 'api.crm.cronjobs_dga.cron_dgamuypequenos.main',  '>> ' + os.path.join(BASE_DIR,'api/log/debug_crondgamedio.log' + ' 2>&1 ')),
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:3001',
]

REST_FRAMEWORK = {
    'DEAFULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'drf_excel.renderers.XLSXRenderer'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.permissions.AllowAny',
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',

    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend'
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

ROOT_URLCONF = 'api.urls'

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

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
	'default': {
    	'ENGINE': 'django.db.backends.postgresql_psycopg2',
    	'NAME': 'postgres',
    	'USER': 'postgres',
    	'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432'        	
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
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Santiago'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
AUTH_USER_MODEL = 'crm.User'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
