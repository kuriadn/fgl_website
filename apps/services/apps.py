"""
App configuration for services application.
"""
from django.apps import AppConfig

class ServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.services'
    verbose_name = 'Services'
    
    def ready(self):
        # Import signals here if needed
        pass