from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


class ProjectCategory(models.Model):
    """Categories for organizing projects"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Emoji or icon class")
    color = models.CharField(max_length=7, default="#1e3c72", help_text="Hex color code")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Project Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    """Main projects/case studies"""
    
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    
    PRIORITY_CHOICES = [
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='projects')
    client_name = models.CharField(max_length=200)
    client_organization = models.CharField(max_length=200)
    
    # Project Details
    short_description = models.TextField(max_length=300, help_text="Brief description for cards")
    detailed_description = models.TextField(help_text="Full project description")
    
    # Project Scope
    location = models.CharField(max_length=200, help_text="Project location")
    area_covered = models.CharField(max_length=100, blank=True, help_text="e.g., '251 km', '1,200 hectares'")
    project_value = models.CharField(max_length=100, blank=True, help_text="e.g., 'KES 50M', '€540K'")
    
    # Timeline
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=100, help_text="e.g., '18 months', '2021-2024'")
    
    # Content
    challenge = models.TextField(help_text="Project challenge/problem statement")
    solution = models.TextField(help_text="Our solution/approach")
    results = models.TextField(help_text="Project results/outcomes")
    
    # Technical Details
    services_provided = models.JSONField(default=list, help_text="List of services provided")
    technologies_used = models.JSONField(default=list, help_text="Technologies and tools used")
    team_size = models.PositiveIntegerField(null=True, blank=True, help_text="Team size")
    
    # Metrics and KPIs
    key_metrics = models.JSONField(default=dict, help_text="Key metrics as JSON object")
    success_metrics = models.JSONField(default=list, help_text="Success metrics/achievements")
    
    # Media and Files
    featured_image = models.ImageField(upload_to='projects/', blank=True)
#    project_files = models.JSONField(default=list, help_text="List of project files/documents")
    
    # SEO and Meta
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    
    # Status and Features
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    is_case_study = models.BooleanField(default=True, help_text="Available as detailed case study")
    is_confidential = models.BooleanField(default=False, help_text="Limit public details")
    
    # Ordering and Display
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', 'order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})

    @property
    def is_ongoing(self):
        return self.status in ['planning', 'in_progress']

    @property
    def completion_year(self):
        if self.end_date:
            return self.end_date.year
        elif self.status == 'completed':
            return self.start_date.year
        return None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.meta_title:
            self.meta_title = f"{self.title} - Case Study"
        if not self.meta_description:
            self.meta_description = self.short_description[:280]
        super().save(*args, **kwargs)


class ProjectFile(models.Model):
    """Project files and documents"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='projects/files/', help_text="Upload project documents, reports, etc.")
    name = models.CharField(max_length=200, help_text="Display name for the file")
    description = models.TextField(blank=True, help_text="Optional description of the file")
    file_type = models.CharField(max_length=50, blank=True, help_text="e.g., 'Report', 'Presentation', 'Data'")
    is_public = models.BooleanField(default=True, help_text="Show to public visitors")
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.project.title} - {self.name}"

    @property
    def file_size_mb(self):
        """Return file size in MB"""
        if self.file:
            return round(self.file.size / 1048576, 2)  # Convert bytes to MB
        return 0

    @property
    def file_extension(self):
        """Return file extension"""
        if self.file:
            return self.file.name.split('.')[-1].upper()
        return ""

class ProjectImage(models.Model):
    """Additional images for projects"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    alt_text = models.CharField(max_length=200, help_text="Alt text for accessibility")
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.project.title} - Image {self.id}"


class ProjectMilestone(models.Model):
    """Project milestones and key achievements"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_achieved = models.DateField()
    is_major = models.BooleanField(default=False, help_text="Major milestone")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['date_achieved', 'order']

    def __str__(self):
        return f"{self.project.title} - {self.title}"


class ProjectTestimonial(models.Model):
    """Client testimonials for specific projects"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='testimonials')
    client_name = models.CharField(max_length=200)
    client_title = models.CharField(max_length=200)
    client_organization = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text="Rating out of 5")
    date_given = models.DateField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_given']

    def __str__(self):
        return f"{self.project.title} - {self.client_name}"


class ProjectUpdate(models.Model):
    """Progress updates for ongoing projects"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200)
    content = models.TextField()
    update_date = models.DateField()
    progress_percentage = models.PositiveIntegerField(
        null=True, blank=True, 
        help_text="Overall project progress (0-100)"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_public = models.BooleanField(default=True, help_text="Show to public")

    class Meta:
        ordering = ['-update_date']

    def __str__(self):
        return f"{self.project.title} - {self.title}"


class ProjectTag(models.Model):
    """Tags for projects"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#6c757d", help_text="Hex color code")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProjectTagging(models.Model):
    """Many-to-many relationship between Projects and Tags"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = models.ForeignKey(ProjectTag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['project', 'tag']

    def __str__(self):
        return f"{self.project.title} - {self.tag.name}"


# Add tags relationship to Project model
Project.add_to_class(
    'tags',
    models.ManyToManyField(
        ProjectTag,
        through=ProjectTagging,
        blank=True,
        help_text="Tags for this project"
    )
)


class Achievement(models.Model):
    """Company achievements and awards"""
    
    ACHIEVEMENT_TYPES = [
        ('award', 'Award'),
        ('certification', 'Certification'),
        ('recognition', 'Recognition'),
        ('milestone', 'Milestone'),
        ('publication', 'Publication'),
    ]
    
    title = models.CharField(max_length=200)
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    description = models.TextField()
    awarding_body = models.CharField(max_length=200, blank=True)
    date_achieved = models.DateField()
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='achievements',
        help_text="Related project (if any)"
    )
    
    # Additional details
    certificate_url = models.URLField(blank=True, help_text="Link to certificate/documentation")
    value = models.CharField(max_length=100, blank=True, help_text="Award value if applicable")
    
    # Display
    icon = models.CharField(max_length=50, default="🏆", help_text="Emoji or icon")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date_achieved', 'order']

    def __str__(self):
        return self.title