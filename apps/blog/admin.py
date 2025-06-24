from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import BlogCategory, BlogPost, BlogComment, BlogSubscriber, ReadingHistory


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'post_count_display', 'color_display', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Appearance', {
            'fields': ('color', 'icon')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def post_count_display(self, obj):
        count = obj.post_count
        if count > 0:
            url = reverse('admin:blog_blogpost_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} posts</a>', url, count)
        return '0 posts'
    post_count_display.short_description = 'Posts'
    
    def color_display(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%; display: inline-block;"></div>',
            obj.color
        )
    color_display.short_description = 'Color'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'category', 'status', 'featured', 'view_count', 
        'is_sticky', 'published_at', 'created_at'
    ]
    list_filter = [
        'status', 'featured', 'is_sticky', 'category', 'author', 
        'created_at', 'published_at'
    ]
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'read_time', 'created_at', 'updated_at']
    filter_horizontal = ['related_posts']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'excerpt', 'content', 'featured_image')
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('status', 'featured', 'is_sticky', 'allow_comments', 'published_at')
        }),
        ('Relationships', {
            'fields': ('related_posts',),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('view_count', 'read_time'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'author').prefetch_related('tags')
    
    def save_model(self, request, obj, form, change):
        if not change:  # New post
            obj.author = request.user
        
        # Auto-publish if status is changed to published and no publish date
        if obj.status == 'published' and not obj.published_at:
            obj.published_at = timezone.now()
        
        super().save_model(request, obj, form, change)
    
    actions = ['make_published', 'make_draft', 'make_featured', 'remove_featured']
    
    def make_published(self, request, queryset):
        updated = queryset.update(status='published', published_at=timezone.now())
        self.message_user(request, f'{updated} posts were successfully published.')
    make_published.short_description = "Mark selected posts as published"
    
    def make_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} posts were marked as draft.')
    make_draft.short_description = "Mark selected posts as draft"
    
    def make_featured(self, request, queryset):
        updated = queryset.update(featured='grid')
        self.message_user(request, f'{updated} posts were marked as featured.')
    make_featured.short_description = "Mark selected posts as featured"
    
    def remove_featured(self, request, queryset):
        updated = queryset.update(featured='none')
        self.message_user(request, f'{updated} posts were removed from featured.')
    remove_featured.short_description = "Remove featured status"


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'is_approved', 'created_at', 'content_preview']
    list_filter = ['is_approved', 'created_at', 'post__category']
    search_fields = ['author_name', 'author_email', 'content', 'post__title']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'author_name', 'author_email', 'author_website', 'content')
        }),
        ('Moderation', {
            'fields': ('is_approved',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post')
    
    actions = ['approve_comments', 'unapprove_comments']
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} comments were approved.')
    approve_comments.short_description = "Approve selected comments"
    
    def unapprove_comments(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} comments were unapproved.')
    unapprove_comments.short_description = "Unapprove selected comments"


@admin.register(BlogSubscriber)
class BlogSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'subscribed_at', 'confirmed_at']
    list_filter = ['is_active', 'subscribed_at', 'confirmed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['subscribed_at', 'confirmed_at']
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email', 'name')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('subscribed_at', 'confirmed_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['activate_subscribers', 'deactivate_subscribers', 'export_emails']
    
    def activate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscribers were activated.')
    activate_subscribers.short_description = "Activate selected subscribers"
    
    def deactivate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscribers were deactivated.')
    deactivate_subscribers.short_description = "Deactivate selected subscribers"
    
    def export_emails(self, request, queryset):
        from django.http import HttpResponse
        import csv
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="blog_subscribers.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Email', 'Name', 'Subscribed Date', 'Is Active'])
        
        for subscriber in queryset:
            writer.writerow([
                subscriber.email,
                subscriber.name,
                subscriber.subscribed_at.strftime('%Y-%m-%d'),
                'Yes' if subscriber.is_active else 'No'
            ])
        
        return response
    export_emails.short_description = "Export email list as CSV"


@admin.register(ReadingHistory)
class ReadingHistoryAdmin(admin.ModelAdmin):
    list_display = ['post', 'session_key_short', 'read_at', 'time_spent_display']
    list_filter = ['read_at', 'post__category']
    search_fields = ['post__title', 'session_key']
    readonly_fields = ['session_key', 'post', 'read_at', 'time_spent']
    
    def session_key_short(self, obj):
        return obj.session_key[:8] + '...' if len(obj.session_key) > 8 else obj.session_key
    session_key_short.short_description = 'Session'
    
    def time_spent_display(self, obj):
        if obj.time_spent < 60:
            return f'{obj.time_spent}s'
        elif obj.time_spent < 3600:
            return f'{obj.time_spent // 60}m {obj.time_spent % 60}s'
        else:
            hours = obj.time_spent // 3600
            minutes = (obj.time_spent % 3600) // 60
            return f'{hours}h {minutes}m'
    time_spent_display.short_description = 'Time Spent'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('post')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


# Custom admin site configuration
admin.site.site_header = "Fayvad Geosolutions Blog Administration"
admin.site.site_title = "Blog Admin"
admin.site.index_title = "Blog Management"