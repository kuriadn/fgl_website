"""
Sitemaps for blog application.
"""
from django.contrib.sitemaps import Sitemap
from .models import BlogPost, BlogCategory


class BlogSitemap(Sitemap):
    """Sitemap for blog posts."""
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return BlogPost.objects.filter(status='published')
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()


class BlogCategorySitemap(Sitemap):
    """Sitemap for blog categories."""
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return BlogCategory.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.created_at
    
    def location(self, obj):
        return obj.get_absolute_url()