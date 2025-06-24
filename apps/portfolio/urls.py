from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Main portfolio pages
    path('featured/', views.featured_projects, name='featured'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('timeline/', views.project_timeline, name='timeline'),
    
    # Achievements
    path('achievements/', views.achievements_list, name='achievements'),
    
    # Filtering
    path('category/<slug:category_slug>/', views.projects_by_category, name='category'),
    path('tag/<slug:tag_slug>/', views.projects_by_tag, name='tag'),
    
    # Individual project detail
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    
    # API endpoints
    path('api/search/', views.project_search_api, name='search_api'),
    path('', views.projects_list, name='projects'),
]