"""
App configuration for blog application.
"""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.blog'
    verbose_name = 'Blog'
    
    def ready(self):
        # Import signals here if needed
        pass