from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Project, ProjectCategory, ProjectTag, Achievement


def projects_list(request):
    """List all projects with filtering and pagination"""
    projects = Project.objects.filter(is_active=True).select_related('category')
    
    # Get filter parameters
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    status = request.GET.get('status')
    year = request.GET.get('year')
    search = request.GET.get('search')
    
    # Apply filters
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    
    if tag_slug:
        projects = projects.filter(tags__slug=tag_slug)
    
    if status:
        projects = projects.filter(status=status)
    
    if year:
        projects = projects.filter(start_date__year=year)
    
    if search:
        projects = projects.filter(
            Q(title__icontains=search) |
            Q(short_description__icontains=search) |
            Q(client_name__icontains=search) |
            Q(location__icontains=search)
        )
    
    # Get featured projects
    featured_projects = Project.objects.filter(
        is_featured=True,
        is_active=True
    )[:3]
    
    # Get filter options
    categories = ProjectCategory.objects.filter(
        is_active=True,
        projects__is_active=True
    ).annotate(project_count=Count('projects')).distinct()
    
    popular_tags = ProjectTag.objects.filter(
        is_active=True,
        projecttagging__project__is_active=True
    ).annotate(project_count=Count('projecttagging')).order_by('-project_count')[:10]
    
    # Get available years
    years = Project.objects.filter(
        is_active=True
    ).dates('start_date', 'year', order='DESC')
    
    # Pagination
    paginator = Paginator(projects, 12)  # Show 12 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'projects': page_obj.object_list,
        'featured_projects': featured_projects,
        'categories': categories,
        'popular_tags': popular_tags,
        'years': years,
        
        # Current filters
        'current_category': category_slug,
        'current_tag': tag_slug,
        'current_status': status,
        'current_year': year,
        'current_search': search,
        
        # Pagination info
        'total_projects': paginator.count,
        
        # Page meta
        'page_title': 'Our Projects & Case Studies',
        'meta_description': 'Explore Fayvad Geosolutions project portfolio including Kenya Railways SGR, KETRACO infrastructure, and international research collaborations.',
    }
    
    return render(request, 'projects_list.html', context)


def project_detail(request, slug):
    """Detailed view of a specific project"""
    project = get_object_or_404(
        Project.objects.select_related('category').prefetch_related(
            'images', 'milestones', 'testimonials', 'achievements', 'tags'
        ),
        slug=slug,
        is_active=True
    )
    
    # Get related projects
    related_projects = Project.objects.filter(
        category=project.category,
        is_active=True
    ).exclude(id=project.id)[:3]
    
    # Get project images
    project_images = project.images.filter().order_by('order')
    
    # Get project milestones
    milestones = project.milestones.all().order_by('date_achieved')
    
    # Get testimonials
    testimonials = project.testimonials.filter(is_active=True)
    
    # Get project updates (for ongoing projects)
    updates = project.updates.filter(is_public=True).order_by('-update_date')[:5]
    
    context = {
        'project': project,
        'related_projects': related_projects,
        'project_images': project_images,
        'milestones': milestones,
        'testimonials': testimonials,
        'updates': updates,
        'page_title': project.meta_title or f"{project.title} - Case Study",
        'meta_description': project.meta_description or project.short_description,
    }
    
    return render(request, 'project_detail.html', context)


def featured_projects(request):
    """Featured projects showcase"""
    featured = Project.objects.filter(
        is_featured=True,
        is_active=True
    ).select_related('category')[:6]
    
    # Get statistics
    stats = {
        'total_projects': Project.objects.filter(is_active=True).count(),
        'completed_projects': Project.objects.filter(is_active=True, status='completed').count(),
        'ongoing_projects': Project.objects.filter(is_active=True, status='in_progress').count(),
        'total_value': 'KES 2.5B+',  # Could be calculated from actual project values
        'countries_served': 3,  # Kenya, Germany, Japan based on experience
    }
    
    context = {
        'featured_projects': featured,
        'stats': stats,
        'page_title': 'Featured Projects',
        'meta_description': 'Showcase of Fayvad Geosolutions most significant projects including national infrastructure, international research, and innovative geospatial solutions.',
    }
    
    return render(request, 'featured_projects.html', context)


def projects_by_category(request, category_slug):
    """Projects filtered by category"""
    category = get_object_or_404(ProjectCategory, slug=category_slug, is_active=True)
    
    projects = Project.objects.filter(
        category=category,
        is_active=True
    ).select_related('category')
    
    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'projects': page_obj.object_list,
        'page_title': f"{category.name} Projects",
        'meta_description': f"Browse {category.name.lower()} projects by Fayvad Geosolutions. {category.description}",
    }
    
    return render(request, 'project_by_category.html', context)


def projects_by_tag(request, tag_slug):
    """Projects filtered by tag"""
    tag = get_object_or_404(ProjectTag, slug=tag_slug, is_active=True)
    
    projects = Project.objects.filter(
        tags=tag,
        is_active=True
    ).select_related('category')
    
    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
        'projects': page_obj.object_list,
        'page_title': f"Projects tagged '{tag.name}'",
        'meta_description': f"Projects related to {tag.name}. {tag.description}",
    }
    
    return render(request, 'project_by_tag.html', context)


def achievements_list(request):
    """List company achievements and awards"""
    achievements = Achievement.objects.filter(is_active=True).order_by('-date_achieved')
    
    # Group by type
    achievements_by_type = {}
    for achievement in achievements:
        type_name = achievement.get_achievement_type_display()
        if type_name not in achievements_by_type:
            achievements_by_type[type_name] = []
        achievements_by_type[type_name].append(achievement)
    
    # Get featured achievements
    featured_achievements = Achievement.objects.filter(
        is_featured=True,
        is_active=True
    )[:4]
    
    context = {
        'achievements': achievements,
        'achievements_by_type': achievements_by_type,
        'featured_achievements': featured_achievements,
        'page_title': 'Awards & Achievements',
        'meta_description': 'Recognition and awards received by Fayvad Geosolutions including the 2025 ISK Land Surveyors Excellence Award and international research recognition.',
    }
    
    return render(request, 'achievements.html', context)


def project_timeline(request):
    """Timeline view of all projects"""
    projects = Project.objects.filter(
        is_active=True
    ).select_related('category').order_by('-start_date')
    
    # Group projects by year
    projects_by_year = {}
    for project in projects:
        year = project.start_date.year
        if year not in projects_by_year:
            projects_by_year[year] = []
        projects_by_year[year].append(project)
    
    context = {
        'projects_by_year': projects_by_year,
        'page_title': 'Project Timeline',
        'meta_description': 'Chronological timeline of Fayvad Geosolutions projects from inception to present, showcasing our growth and expertise development.',
    }
    
    return render(request, 'project_timeline.html', context)


@require_GET
def project_search_api(request):
    """AJAX API for project search"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 3:
        return JsonResponse({'results': []})
    
    projects = Project.objects.filter(
        Q(title__icontains=query) |
        Q(short_description__icontains=query) |
        Q(client_name__icontains=query) |
        Q(location__icontains=query),
        is_active=True
    ).select_related('category')[:10]
    
    results = []
    for project in projects:
        results.append({
            'title': project.title,
            'url': project.get_absolute_url(),
            'description': project.short_description[:100] + '...' if len(project.short_description) > 100 else project.short_description,
            'client': project.client_name,
            'category': project.category.name,
            'year': project.start_date.year,
        })
    
    return JsonResponse({'results': results})


def case_studies(request):
    """Detailed case studies page"""
    case_studies = Project.objects.filter(
        is_case_study=True,
        is_active=True,
        status='completed'
    ).select_related('category')
    
    # Get filter parameters
    category_slug = request.GET.get('category')
    if category_slug:
        case_studies = case_studies.filter(category__slug=category_slug)
    
    # Get categories for filtering
    categories = ProjectCategory.objects.filter(
        is_active=True,
        projects__is_case_study=True,
        projects__is_active=True
    ).annotate(case_study_count=Count('projects')).distinct()
    
    # Pagination
    paginator = Paginator(case_studies, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'case_studies': page_obj.object_list,
        'categories': categories,
        'current_category': category_slug,
        'page_title': 'Case Studies',
        'meta_description': 'In-depth case studies showcasing Fayvad Geosolutions expertise in delivering complex geospatial projects across Kenya and internationally.',
    }
    
    return render(request, 'case_studies.html', context)


def success_stories(request):
    """Success stories and impact page"""
    # Get projects with strong results/impact
    success_projects = Project.objects.filter(
        is_active=True,
        status='completed',
        testimonials__isnull=False
    ).distinct().select_related('category')[:6]
    
    # Get key statistics
    stats = {
        'projects_completed': Project.objects.filter(status='completed', is_active=True).count(),
        'clients_served': Project.objects.filter(is_active=True).values('client_organization').distinct().count(),
        'total_area_surveyed': '2,500+ km²',  # Could be calculated from actual data
        'average_rating': 4.9,  # Could be calculated from testimonials
    }
    
    # Get featured testimonials
    featured_testimonials = []
    for project in success_projects:
        testimonial = project.testimonials.filter(is_featured=True, is_active=True).first()
        if testimonial:
            featured_testimonials.append(testimonial)
    
    context = {
        'success_projects': success_projects,
        'stats': stats,
        'featured_testimonials': featured_testimonials[:4],
        'page_title': 'Success Stories',
        'meta_description': 'Real success stories and client testimonials showcasing the impact of Fayvad Geosolutions geospatial expertise across diverse projects.',
    }
    
    return render(request, 'success_stories.html', context)