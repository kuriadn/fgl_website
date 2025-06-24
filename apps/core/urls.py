"""
URL configuration for core app.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    
    # About page
    path('about/', views.AboutView.as_view(), name='about'),
    
    # Contact pages
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/success/', views.ContactSuccessView.as_view(), name='contact_success'),
    
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    
    # AJAX endpoints
    path('ajax/newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('ajax/search/', views.search_api, name='search_api'),
    
    # Generic pages (should be last to avoid conflicts)
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),

    # Homepage
    path('', views.HomeView.as_view(), name='home'),
]