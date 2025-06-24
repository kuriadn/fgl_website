from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Main blog views
    path('', views.blog_list, name='list'),
    path('search/', views.search, name='search'),
    path('archive/', views.archive, name='archive'),
    
    # Category and tag views
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag'),
    
    # AJAX endpoints
    path('subscribe/', views.subscribe, name='subscribe'),
    path('track-reading/<slug:slug>/', views.track_reading_time, name='track_reading'),
    
    # Post detail - Keep this last to avoid conflicts
    path('<slug:slug>/', views.blog_detail, name='detail'),
]