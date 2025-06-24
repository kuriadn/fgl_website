from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML
from .models import BlogComment, BlogSubscriber


class BlogSearchForm(forms.Form):
    """Simple blog search form"""
    q = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search articles, insights, case studies...',
            'class': 'form-control form-control-lg',
            'autocomplete': 'off'
        }),
        label='Search'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'blog-search-form'
        self.helper.form_show_labels = False
        
        self.helper.layout = Layout(
            Div(
                'q',
                HTML('<button type="submit" class="btn btn-primary btn-lg ms-2"><i class="fas fa-search me-2"></i>Search</button>'),
                css_class='input-group'
            )
        )


class CommentForm(forms.ModelForm):
    """Comment submission form"""
    
    class Meta:
        model = BlogComment
        fields = ['author_name', 'author_email', 'author_website', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'class': 'form-control'
            }),
            'author_email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com',
                'class': 'form-control'
            }),
            'author_website': forms.URLInput(attrs={
                'placeholder': 'https://yourwebsite.com (optional)',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Share your thoughts on this article...',
                'rows': 4,
                'class': 'form-control'
            })
        }
        labels = {
            'author_name': 'Name',
            'author_email': 'Email',
            'author_website': 'Website',
            'content': 'Comment'
        }
    
    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 10:
            raise ValidationError('Comment must be at least 10 characters long.')
        return content
    
    def clean_author_name(self):
        name = self.cleaned_data['author_name']
        if len(name) < 2:
            raise ValidationError('Please enter your full name.')
        return name


class SubscriptionForm(forms.ModelForm):
    """Newsletter subscription form"""
    
    class Meta:
        model = BlogSubscriber
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address',
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Your name (optional)',
                'class': 'form-control'
            })
        }
        labels = {
            'email': 'Email Address',
            'name': 'Name'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'subscription-form'
        self.helper.form_id = 'blog-subscription-form'
        
        self.helper.layout = Layout(
            HTML('<div class="subscription-header"><h4><i class="fas fa-envelope me-2"></i>Stay Updated</h4><p class="text-muted">Get the latest insights on geospatial technology and innovation.</p></div>'),
            'name',
            'email',
            HTML('<div class="form-text mb-3"><small><i class="fas fa-shield-alt me-1"></i>We respect your privacy. Unsubscribe at any time.</small></div>'),
            Submit('subscribe', 'Subscribe Now', css_class='btn btn-secondary btn-lg w-100')
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if email:
            # Check if already subscribed
            if BlogSubscriber.objects.filter(email=email, is_active=True).exists():
                raise ValidationError('This email is already subscribed to our blog updates.')
        
        return email