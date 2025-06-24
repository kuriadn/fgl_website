from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class ServiceCategory(models.Model):
    """Service categories for organizing services"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Emoji or icon class")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    """Main services offered by Fayvad Geosolutions"""
    
    PRIORITY_CHOICES = [
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    short_description = models.TextField(max_length=300, help_text="Brief description for cards")
    detailed_description = models.TextField(help_text="Full service description")
    
    # Service details
    icon = models.CharField(max_length=50, help_text="Emoji or icon class")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    price_range = models.CharField(max_length=100, blank=True, help_text="e.g., 'KES 500K - 2M' or 'Contact for quote'")
    duration_range = models.CharField(max_length=100, blank=True, help_text="e.g., '2-6 months' or 'Project dependent'")
    
    # Content
    overview = models.TextField(help_text="Service overview section")
    key_features = models.JSONField(default=list, help_text="List of key features")
    deliverables = models.JSONField(default=list, help_text="List of deliverables")
    process_steps = models.JSONField(default=list, help_text="Process steps")
    technologies = models.JSONField(default=list, help_text="Technologies used")
    
    # SEO and meta
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_title:
            self.meta_title = f"{self.name} - Fayvad Geosolutions"
        if not self.meta_description:
            self.meta_description = self.short_description[:280]
        super().save(*args, **kwargs)


class ServiceFeature(models.Model):
    """Detailed features for services"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.service.name} - {self.title}"


class ServiceBenefit(models.Model):
    """Benefits of each service"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='benefits')
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.service.name} - {self.title}"


class ServiceFAQ(models.Model):
    """Frequently asked questions for services"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'question']
        verbose_name = "Service FAQ"
        verbose_name_plural = "Service FAQs"

    def __str__(self):
        return f"{self.service.name} - {self.question[:50]}"


class ServiceInquiry(models.Model):
    """Service-specific inquiries"""
    
    INQUIRY_STATUS = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('quoted', 'Quoted'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]
    
    BUDGET_RANGES = [
        ('under_500k', 'Under KES 500,000'),
        ('500k_1m', 'KES 500,000 - 1,000,000'),
        ('1m_5m', 'KES 1,000,000 - 5,000,000'),
        ('5m_10m', 'KES 5,000,000 - 10,000,000'),
        ('over_10m', 'Over KES 10,000,000'),
        ('discuss', 'Prefer to discuss'),
    ]
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='inquiries')
    
    # Contact details
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    
    # Project details
    project_description = models.TextField()
    budget_range = models.CharField(max_length=20, choices=BUDGET_RANGES, blank=True)
    timeline = models.CharField(max_length=200, blank=True, help_text="Expected timeline")
    location = models.CharField(max_length=200, blank=True, help_text="Project location")
    
    # Internal tracking
    status = models.CharField(max_length=20, choices=INQUIRY_STATUS, default='new')
    notes = models.TextField(blank=True, help_text="Internal notes")
    quoted_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Service Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.service.name} - {self.name} ({self.created_at.strftime('%Y-%m-%d')})"


class ServiceTestimonial(models.Model):
    """Service-specific testimonials"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='testimonials')
    client_name = models.CharField(max_length=200)
    client_title = models.CharField(max_length=200)
    client_organization = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text="Rating out of 5")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.service.name} - {self.client_name}"


class ServiceCaseStudy(models.Model):
    """Case studies for services"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='case_studies')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    client = models.CharField(max_length=200)
    project_duration = models.CharField(max_length=100)
    project_value = models.CharField(max_length=100, blank=True)
    
    # Content
    challenge = models.TextField(help_text="Project challenge")
    solution = models.TextField(help_text="Our solution")
    results = models.TextField(help_text="Project results")
    
    # Metrics
    metrics = models.JSONField(default=dict, help_text="Key metrics as JSON")
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Service Case Studies"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('services:case_study', kwargs={'service_slug': self.service.slug, 'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)