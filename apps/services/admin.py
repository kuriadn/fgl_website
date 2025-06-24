from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    ServiceCategory, Service, ServiceFeature, ServiceBenefit,
    ServiceFAQ, ServiceInquiry, ServiceTestimonial, ServiceCaseStudy
)


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1
    fields = ['title', 'description', 'icon', 'order', 'is_active']


class ServiceBenefitInline(admin.TabularInline):
    model = ServiceBenefit
    extra = 1
    fields = ['title', 'description', 'icon', 'order']


class ServiceFAQInline(admin.TabularInline):
    model = ServiceFAQ
    extra = 1
    fields = ['question', 'answer', 'order', 'is_active']


class ServiceTestimonialInline(admin.TabularInline):
    model = ServiceTestimonial
    extra = 0
    fields = ['client_name', 'client_organization', 'content', 'rating', 'is_featured']
    readonly_fields = ['created_at']


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'service_count', 'order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

    def service_count(self, obj):
        return obj.services.filter(is_active=True).count()
    service_count.short_description = 'Active Services'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'priority', 'is_featured', 'is_active', 
        'inquiry_count', 'order'
    ]
    list_filter = [
        'category', 'priority', 'is_featured', 'is_active', 'created_at'
    ]
    search_fields = ['name', 'short_description', 'detailed_description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'icon', 'priority')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'detailed_description', 'overview')
        }),
        ('Service Details', {
            'fields': ('price_range', 'duration_range')
        }),
        ('Content (JSON Fields)', {
            'fields': ('key_features', 'deliverables', 'process_steps', 'technologies'),
            'description': 'Enter as JSON arrays, e.g., ["Feature 1", "Feature 2"]'
        }),
        ('SEO & Meta', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status & Ordering', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )
    
    inlines = [ServiceFeatureInline, ServiceBenefitInline, ServiceFAQInline]
    
    def inquiry_count(self, obj):
        count = obj.inquiries.count()
        if count > 0:
            url = reverse('admin:services_serviceinquiry_changelist')
            return format_html(
                '<a href="{}?service__id__exact={}">{}</a>',
                url, obj.id, count
            )
        return count
    inquiry_count.short_description = 'Inquiries'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ['created_at', 'updated_at']
        return []


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'service', 'icon', 'order', 'is_active']
    list_filter = ['service', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['service', 'order', 'title']


@admin.register(ServiceBenefit)
class ServiceBenefitAdmin(admin.ModelAdmin):
    list_display = ['title', 'service', 'icon', 'order']
    list_filter = ['service']
    search_fields = ['title', 'description']
    ordering = ['service', 'order', 'title']


@admin.register(ServiceFAQ)
class ServiceFAQAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'service', 'order', 'is_active']
    list_filter = ['service', 'is_active']
    search_fields = ['question', 'answer']
    ordering = ['service', 'order']

    def question_preview(self, obj):
        return obj.question[:50] + "..." if len(obj.question) > 50 else obj.question
    question_preview.short_description = 'Question'


@admin.register(ServiceInquiry)
class ServiceInquiryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'service', 'email', 'budget_range', 'status', 
        'created_at', 'inquiry_actions'
    ]
    list_filter = [
        'service', 'status', 'budget_range', 'created_at'
    ]
    search_fields = ['name', 'email', 'organization', 'project_description']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'organization')
        }),
        ('Service & Project', {
            'fields': ('service', 'project_description', 'budget_range', 'timeline', 'location')
        }),
        ('Internal Tracking', {
            'fields': ('status', 'notes', 'quoted_amount'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['mark_as_in_progress', 'mark_as_quoted', 'mark_as_won']

    def inquiry_actions(self, obj):
        actions = []
        if obj.email:
            actions.append(
                f'<a href="mailto:{obj.email}" target="_blank">Email</a>'
            )
        if obj.phone:
            actions.append(
                f'<a href="tel:{obj.phone}" target="_blank">Call</a>'
            )
        return mark_safe(' | '.join(actions))
    inquiry_actions.short_description = 'Actions'

    def mark_as_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} inquiries marked as in progress.')
    mark_as_in_progress.short_description = 'Mark as in progress'

    def mark_as_quoted(self, request, queryset):
        updated = queryset.update(status='quoted')
        self.message_user(request, f'{updated} inquiries marked as quoted.')
    mark_as_quoted.short_description = 'Mark as quoted'

    def mark_as_won(self, request, queryset):
        updated = queryset.update(status='won')
        self.message_user(request, f'{updated} inquiries marked as won.')
    mark_as_won.short_description = 'Mark as won'


@admin.register(ServiceTestimonial)
class ServiceTestimonialAdmin(admin.ModelAdmin):
    list_display = [
        'client_name', 'service', 'client_organization', 'rating', 
        'is_featured', 'is_active', 'created_at'
    ]
    list_filter = ['service', 'rating', 'is_featured', 'is_active', 'created_at']
    search_fields = ['client_name', 'client_organization', 'content']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_title', 'client_organization')
        }),
        ('Testimonial', {
            'fields': ('service', 'content', 'rating')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
    )


@admin.register(ServiceCaseStudy)
class ServiceCaseStudyAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'service', 'client', 'project_duration', 
        'is_featured', 'is_active', 'created_at'
    ]
    list_filter = ['service', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'client', 'challenge', 'solution']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'service', 'client')
        }),
        ('Project Details', {
            'fields': ('project_duration', 'project_value')
        }),
        ('Content', {
            'fields': ('challenge', 'solution', 'results')
        }),
        ('Metrics', {
            'fields': ('metrics',),
            'description': 'Enter as JSON object, e.g., {"area_surveyed": "251 km", "accuracy": "±2cm"}'
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
    )

# Admin site customization
admin.site.site_header = "Fayvad Geosolutions Admin"
admin.site.site_title = "Fayvad Admin"
admin.site.index_title = "Services Administration"