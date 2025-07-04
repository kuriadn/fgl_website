# Generated by Django 4.2.7 on 2025-06-21 19:50

import ckeditor.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Achievement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("date_achieved", models.DateField()),
                ("organization", models.CharField(blank=True, max_length=200)),
                ("is_featured", models.BooleanField(default=False)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["-date_achieved", "order"],
            },
        ),
        migrations.CreateModel(
            name="CompanyInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(default="Fayvad Geosolutions Ltd", max_length=200),
                ),
                (
                    "tagline",
                    models.CharField(default="PhD-Level GIS Expertise", max_length=300),
                ),
                ("description", ckeditor.fields.RichTextField(blank=True)),
                ("phone", models.CharField(default="+254 769 069 640", max_length=20)),
                (
                    "email",
                    models.EmailField(default="info@geo.fayvad.com", max_length=254),
                ),
                (
                    "address",
                    models.TextField(
                        default="Grace House 3rd Floor Suite 10, Nkuruma Road, Thika, Kenya"
                    ),
                ),
                (
                    "business_hours",
                    models.TextField(
                        default="Monday - Friday: 8:00 AM - 5:00 PM\nSaturday: By Appointment\nSunday: Emergency Only"
                    ),
                ),
                ("linkedin_url", models.URLField(blank=True)),
                ("twitter_url", models.URLField(blank=True)),
                ("facebook_url", models.URLField(blank=True)),
                ("meta_description", models.TextField(blank=True, max_length=160)),
                ("meta_keywords", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "verbose_name": "Company Information",
                "verbose_name_plural": "Company Information",
            },
        ),
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        validators=[django.core.validators.EmailValidator()],
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Phone number must be in format: '+999999999'. Up to 15 digits allowed.",
                                regex="^\\+?1?\\d{9,15}$",
                            )
                        ],
                    ),
                ),
                ("company", models.CharField(blank=True, max_length=200)),
                (
                    "inquiry_type",
                    models.CharField(
                        choices=[
                            ("general", "General Inquiry"),
                            ("quote", "Request Quote"),
                            ("support", "Technical Support"),
                            ("partnership", "Partnership"),
                        ],
                        default="general",
                        max_length=20,
                    ),
                ),
                ("subject", models.CharField(max_length=200)),
                ("message", models.TextField()),
                ("is_read", models.BooleanField(default=False)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="FAQ",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("question", models.CharField(max_length=300)),
                ("answer", ckeditor.fields.RichTextField()),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("general", "General"),
                            ("services", "Services"),
                            ("pricing", "Pricing"),
                            ("technical", "Technical"),
                            ("support", "Support"),
                        ],
                        default="general",
                        max_length=20,
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_published", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "FAQ",
                "verbose_name_plural": "FAQs",
                "ordering": ["category", "order", "question"],
            },
        ),
        migrations.CreateModel(
            name="Newsletter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        unique=True,
                        validators=[django.core.validators.EmailValidator()],
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("confirmed_at", models.DateTimeField(blank=True, null=True)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("content", ckeditor.fields.RichTextField()),
                ("meta_description", models.TextField(blank=True, max_length=160)),
                ("meta_keywords", models.CharField(blank=True, max_length=255)),
                ("is_published", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["order", "title"],
            },
        ),
        migrations.CreateModel(
            name="Testimonial",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("client_name", models.CharField(max_length=200)),
                ("client_title", models.CharField(blank=True, max_length=200)),
                ("client_company", models.CharField(blank=True, max_length=200)),
                ("content", models.TextField()),
                (
                    "rating",
                    models.PositiveIntegerField(
                        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5
                    ),
                ),
                ("project", models.CharField(blank=True, max_length=200)),
                ("is_featured", models.BooleanField(default=False)),
                ("is_published", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["order", "-created_at"],
            },
        ),
    ]
