"""
Sitemaps for core application.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.8
    changefreq = 'monthly'
    
    def items(self):
        return ['core:home', 'core:about', 'core:contact']
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        # You can customize this based on when each page was last updated
        return None