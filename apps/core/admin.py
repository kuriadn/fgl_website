"""
Admin configuration for core models.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    Page, ContactMessage, Newsletter, Testimonial, 
    FAQ, CompanyInfo, Achievement
)

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """Admin interface for Page model."""
    list_display = ['title', 'slug', 'is_published', 'order', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'order']
    ordering = ['order', 'title']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'content')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('is_published', 'order')
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for ContactMessage model."""
    list_display = [
        'get_full_name', 'email', 'inquiry_type', 
        'subject', 'is_read', 'created_at'
    ]
    list_filter = ['inquiry_type', 'is_read', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'subject', 'message']
    readonly_fields = ['created_at', 'ip_address']
    list_editable = ['is_read']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'company')
        }),
        ('Message Details', {
            'fields': ('inquiry_type', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('System Information', {
            'fields': ('created_at', 'ip_address'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Name'
    get_full_name.admin_order_field = 'first_name'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Admin interface for Newsletter model."""
    list_display = ['email', 'is_active', 'confirmed_at', 'created_at']
    list_filter = ['is_active', 'confirmed_at', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at', 'ip_address']
    list_editable = ['is_active']
    ordering = ['-created_at']
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True)
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    def deactivate_subscriptions(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_subscriptions.short_description = "Deactivate selected subscriptions"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin interface for Testimonial model."""
    list_display = [
        'client_name', 'client_company', 'rating', 
        'is_featured', 'is_published', 'order', 'created_at'
    ]
    list_filter = ['rating', 'is_featured', 'is_published', 'created_at']
    search_fields = ['client_name', 'client_company', 'content', 'project']
    list_editable = ['is_featured', 'is_published', 'order']
    ordering = ['order', '-created_at']
    
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'client_title', 'client_company')
        }),
        ('Testimonial Content', {
            'fields': ('content', 'rating', 'project')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_published', 'order')
        }),
    )
    
    def get_rating_display(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: #ffc107;">{}</span>', stars)
    get_rating_display.short_description = 'Rating'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Admin interface for FAQ model."""
    list_display = ['question', 'category', 'is_published', 'order']
    list_filter = ['category', 'is_published']
    search_fields = ['question', 'answer']
    list_editable = ['is_published', 'order']
    ordering = ['category', 'order']
    
    fieldsets = (
        ('Question & Answer', {
            'fields': ('question', 'answer')
        }),
        ('Organization', {
            'fields': ('category', 'order')
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
    )

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    """Admin interface for CompanyInfo model."""
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not CompanyInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'tagline', 'description')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address', 'business_hours')
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'twitter_url', 'facebook_url'),
            'classes': ('collapse',)
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """Admin interface for Achievement model."""
    list_display = ['title', 'organization', 'date_achieved', 'is_featured', 'order']
    list_filter = ['is_featured', 'date_achieved', 'organization']
    search_fields = ['title', 'description', 'organization']
    list_editable = ['is_featured', 'order']
    ordering = ['-date_achieved', 'order']
    date_hierarchy = 'date_achieved'
    
    fieldsets = (
        ('Achievement Details', {
            'fields': ('title', 'description', 'date_achieved', 'organization')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'order')
        }),
    )

# Customize admin site
admin.site.site_header = 'Fayvad Geosolutions Administration'
admin.site.site_title = 'Fayvad Admin'
admin.site.index_title = 'Welcome to Fayvad Geosolutions Administration'