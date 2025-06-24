"""
App configuration for portfolio application.
"""
from django.apps import AppConfig

class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.portfolio'
    verbose_name = 'Portfolio'
    
    def ready(self):
        # Import signals here if needed
        pass