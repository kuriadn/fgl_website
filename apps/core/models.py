"""
Core models for Fayvad Geosolutions.
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.core.validators import EmailValidator, RegexValidator

class TimestampMixin(models.Model):
    """Abstract model to add timestamp fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Page(TimestampMixin):
    """Static pages model."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = RichTextField()
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'title']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:page_detail', kwargs={'slug': self.slug})

class ContactMessage(TimestampMixin):
    """Contact form submissions."""
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('quote', 'Request Quote'),
        ('support', 'Technical Support'),
        ('partnership', 'Partnership'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    phone = models.CharField(
        max_length=20, 
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be in format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    company = models.CharField(max_length=200, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_full_name()} - {self.subject}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return self.get_full_name()

class Newsletter(TimestampMixin):
    """Newsletter subscriptions."""
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    is_active = models.BooleanField(default=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.email

class Testimonial(TimestampMixin):
    """Client testimonials."""
    client_name = models.CharField(max_length=200)
    client_title = models.CharField(max_length=200, blank=True)
    client_company = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    project = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-created_at']
        
    def __str__(self):
        return f"{self.client_name} - {self.client_company}"

class FAQ(TimestampMixin):
    """Frequently Asked Questions."""
    CATEGORIES = [
        ('general', 'General'),
        ('services', 'Services'),
        ('pricing', 'Pricing'),
        ('technical', 'Technical'),
        ('support', 'Support'),
    ]
    
    question = models.CharField(max_length=300)
    answer = RichTextField()
    category = models.CharField(max_length=20, choices=CATEGORIES, default='general')
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['category', 'order', 'question']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        
    def __str__(self):
        return self.question

class CompanyInfo(TimestampMixin):
    """Company information singleton model."""
    name = models.CharField(max_length=200, default='Fayvad Geosolutions Ltd')
    tagline = models.CharField(max_length=300, default='PhD-Level GIS Expertise')
    description = RichTextField(blank=True)
    
    # Contact Information
    phone = models.CharField(max_length=20, default='+254 769 069 640')
    email = models.EmailField(default='info@geo.fayvad.com')
    address = models.TextField(default='Grace House 3rd Floor Suite 10, Nkuruma Road, Thika, Kenya')
    
    # Business Hours
    business_hours = models.TextField(
        default='Monday - Friday: 8:00 AM - 5:00 PM\nSaturday: By Appointment\nSunday: Emergency Only'
    )
    
    # Social Media
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    
    # SEO
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    class Meta:
        verbose_name = 'Company Information'
        verbose_name_plural = 'Company Information'
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and CompanyInfo.objects.exists():
            raise ValueError('Only one CompanyInfo instance allowed')
        super().save(*args, **kwargs)
    
    @classmethod
    def get_solo(cls):
        """Get or create the singleton instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class Achievement(TimestampMixin):
    """Company achievements and awards."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_achieved = models.DateField()
    organization = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-date_achieved', 'order']
        
    def __str__(self):
        return f"{self.title} ({self.date_achieved.year})"