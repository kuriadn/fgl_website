"""
Docker-specific settings that work for both development and production
"""
import os
from .base import *

# Database configuration for Docker
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'fgl_website'),
        'USER': os.getenv('DB_USER', 'fayvad'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'four@One2'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'disable',
        }
    }
}

# Remove problematic development apps in Docker
if 'debug_toolbar' in INSTALLED_APPS:
    INSTALLED_APPS.remove('debug_toolbar')
if 'django_browser_reload' in INSTALLED_APPS:
    INSTALLED_APPS.remove('django_browser_reload')

# Remove problematic middleware
MIDDLEWARE = [mw for mw in MIDDLEWARE if mw not in [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]]

# Static files configuration for Docker
STATIC_ROOT = '/app/staticfiles'
MEDIA_ROOT = '/app/media'

# Simple cache for Docker
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

print(f"🐳 Docker settings loaded - DEBUG: {DEBUG}")
