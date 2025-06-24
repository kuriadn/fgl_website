from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .models import Service, ServiceCategory, ServiceInquiry, ServiceCaseStudy
from .forms import ServiceInquiryForm


def services_list(request):
    """List all active services grouped by category"""
    categories = ServiceCategory.objects.filter(
        is_active=True,
        services__is_active=True
    ).distinct().prefetch_related('services')
    
    featured_services = Service.objects.filter(
        is_featured=True,
        is_active=True
    )[:3]
    
    context = {
        'categories': categories,
        'featured_services': featured_services,
        'page_title': 'Our Services',
        'meta_description': 'Comprehensive geospatial services including land surveying, GIS development, drone mapping, environmental intelligence, and government technology solutions.',
    }
    return render(request, 'list.html', context)


def service_detail(request, slug):
    """Detailed view of a specific service"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    # Get related services from same category
    related_services = Service.objects.filter(
        category=service.category,
        is_active=True
    ).exclude(id=service.id)[:3]
    
    # Get testimonials
    testimonials = service.testimonials.filter(is_active=True)[:3]
    
    # Get case studies
    case_studies = service.case_studies.filter(is_active=True)[:2]
    
    # Initialize inquiry form
    inquiry_form = ServiceInquiryForm()
    
    context = {
        'service': service,
        'related_services': related_services,
        'testimonials': testimonials,
        'case_studies': case_studies,
        'inquiry_form': inquiry_form,
        'page_title': service.meta_title or service.name,
        'meta_description': service.meta_description or service.short_description,
    }
    return render(request, 'service_detail.html', context)


def land_surveying(request):
    """Land Surveying Solutions page"""
    service = get_object_or_404(Service, slug='land-surveying', is_active=True)
    return service_detail(request, 'land-surveying')


def gis_development(request):
    """GIS Development & Analytics page"""
    service = get_object_or_404(Service, slug='gis-development', is_active=True)
    return service_detail(request, 'gis-development')


def drone_mapping(request):
    """Drone Mapping & Remote Sensing page"""
    service = get_object_or_404(Service, slug='drone-mapping', is_active=True)
    return service_detail(request, 'drone-mapping')


def environmental_intelligence(request):
    """Environmental Intelligence page"""
    service = get_object_or_404(Service, slug='environmental-intelligence', is_active=True)
    return service_detail(request, 'environmental-intelligence')


def government_solutions(request):
    """Government Technology Solutions page"""
    service = get_object_or_404(Service, slug='government-solutions', is_active=True)
    return service_detail(request, 'government-solutions')


def research_development(request):
    """Research & Development page"""
    service = get_object_or_404(Service, slug='research-development', is_active=True)
    return service_detail(request, 'research-development')


def case_study_detail(request, service_slug, slug):
    """Detailed view of a case study"""
    service = get_object_or_404(Service, slug=service_slug, is_active=True)
    case_study = get_object_or_404(
        ServiceCaseStudy,
        service=service,
        slug=slug,
        is_active=True
    )
    
    # Get other case studies from same service
    related_case_studies = ServiceCaseStudy.objects.filter(
        service=service,
        is_active=True
    ).exclude(id=case_study.id)[:3]
    
    context = {
        'case_study': case_study,
        'service': service,
        'related_case_studies': related_case_studies,
        'page_title': f"{case_study.title} - {service.name} Case Study",
        'meta_description': f"Case study: {case_study.title}. Learn how Fayvad Geosolutions delivered {service.name} solutions for {case_study.client}.",
    }
    return render(request, 'case_study.html', context)


@require_POST
def submit_inquiry(request):
    """Handle service inquiry form submission"""
    form = ServiceInquiryForm(request.POST)
    
    if form.is_valid():
        inquiry = form.save()
        
        # Send notification email to admin
        try:
            subject = f"New Service Inquiry: {inquiry.service.name}"
            message = render_to_string('inquiry_notification.html', {
                'inquiry': inquiry,
            })
            
            send_mail(
                subject=subject,
                message='',
                html_message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't fail the request
            print(f"Failed to send inquiry notification: {e}")
        
        # Send confirmation email to client
        try:
            subject = f"Thank you for your inquiry - {inquiry.service.name}"
            message = render_to_string('inquiry_confirmation.html', {
                'inquiry': inquiry,
            })
            
            send_mail(
                subject=subject,
                message='',
                html_message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[inquiry.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send inquiry confirmation: {e}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your inquiry! We will contact you within 24 hours.'
            })
        else:
            messages.success(
                request,
                'Thank you for your inquiry! We will contact you within 24 hours.'
            )
            return redirect('services:detail', slug=inquiry.service.slug)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = error_list[0]  # Get first error for each field
        
        return JsonResponse({
            'success': False,
            'message': 'Please correct the errors below.',
            'errors': errors
        })
    else:
        messages.error(request, 'Please correct the errors in the form.')
        # Redirect back to the service page with form errors
        service_slug = request.POST.get('service', '')
        if service_slug:
            return redirect('services:detail', slug=service_slug)
        return redirect('services:list')


def compare_services(request):
    """Compare multiple services side by side"""
    service_slugs = request.GET.get('services', '').split(',')
    service_slugs = [slug.strip() for slug in service_slugs if slug.strip()]
    
    if not service_slugs:
        return redirect('services:list')
    
    services = Service.objects.filter(
        slug__in=service_slugs,
        is_active=True
    )
    
    if not services:
        return redirect('services:list')
    
    context = {
        'services': services,
        'page_title': 'Compare Services',
        'meta_description': 'Compare Fayvad Geosolutions services to find the right solution for your project needs.',
    }
    return render(request, 'compare.html', context)


def service_capabilities(request):
    """Overview of all capabilities across services"""
    categories = ServiceCategory.objects.filter(
        is_active=True,
        services__is_active=True
    ).distinct().prefetch_related('services')
    
    # Get all unique technologies across services
    all_technologies = set()
    services = Service.objects.filter(is_active=True)
    for service in services:
        if service.technologies:
            all_technologies.update(service.technologies)
    
    context = {
        'categories': categories,
        'technologies': sorted(all_technologies),
        'page_title': 'Our Capabilities',
        'meta_description': 'Comprehensive overview of Fayvad Geosolutions capabilities in geospatial technology, surveying, GIS development, and environmental intelligence.',
    }
    return render(request, 'capabilities.html', context)


def get_service_quote(request, slug):
    """Get a quote for a specific service"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    if request.method == 'POST':
        form = ServiceInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            inquiry.status = 'quoted'  # Mark as quote request
            inquiry.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Quote request submitted! We will provide a detailed quote within 24 hours.'
                })
            else:
                messages.success(
                    request,
                    'Quote request submitted! We will provide a detailed quote within 24 hours.'
                )
                return redirect('services:detail', slug=slug)
    else:
        form = ServiceInquiryForm(initial={'service': service})
    
    context = {
        'service': service,
        'form': form,
        'page_title': f'Get Quote - {service.name}',
        'meta_description': f'Request a quote for {service.name} services from Fayvad Geosolutions. Professional geospatial solutions tailored to your needs.',
    }
    return render(request, 'quote.html', context)