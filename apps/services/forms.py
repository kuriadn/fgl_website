from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, HTML, Row, Column, Submit
from crispy_forms.bootstrap import FormActions

from .models import ServiceInquiry, Service


class ServiceInquiryForm(forms.ModelForm):
    """Form for service inquiries and quote requests"""
    
    class Meta:
        model = ServiceInquiry
        fields = [
            'service', 'name', 'email', 'phone', 'organization',
            'project_description', 'budget_range', 'timeline', 'location'
        ]
        widgets = {
            'project_description': forms.Textarea(attrs={'rows': 5}),
            'service': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter active services only
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        
        # Update field attributes
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Your full name',
            'class': 'form-control'
        })
        
        self.fields['email'].widget.attrs.update({
            'placeholder': 'your.email@example.com',
            'class': 'form-control'
        })
        
        self.fields['phone'].widget.attrs.update({
            'placeholder': '+254 700 000 000',
            'class': 'form-control'
        })
        
        self.fields['organization'].widget.attrs.update({
            'placeholder': 'Your organization/company name',
            'class': 'form-control'
        })
        
        self.fields['project_description'].widget.attrs.update({
            'placeholder': 'Please describe your project requirements, objectives, and any specific needs...',
            'class': 'form-control'
        })
        
        self.fields['timeline'].widget.attrs.update({
            'placeholder': 'e.g., 3 months, ASAP, flexible',
            'class': 'form-control'
        })
        
        self.fields['location'].widget.attrs.update({
            'placeholder': 'Project location or area',
            'class': 'form-control'
        })

        # Set up Crispy Forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'service-inquiry-form'
        self.helper.layout = Layout(
            Fieldset(
                'Contact Information',
                Row(
                    Column('name', css_class='form-group col-md-6'),
                    Column('email', css_class='form-group col-md-6'),
                ),
                Row(
                    Column('phone', css_class='form-group col-md-6'),
                    Column('organization', css_class='form-group col-md-6'),
                ),
            ),
            Fieldset(
                'Project Details',
                'service',
                'project_description',
                Row(
                    Column('budget_range', css_class='form-group col-md-6'),
                    Column('timeline', css_class='form-group col-md-6'),
                ),
                'location',
            ),
            FormActions(
                Submit('submit', 'Submit Inquiry', css_class='btn btn-primary btn-lg'),
                HTML('<a href="{% url "core:contact" %}" class="btn btn-outline-secondary">Or Contact Us Directly</a>')
            )
        )

    def clean_phone(self):
        """Validate and format phone number"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove all non-digit characters except +
            import re
            phone = re.sub(r'[^\d+]', '', phone)
            
            # Format Kenyan numbers
            if phone.startswith('0'):
                phone = '+254' + phone[1:]
            elif phone.startswith('254'):
                phone = '+' + phone
            elif not phone.startswith('+'):
                phone = '+254' + phone
                
        return phone

    def clean_project_description(self):
        """Validate project description"""
        description = self.cleaned_data.get('project_description')
        if description and len(description) < 50:
            raise forms.ValidationError(
                "Please provide more details about your project (at least 50 characters)."
            )
        return description


class ServiceCompareForm(forms.Form):
    """Form for comparing multiple services"""
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Select 2-4 services to compare"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_action = 'services:compare'
        self.helper.layout = Layout(
            'services',
            Submit('compare', 'Compare Selected Services', css_class='btn btn-primary')
        )

    def clean_services(self):
        """Validate number of services selected"""
        services = self.cleaned_data.get('services')
        if services:
            if len(services) < 2:
                raise forms.ValidationError("Please select at least 2 services to compare.")
            if len(services) > 4:
                raise forms.ValidationError("Please select no more than 4 services to compare.")
        return services


class QuoteRequestForm(ServiceInquiryForm):
    """Extended form specifically for quote requests"""
    
    URGENCY_CHOICES = [
        ('low', 'Standard (2-4 weeks)'),
        ('medium', 'Urgent (1-2 weeks)'),
        ('high', 'Critical (Less than 1 week)'),
    ]
    
    urgency = forms.ChoiceField(
        choices=URGENCY_CHOICES,
        required=False,
        help_text="How quickly do you need this project completed?"
    )
    
    existing_data = forms.BooleanField(
        required=False,
        label="Do you have existing survey data or GIS datasets?",
        help_text="This can affect project timeline and cost"
    )
    
    site_access = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        label="Site access information",
        help_text="Any restrictions, permissions needed, or access challenges?"
    )

    class Meta(ServiceInquiryForm.Meta):
        fields = ServiceInquiryForm.Meta.fields + ['urgency', 'existing_data', 'site_access']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Update layout for quote form
        self.helper.layout = Layout(
            Fieldset(
                'Contact Information',
                Row(
                    Column('name', css_class='form-group col-md-6'),
                    Column('email', css_class='form-group col-md-6'),
                ),
                Row(
                    Column('phone', css_class='form-group col-md-6'),
                    Column('organization', css_class='form-group col-md-6'),
                ),
            ),
            Fieldset(
                'Project Details',
                'service',
                'project_description',
                Row(
                    Column('budget_range', css_class='form-group col-md-6'),
                    Column('timeline', css_class='form-group col-md-6'),
                ),
                Row(
                    Column('location', css_class='form-group col-md-6'),
                    Column('urgency', css_class='form-group col-md-6'),
                ),
            ),
            Fieldset(
                'Additional Information',
                'existing_data',
                'site_access',
            ),
            FormActions(
                Submit('submit', 'Request Detailed Quote', css_class='btn btn-primary btn-lg'),
                HTML('<p class="text-muted mt-2">We will provide a detailed quote within 24 hours during business hours.</p>')
            )
        )


class ServiceFeedbackForm(forms.Form):
    """Form for service feedback and suggestions"""
    
    FEEDBACK_TYPE_CHOICES = [
        ('general', 'General Feedback'),
        ('service_suggestion', 'Service Suggestion'),
        ('improvement', 'Service Improvement'),
        ('complaint', 'Complaint'),
        ('compliment', 'Compliment'),
    ]
    
    RATING_CHOICES = [
        (5, 'Excellent'),
        (4, 'Very Good'),
        (3, 'Good'),
        (2, 'Fair'),
        (1, 'Poor'),
    ]
    
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        required=False,
        help_text="Select the service this feedback relates to (optional)"
    )
    feedback_type = forms.ChoiceField(choices=FEEDBACK_TYPE_CHOICES)
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        required=False,
        help_text="Rate your experience (optional)"
    )
    subject = forms.CharField(max_length=200)
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        help_text="Please provide detailed feedback"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
            ),
            Row(
                Column('service', css_class='form-group col-md-6'),
                Column('feedback_type', css_class='form-group col-md-6'),
            ),
            Row(
                Column('rating', css_class='form-group col-md-6'),
                Column('subject', css_class='form-group col-md-6'),
            ),
            'message',
            Submit('submit', 'Send Feedback', css_class='btn btn-primary')
        )