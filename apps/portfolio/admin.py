from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (
    ProjectCategory, Project, ProjectFile, ProjectImage, ProjectMilestone,
    ProjectTestimonial, ProjectUpdate, ProjectTag, ProjectTagging, Achievement
)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'alt_text', 'order', 'is_featured']


class ProjectMilestoneInline(admin.TabularInline):
    model = ProjectMilestone
    extra = 1
    fields = ['title', 'description', 'date_achieved', 'is_major', 'order']


class ProjectTestimonialInline(admin.TabularInline):
    model = ProjectTestimonial
    extra = 0
    fields = ['client_name', 'client_title', 'client_organization', 'content', 'rating', 'is_featured']


class ProjectUpdateInline(admin.TabularInline):
    model = ProjectUpdate
    extra = 0
    fields = ['title', 'content', 'update_date', 'progress_percentage', 'is_public']

class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 1
    fields = ['name', 'file', 'description', 'file_type', 'is_public', 'order']
    readonly_fields = []
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('project')

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'project_count', 'order', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

    def project_count(self, obj):
        return obj.projects.filter(is_active=True).count()
    project_count.short_description = 'Active Projects'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'client_name', 'status', 'start_date', 
        'is_featured', 'is_active', 'order'
    ]
    list_filter = [
        'category', 'status', 'priority', 'is_featured', 'is_active', 
        'start_date', 'created_at'
    ]
    search_fields = [
        'title', 'client_name', 'client_organization', 'location', 
        'detailed_description'
    ]
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-start_date', 'order']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'client_name', 'client_organization')
        }),
        ('Project Details', {
            'fields': ('short_description', 'detailed_description', 'location', 'area_covered', 'project_value')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'duration', 'status', 'priority')
        }),
        ('Content', {
            'fields': ('challenge', 'solution', 'results')
        }),
        ('Technical Details', {
            'fields': ('services_provided', 'technologies_used', 'team_size'),
            'description': 'Enter as JSON arrays/objects'
        }),
        ('Metrics', {
            'fields': ('key_metrics', 'success_metrics'),
            'description': 'Enter as JSON objects/arrays'
        }),
        ('Media', {
            'fields': ('featured_image',),
            'classes': ('collapse',)
        }),
        ('SEO & Meta', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status & Features', {
            'fields': ('is_featured', 'is_case_study', 'is_confidential', 'order', 'is_active')
        }),
    )
    
    inlines = [ProjectImageInline, ProjectMilestoneInline, ProjectTestimonialInline, ProjectUpdateInline, ProjectFileInline]
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ['created_at', 'updated_at']
        return []


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'order', 'is_featured']
    list_filter = ['project', 'is_featured']
    search_fields = ['caption', 'alt_text']
    ordering = ['project', 'order']


@admin.register(ProjectMilestone)
class ProjectMilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'date_achieved', 'is_major', 'order']
    list_filter = ['project', 'is_major', 'date_achieved']
    search_fields = ['title', 'description']
    ordering = ['project', 'date_achieved', 'order']
    date_hierarchy = 'date_achieved'


@admin.register(ProjectTestimonial)
class ProjectTestimonialAdmin(admin.ModelAdmin):
    list_display = [
        'client_name', 'project', 'client_organization', 'rating', 
        'is_featured', 'is_active'
    ]
    list_filter = ['project', 'rating', 'is_featured', 'is_active', 'date_given']
    search_fields = ['client_name', 'client_organization', 'content']
    ordering = ['-date_given']
    date_hierarchy = 'date_given'


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'project', 'update_date', 'progress_percentage', 
        'author', 'is_public'
    ]
    list_filter = ['project', 'is_public', 'update_date']
    search_fields = ['title', 'content']
    ordering = ['-update_date']
    date_hierarchy = 'update_date'


@admin.register(ProjectTag)
class ProjectTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'achievement_type', 'awarding_body', 'date_achieved', 
        'project', 'is_featured', 'is_active'
    ]
    list_filter = [
        'achievement_type', 'is_featured', 'is_active', 'date_achieved'
    ]
    search_fields = ['title', 'description', 'awarding_body']
    ordering = ['-date_achieved', 'order']
    date_hierarchy = 'date_achieved'
    
    fieldsets = (
        ('Achievement Details', {
            'fields': ('title', 'achievement_type', 'description', 'awarding_body', 'date_achieved')
        }),
        ('Related Project', {
            'fields': ('project',),
            'description': 'Optional: Link this achievement to a specific project'
        }),
        ('Additional Information', {
            'fields': ('certificate_url', 'value'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('icon', 'is_featured', 'is_active', 'order')
        }),
    )

@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'file_type', 'is_public', 'file_size_mb', 'uploaded_at']
    list_filter = ['file_type', 'is_public', 'uploaded_at', 'project__category']
    search_fields = ['name', 'description', 'project__title']
    ordering = ['project', 'order', 'name']
    list_select_related = ['project']
    
    fieldsets = (
        ('File Information', {
            'fields': ('project', 'name', 'file', 'description')
        }),
        ('Categorization', {
            'fields': ('file_type', 'is_public', 'order')
        }),
    )

# Admin site customization
admin.site.site_header = 'Fayvad Geosolutions Administration'
admin.site.site_title = 'Fayvad Admin'
admin.site.index_title = 'Portfolio & Projects Administration'