from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
import os


class BlogCategory(models.Model):
    """Blog categories for organizing posts"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#1e3c72', help_text='Hex color code')
    icon = models.CharField(max_length=50, default='fas fa-folder', help_text='FontAwesome icon class')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})
    
    @property
    def post_count(self):
        return self.posts.filter(status='published').count()


class BlogPost(models.Model):
    """Main blog post model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    FEATURED_CHOICES = [
        ('none', 'Not Featured'),
        ('hero', 'Hero Featured'),
        ('sidebar', 'Sidebar Featured'),
        ('grid', 'Grid Featured'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    
    # Content
    excerpt = models.TextField(max_length=500, help_text='Brief description shown in listings')
    content = RichTextUploadingField()
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    
    # SEO
    meta_title = models.CharField(max_length=60, blank=True, help_text='Leave blank to use post title')
    meta_description = models.CharField(max_length=160, blank=True, help_text='Leave blank to use excerpt')
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    # Publishing
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured = models.CharField(max_length=10, choices=FEATURED_CHOICES, default='none')
    is_sticky = models.BooleanField(default=False, help_text='Pin to top of listings')
    allow_comments = models.BooleanField(default=True)
    
    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    read_time = models.PositiveIntegerField(default=0, help_text='Estimated read time in minutes')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Relations
    tags = TaggableManager(blank=True)
    related_posts = models.ManyToManyField('self', blank=True, symmetrical=False)
    
    class Meta:
        ordering = ['-is_sticky', '-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['featured', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while BlogPost.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # Set published date when status changes to published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        # Auto-generate SEO fields if empty
        if not self.meta_title:
            self.meta_title = self.title[:60]
        if not self.meta_description:
            self.meta_description = self.excerpt[:160] if self.excerpt else ''
        
        # Calculate read time (average 200 words per minute)
        if self.content:
            # Remove HTML tags for word count
            import re
            clean_content = re.sub(r'<[^>]+>', '', self.content)
            word_count = len(clean_content.split())
            self.read_time = max(1, word_count // 200)
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        return self.status == 'published' and self.published_at and self.published_at <= timezone.now()
    
    @property
    def featured_image_url(self):
        if self.featured_image:
            return self.featured_image.url
        return None
    
    @property
    def next_post(self):
        """Get next published post"""
        return BlogPost.objects.filter(
            status='published',
            published_at__gt=self.published_at
        ).order_by('published_at').first()
    
    @property
    def previous_post(self):
        """Get previous published post"""
        return BlogPost.objects.filter(
            status='published',
            published_at__lt=self.published_at
        ).order_by('-published_at').first()
    
    def increment_view_count(self):
        """Thread-safe view count increment"""
        BlogPost.objects.filter(pk=self.pk).update(view_count=models.F('view_count') + 1)
        self.refresh_from_db(fields=['view_count'])


class BlogComment(models.Model):
    """Comments on blog posts"""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    author_website = models.URLField(blank=True)
    content = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'is_approved']),
            models.Index(fields=['is_approved', 'created_at']),
        ]
    
    def __str__(self):
        return f'Comment by {self.author_name} on {self.post.title}'


class BlogSubscriber(models.Model):
    """Email subscribers for blog updates"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        indexes = [
            models.Index(fields=['is_active', 'email']),
        ]
    
    def __str__(self):
        return self.email


class ReadingHistory(models.Model):
    """Track user reading behavior for recommendations"""
    session_key = models.CharField(max_length=40)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    read_at = models.DateTimeField(auto_now_add=True)
    time_spent = models.PositiveIntegerField(default=0, help_text='Time spent reading in seconds')
    
    class Meta:
        unique_together = ['session_key', 'post']
        ordering = ['-read_at']
        indexes = [
            models.Index(fields=['session_key', 'read_at']),
            models.Index(fields=['post', 'read_at']),
        ]