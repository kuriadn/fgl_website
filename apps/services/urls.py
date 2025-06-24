"""
URL configuration for services app.
"""
from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Main services pages
    path('capabilities/', views.service_capabilities, name='capabilities'),
    path('compare/', views.compare_services, name='compare'),
    
    # Specific service pages - matching footer and navigation references
    path('land-surveying/', views.service_detail, {'slug': 'land-surveying'}, name='land_surveying'),
    path('gis-development/', views.service_detail, {'slug': 'gis-development'}, name='gis_development'),
    path('drone-mapping/', views.service_detail, {'slug': 'drone-mapping'}, name='drone_mapping'),
    path('environmental/', views.service_detail, {'slug': 'environmental-intelligence'}, name='environmental'),
    path('government/', views.service_detail, {'slug': 'government-solutions'}, name='government'),
    
    # Form submissions
    path('inquiry/submit/', views.submit_inquiry, name='submit_inquiry'),
    
    # Case studies
    path('<slug:service_slug>/case-studies/<slug:slug>/', views.case_study_detail, name='case_study'),
    
    # Generic service detail (must be last to avoid conflicts)
    path('<slug:slug>/', views.service_detail, name='detail'),

    path('', views.services_list, name='list'),
]