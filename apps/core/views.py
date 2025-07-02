"""
Views for the core application.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Page, ContactMessage, Newsletter, Testimonial, FAQ, CompanyInfo, Achievement
from .forms import ContactForm, NewsletterForm
from apps.services.models import Service
from apps.portfolio.models import Project

class HomeView(TemplateView):
    """Homepage view with dynamic content."""
    template_name = 'home.html'
    
    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get featured content
        context.update({
            'services': Service.objects.filter(is_featured=True, is_active=True)[:6],
            'featured_projects': Project.objects.filter(is_featured=True, is_active=True)[:3],
            'testimonials': Testimonial.objects.filter(is_featured=True, is_published=True)[:4],
            'achievements': Achievement.objects.filter(is_featured=True)[:4],
            'company_info': CompanyInfo.get_solo(),
        })
        
        return context

class AboutView(TemplateView):
    """About page view."""
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({
            'achievements': Achievement.objects.all()[:10],
            'company_info': CompanyInfo.get_solo(),
            'testimonials': Testimonial.objects.filter(is_published=True)[:6],
        })
        
        return context

class ContactView(CreateView):
    """Contact page with form."""
    model = ContactMessage
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = reverse_lazy('core:contact_success')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context.update({
            'company_info': CompanyInfo.get_solo(),
            'faqs': FAQ.objects.filter(is_published=True, category='general')[:5],
        })
        
        return context
    
    def form_valid(self, form):
        # Save the contact message
        contact_message = form.save(commit=False)
        contact_message.ip_address = self.get_client_ip()
        contact_message.save()
        
        # Send notification email
        self.send_notification_email(contact_message)
        
        # Add success message
        messages.success(
            self.request, 
            'Thank you for your message! We will respond within 24 hours during business hours.'
        )
        
        return super().form_valid(form)
    
    def get_client_ip(self):
        """Get client IP address."""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
    
    def send_notification_email(self, contact_message):
        """Send notification email to admin."""
        try:
            subject = f'New Contact Form Submission: {contact_message.subject}'
            message = f'''
            New contact form submission from {contact_message.get_full_name()}
            
            Name: {contact_message.get_full_name()}
            Email: {contact_message.email}
            Phone: {contact_message.phone}
            Company: {contact_message.company}
            Inquiry Type: {contact_message.get_inquiry_type_display()}
            Subject: {contact_message.subject}
            
            Message:
            {contact_message.message}
            
            Submitted at: {contact_message.created_at}
            IP Address: {contact_message.ip_address}
            '''
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            # Log the error but don't fail the form submission
            print(f"Failed to send notification email: {e}")

class ContactSuccessView(TemplateView):
    """Contact form success page."""
    template_name = 'contact_success.html'

class PageDetailView(DetailView):
    """Generic page detail view."""
    model = Page
    template_name = 'page_detail.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Page.objects.filter(is_published=True)

class SearchView(ListView):
    """Site-wide search view."""
    template_name = 'search.html'
    context_object_name = 'results'
    paginate_by = 20
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        
        if not query:
            return []
        
        # Search across multiple models
        results = []
        
        # Search pages
        pages = Page.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True
        )
        for page in pages:
            results.append({
                'title': page.title,
                'content': page.content[:200] + '...' if len(page.content) > 200 else page.content,
                'url': page.get_absolute_url(),
                'type': 'Page'
            })
        
        # Search services
        services = Service.objects.filter(
            Q(name__icontains=query) | Q(detailed_description__icontains=query),
            is_active=True
        )
        for service in services:
            results.append({
                'title': service.name,
                'content': service.detailed_description[:200] + '...' if len(service.detailed_description) > 200 else service.detailed_description,
                'url': service.get_absolute_url(),
                'type': 'Service'
            })
        
        # Search projects
        projects = Project.objects.filter(
            Q(title__icontains=query) | Q(detailed_description__icontains=query),
            is_active=True
        )
        for project in projects:
            results.append({
                'title': project.title,
                'content': project.detailed_description[:200] + '...' if len(project.detailed_description) > 200 else project.detailed_description,
                'url': project.get_absolute_url(),
                'type': 'Project'
            })
        
        return results
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

# AJAX Views
@csrf_exempt
def newsletter_subscribe(request):
    """AJAX newsletter subscription."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '')
            
            if not email:
                return JsonResponse({'success': False, 'message': 'Email is required'})
            
            # Check if already subscribed
            if Newsletter.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already subscribed'})
            
            # Create subscription
            Newsletter.objects.create(
                email=email,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return JsonResponse({'success': True, 'message': 'Successfully subscribed to newsletter!'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def search_api(request):
    """API endpoint for search suggestions."""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    results = []
    
    # Quick search across key models
    services = Service.objects.filter(
        name__icontains=query, is_active=True
    )[:3]
    
    for service in services:
        results.append({
            'title': service.name,
            'url': service.get_absolute_url(),
            'type': 'Service',
            'snippet': service.short_description[:100] + '...' if len(service.short_description) > 100 else service.short_description
        })
    
    projects = Project.objects.filter(
        title__icontains=query, is_active=True
    )[:3]
    
    for project in projects:
        results.append({
            'title': project.title,
            'url': project.get_absolute_url(),
            'type': 'Project',
            'snippet': project.short_description[:100] + '...' if len(project.short_description) > 100 else project.short_description
        })
    
    return JsonResponse({'results': results})

# Error Views
def custom_404(request, exception):
    """Custom 404 error page."""
    return render(request, '404.html', status=404)

def custom_500(request):
    """Custom 500 error page."""
    return render(request, '500.html', status=500)

def custom_400(request):
    """Custom 400 error page."""
    return render(request, '400.html', status=400)