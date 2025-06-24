import os, sys
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.gis',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'taggit',
    'django_extensions',
]

LOCAL_APPS = [
    'apps.core',
    'apps.blog',
    'apps.portfolio',
    'apps.services',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'fayvad_geosolutions.config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'fayvad_geosolutions.config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config('DB_NAME', default='fgl_website'),
        'USER': config('DB_USER', default='fayvad'),
        'PASSWORD': config('DB_PASSWORD', default='four@One2'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5433'),
    }
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Site ID
SITE_ID = 1

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Django Allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Email Configuration
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@geo.fayvad.com')

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Cache Configuration (Safe with fallback)
try:
    # Try Redis first
    import redis
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
except ImportError:
    # Fallback to dummy cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    
# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Security Settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CKEditor Configuration (Unified configuration)
CKEDITOR_UPLOAD_PATH = "blog/uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_RESTRICT_BY_USER = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': '100%',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
            ['Image', 'Table', 'HorizontalRule'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Smiley', 'SpecialChar'],
            ['Maximize'],
        ],
        'extraPlugins': ','.join([
            'uploadimage',
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
        'removePlugins': ','.join([
            'stylesheetparser',
        ]),
        'stylesSet': [
            {
                'name': 'Lead Paragraph',
                'element': 'p',
                'attributes': {'class': 'lead'}
            },
            {
                'name': 'Code Block',
                'element': 'pre',
                'attributes': {'class': 'code-block'}
            },
            {
                'name': 'Highlight',
                'element': 'span',
                'attributes': {'class': 'highlight'}
            },
        ],
        'format_tags': 'p;h2;h3;h4;h5;h6;pre;address;div',
    },
    'blog': {
        'toolbar': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', 'Blockquote'],
            ['Link', 'Unlink', 'Anchor'],
            ['Image', 'Table', 'HorizontalRule'],
            ['Styles', 'Format'],
            ['Source', 'Maximize'],
        ],
        'height': 500,
        'width': '100%',
        'stylesSet': [
            {
                'name': 'Article Lead',
                'element': 'p',
                'attributes': {'class': 'article-lead'}
            },
            {
                'name': 'Callout Box',
                'element': 'div',
                'attributes': {'class': 'callout-box'}
            },
            {
                'name': 'Code Snippet',
                'element': 'code',
                'attributes': {'class': 'code-snippet'}
            },
        ],
    }
}

# Blog-specific settings
BLOG_POSTS_PER_PAGE = 12
BLOG_COMMENTS_PER_PAGE = 20
BLOG_ENABLE_COMMENTS = True
BLOG_MODERATE_COMMENTS = True
BLOG_ENABLE_SUBSCRIPTIONS = True

# Company Information
COMPANY_INFO = {
    'name': 'Fayvad Geosolutions Ltd',
    'tagline': 'PhD-Level GIS Expertise',
    'phone': '+254 769 069 640',
    'email': 'info@geo.fayvad.com',
    'address': 'Grace House 3rd Floor Suite 10, Nkuruma Road, Thika, Kenya',
    'website': 'https://geo.fayvad.com',
    'social': {
        'linkedin': 'https://linkedin.com/company/fayvad-geosolutions',
        'twitter': 'https://twitter.com/fayvadgeo',
    }
}