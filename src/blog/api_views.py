from django.http import JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .models import BlogPage, BlogIndexPage
import json


@require_GET
def load_more_posts(request):
    """
    API endpoint para carregar mais posts via AJAX
    """
    try:
        page = int(request.GET.get('page', 1))
        category = request.GET.get('category', '')
        search = request.GET.get('search', '')
        
        # Buscar posts
        posts = BlogPage.objects.live().order_by('-date')
        
        # Filtrar por categoria se especificada
        if category:
            posts = posts.filter(categories__slug=category)
        
        # Filtrar por busca se especificada
        if search:
            posts = posts.filter(title__icontains=search)
        
        # Paginação
        paginator = Paginator(posts, 6)  # 6 posts por página
        page_obj = paginator.get_page(page)
        
        # Renderizar HTML dos posts
        posts_html = render_to_string('blog/partials/blog_posts.html', {
            'blogpages': page_obj,
            'request': request
        })
        
        return JsonResponse({
            'success': True,
            'html': posts_html,
            'has_next': page_obj.has_next(),
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_posts': paginator.count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_GET
def search_posts(request):
    """
    API endpoint para buscar posts
    """
    try:
        search_query = request.GET.get('q', '').strip()
        category = request.GET.get('category', '')
        
        if not search_query:
            return JsonResponse({
                'success': False,
                'error': 'Query de busca é obrigatória'
            }, status=400)
        
        # Buscar posts
        posts = BlogPage.objects.live().filter(
            title__icontains=search_query
        ).order_by('-date')
        
        # Filtrar por categoria se especificada
        if category:
            posts = posts.filter(categories__slug=category)
        
        # Paginação
        paginator = Paginator(posts, 6)
        page_obj = paginator.get_page(1)
        
        # Renderizar HTML dos posts
        posts_html = render_to_string('blog/partials/blog_posts.html', {
            'blogpages': page_obj,
            'request': request
        })
        
        return JsonResponse({
            'success': True,
            'html': posts_html,
            'has_next': page_obj.has_next(),
            'total_posts': paginator.count,
            'search_query': search_query
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_GET
def get_categories(request):
    """
    API endpoint para obter categorias
    """
    try:
        from .models import BlogCategory
        
        categories = BlogCategory.objects.all().order_by('name')
        
        categories_data = []
        for category in categories:
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
                'post_count': BlogPage.objects.live().filter(categories=category).count()
            })
        
        return JsonResponse({
            'success': True,
            'categories': categories_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)