"""
URL configuration for fayvad_geosolutions project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

# Import sitemaps
from apps.core.sitemaps import StaticViewSitemap
from apps.blog.sitemaps import BlogSitemap, BlogCategorySitemap

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'blog_categories': BlogCategorySitemap,
}

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Main apps
    path('services/', include('apps.services.urls')),
    path('portfolio/', include('apps.portfolio.urls')),
    path('blog/', include('apps.blog.urls')),  # Add this line
    path('ckeditor/', include('ckeditor_uploader.urls')),  # Add this for CKEditor uploads
    path('', include('apps.core.urls')),
    
    # SEO and utilities
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Add django_browser_reload URLs
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]

    # Add debug toolbar URLs in development
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
