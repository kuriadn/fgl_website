from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.middleware.csrf import get_token
from taggit.models import Tag
from .models import BlogPost, BlogCategory, BlogComment, BlogSubscriber, ReadingHistory
from .forms import CommentForm, SubscriptionForm, BlogSearchForm
import json


def blog_list(request):
    """Main blog listing page with filtering and search"""
    posts = BlogPost.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags')
    
    # Search functionality
    search_form = BlogSearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('q')
        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
    
    # Category filtering
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(BlogCategory, slug=category_slug, is_active=True)
        posts = posts.filter(category=selected_category)
    
    # Tag filtering
    tag_slug = request.GET.get('tag')
    selected_tag = None
    if tag_slug:
        selected_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=selected_tag)
    
    # Featured posts for hero section
    featured_posts = BlogPost.objects.filter(
        status='published',
        featured__in=['hero', 'grid']
    ).select_related('category', 'author')[:3]
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Sidebar data
    categories = BlogCategory.objects.filter(is_active=True)
    
    popular_posts = BlogPost.objects.filter(status='published').order_by('-view_count')[:5]
    recent_posts = BlogPost.objects.filter(status='published').order_by('-published_at')[:5]
    popular_tags = Tag.objects.filter(
        taggit_taggeditem_items__content_type__model='blogpost'
    ).annotate(
        post_count=Count('taggit_taggeditem_items')
    ).order_by('-post_count')[:10]
    
    context = {
        'page_obj': page_obj,
        'featured_posts': featured_posts,
        'categories': categories,
        'popular_posts': popular_posts,
        'recent_posts': recent_posts,
        'popular_tags': popular_tags,
        'selected_category': selected_category,
        'selected_tag': selected_tag,
        'search_form': search_form,
        'subscription_form': SubscriptionForm(),
        'meta_title': 'Insights & Innovation - Fayvad Geosolutions Blog',
        'meta_description': 'Expert insights on GIS, land surveying, drone mapping, and geospatial technology. Stay updated with the latest innovations in geospatial solutions.',
    }
    
    return render(request, 'blog/list.html', context)


def blog_detail(request, slug):
    """Individual blog post detail page"""
    post = get_object_or_404(
        BlogPost.objects.select_related('category', 'author').prefetch_related('tags'),
        slug=slug,
        status='published'
    )
    
    # Increment view count
    post.increment_view_count()
    
    # Get approved comments
    comments = post.comments.filter(is_approved=True).order_by('created_at')
    
    # Related posts based on category and tags
    related_posts = BlogPost.objects.filter(
        Q(category=post.category) | Q(tags__in=post.tags.all()),
        status='published'
    ).exclude(pk=post.pk).distinct().select_related('category')[:4]
    
    # Comment form handling
    comment_form = CommentForm()
    if request.method == 'POST' and 'comment_submit' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been submitted for review.')
            return redirect('blog:detail', slug=post.slug)
    
    # # Track reading behavior
    # try:
    #     # Ensure session exists
    #     if not request.session.session_key:
    #         request.session.save()
    #     if request.session.session_key:
    #         ReadingHistory.objects.get_or_create(
    #             session_key=request.session.session_key,
    #             post=post
    #         )
    # except Exception:
    #     # If session handling fails, continue without tracking
    #     pass
    
    # Navigation posts
    next_post = post.next_post
    previous_post = post.previous_post
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
        'next_post': next_post,
        'previous_post': previous_post,
        'meta_title': post.meta_title or post.title,
        'meta_description': post.meta_description or post.excerpt,
        'meta_keywords': post.meta_keywords,
    }
    
    return render(request, 'blog/detail.html', context)


def category_detail(request, slug):
    """Category archive page"""
    category = get_object_or_404(BlogCategory, slug=slug, is_active=True)
    
    posts = BlogPost.objects.filter(
        category=category,
        status='published'
    ).select_related('author').prefetch_related('tags')
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'meta_title': f'{category.name} - Fayvad Geosolutions Blog',
        'meta_description': category.description or f'All posts in {category.name} category.',
    }
    
    return render(request, 'blog/category.html', context)


def tag_detail(request, slug):
    """Tag archive page"""
    tag = get_object_or_404(Tag, slug=slug)
    
    posts = BlogPost.objects.filter(
        tags=tag,
        status='published'
    ).select_related('category', 'author')
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
        'post_count': posts.count(),
        'meta_title': f'#{tag.name} - Fayvad Geosolutions Blog',
        'meta_description': f'All blog posts tagged with {tag.name}.',
    }
    
    return render(request, 'blog/tag.html', context)


def archive(request):
    """Blog archive by year and month"""
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    posts = BlogPost.objects.filter(status='published')
    
    if year:
        try:
            year = int(year)
            posts = posts.filter(published_at__year=year)
            if month:
                month = int(month)
                posts = posts.filter(published_at__month=month)
        except (ValueError, TypeError):
            # Invalid year/month parameters
            pass
    
    # Archive stats
    archive_stats = BlogPost.objects.filter(
        status='published'
    ).extra(
        select={'year': 'EXTRACT(year FROM published_at)', 'month': 'EXTRACT(month FROM published_at)'}
    ).values('year', 'month').annotate(count=Count('id')).order_by('-year', '-month')
    
    paginator = Paginator(posts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'archive_stats': archive_stats,
        'selected_year': year,
        'selected_month': month,
        'meta_title': 'Blog Archive - Fayvad Geosolutions',
        'meta_description': 'Browse our complete archive of geospatial insights and technology articles.',
    }
    
    return render(request, 'blog/archive.html', context)


def search(request):
    """Blog search with filters"""
    form = BlogSearchForm(request.GET)
    posts = BlogPost.objects.none()
    query = None
    
    if form.is_valid():
        query = form.cleaned_data.get('q')
        if query:
            posts = BlogPost.objects.filter(
                Q(title__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query) |
                Q(category__name__icontains=query)
            ).filter(status='published').distinct().select_related('category', 'author')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'query': query,
        'total_results': posts.count() if query else 0,
        'meta_title': f'Search Results for "{query}"' if query else 'Blog Search',
        'meta_description': f'Search results for "{query}" in Fayvad Geosolutions blog.' if query else 'Search our blog for geospatial insights and technology articles.',
    }
    
    return render(request, 'blog/search.html', context)


@require_http_methods(["POST"])
def subscribe(request):
    """Handle newsletter subscription via AJAX"""
    try:
        data = json.loads(request.body)
        form = SubscriptionForm(data)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data.get('name', '')
            
            subscriber, created = BlogSubscriber.objects.get_or_create(
                email=email,
                defaults={'name': name}
            )
            
            if created:
                return JsonResponse({
                    'success': True,
                    'message': 'Successfully subscribed to our blog updates!'
                })
            else:
                if subscriber.is_active:
                    return JsonResponse({
                        'success': False,
                        'message': 'This email is already subscribed.'
                    })
                else:
                    subscriber.is_active = True
                    subscriber.save()
                    return JsonResponse({
                        'success': True,
                        'message': 'Your subscription has been reactivated!'
                    })
        else:
            errors = form.errors.get('email', ['Please enter a valid email address.'])
            return JsonResponse({
                'success': False,
                'message': errors[0]
            })
    
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({
            'success': False,
            'message': 'Invalid request data.'
        })
    except Exception:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        })


@require_http_methods(["POST"])
def track_reading_time(request, slug):
    """Track time spent reading a post"""
    try:
        post = get_object_or_404(BlogPost, slug=slug, status='published')
        data = json.loads(request.body)
        time_spent = int(data.get('time_spent', 0))
        
        # Validate time_spent is reasonable (0-7200 seconds = 2 hours max)
        if not 0 <= time_spent <= 7200:
            return JsonResponse({'success': False})
        
        # try:
        #     if not request.session.session_key:
        #         request.session.save()
            
        #     if request.session.session_key:
        #         reading_history, created = ReadingHistory.objects.get_or_create(
        #             session_key=request.session.session_key,
        #             post=post
        #         )
        # except Exception:
        #     pass 
        
        reading_history.time_spent = max(reading_history.time_spent, time_spent)
        reading_history.save()
        
        return JsonResponse({'success': True})
    
    except (json.JSONDecodeError, ValueError, TypeError):
        return JsonResponse({'success': False})
    except Exception:
        return JsonResponse({'success': False})