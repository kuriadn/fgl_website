"""
Development settings for Fayvad Geosolutions project.
"""

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'fgl_website',
        'USER': 'fayvad',
        'PASSWORD': 'four@One2',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}

# Add development apps
INSTALLED_APPS += [
    'debug_toolbar',
    'django_browser_reload',
]

# Add development middleware
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

# Internal IPs for debug toolbar
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache (use dummy cache for development)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Django Extensions
DJANGO_EXTENSIONS_GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

# Disable security features for development
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Media files served by Django in development
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files served by Django in development
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Logging for development
LOGGING['handlers']['console']['level'] = 'INFO'
LOGGING['loggers']['django']['level'] = 'INFO'

# Add apps-specific logging
LOGGING['loggers'].update({
    'apps': {
        'handlers': ['console'],
        'level': 'WARNING',
        'propagate': False,
    }
})