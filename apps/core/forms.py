"""
Forms for the core application.
"""
from django import forms
from django.core.validators import EmailValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from crispy_forms.bootstrap import FormActions

from .models import ContactMessage, Newsletter

class ContactForm(forms.ModelForm):
    """Contact form with enhanced styling."""
    
    class Meta:
        model = ContactMessage
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'company', 'inquiry_type', 'subject', 'message'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter your first name',
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter your last name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+254 XXX XXX XXX',
                'class': 'form-control'
            }),
            'company': forms.TextInput(attrs={
                'placeholder': 'Your company name (optional)',
                'class': 'form-control'
            }),
            'inquiry_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Brief description of your inquiry',
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Please provide details about your project requirements, timeline, and any specific needs...',
                'rows': 5,
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'contact-form'
        self.helper.form_id = 'contact-form'
        
        self.helper.layout = Layout(
            HTML('<h4 class="mb-4">Get In Touch</h4>'),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-3'),
                Column('last_name', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-3'),
                Column('phone', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Div('company', css_class='form-group mb-3'),
            Row(
                Column('inquiry_type', css_class='form-group col-md-6 mb-3'),
                Column('subject', css_class='form-group col-md-6 mb-3'),
                css_class='form-row'
            ),
            Div('message', css_class='form-group mb-4'),
            FormActions(
                Submit('submit', 'Send Message', css_class='btn btn-primary btn-lg')
            )
        )
        
        # Add required field labels
        self.fields['first_name'].label = 'First Name *'
        self.fields['last_name'].label = 'Last Name *'
        self.fields['email'].label = 'Email Address *'
        self.fields['phone'].label = 'Phone Number'
        self.fields['company'].label = 'Company/Organization'
        self.fields['inquiry_type'].label = 'Inquiry Type *'
        self.fields['subject'].label = 'Subject *'
        self.fields['message'].label = 'Message *'
    
    def clean_email(self):
        """Validate email field."""
        email = self.cleaned_data.get('email')
        if email:
            validator = EmailValidator()
            validator(email)
        return email

class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form."""
    
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address',
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'newsletter-form d-flex'
        self.helper.form_show_labels = False
        
        self.helper.layout = Layout(
            Div(
                'email',
                Submit('submit', 'Subscribe', css_class='btn btn-primary ms-2'),
                css_class='input-group'
            )
        )
    
    def clean_email(self):
        """Validate email and check for duplicates."""
        email = self.cleaned_data.get('email')
        
        if email:
            # Validate email format
            validator = EmailValidator()
            validator(email)
            
            # Check if already subscribed
            if Newsletter.objects.filter(email=email, is_active=True).exists():
                raise forms.ValidationError('This email is already subscribed to our newsletter.')
        
        return email

class QuickContactForm(forms.Form):
    """Quick contact form for service-specific inquiries."""
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your full name',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            'class': 'form-control'
        })
    )
    service = forms.CharField(
        max_length=200,
        widget=forms.HiddenInput()
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell us about your project...',
            'rows': 4,
            'class': 'form-control'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'quick-contact-form'
        
        self.helper.layout = Layout(
            'name',
            'email',
            'service',
            'message',
            Submit('submit', 'Get Quote', css_class='btn btn-primary')
        )

class SearchForm(forms.Form):
    """Site search form."""
    q = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search services, projects, blog posts...',
            'class': 'form-control',
            'autocomplete': 'off'
        }),
        label='Search'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'search-form d-flex'
        self.helper.form_show_labels = False
        
        self.helper.layout = Layout(
            Div(
                'q',
                Submit('submit', 'Search', css_class='btn btn-outline-primary ms-2'),
                css_class='input-group'
            )
        )