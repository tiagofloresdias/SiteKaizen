from django.shortcuts import render
from django.core.paginator import Paginator
from wagtail.models import Page
from taggit.models import Tag as TaggitTag
from .models import BlogPage, BlogIndexPage, BlogCategory


def blog_index(request):
    """
    View para listar todos os posts do blog
    """
    blog_index = BlogIndexPage.objects.first()
    if not blog_index:
        return render(request, 'blog/blog_index.html', {'blogpages': []})
    
    posts = BlogPage.objects.live().order_by('-date')
    
    # Paginação
    paginator = Paginator(posts, 12)  # 12 posts por página (grid 3x4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Categorias para o filtro
    categories = BlogCategory.objects.all().order_by('name')
    popular_tags = TaggitTag.objects.all()[:10]
    
    context = {
        'blog_index': blog_index,
        'page_obj': page_obj,
        'blogpages': page_obj,  # Para compatibilidade com o template
        'categories': categories,
        'popular_tags': popular_tags,
    }
    
    return render(request, 'blog/blog_index.html', context)


def blog_category(request, slug):
    """
    Lista posts por categoria em rota SEO: /categorias/<slug>/
    """
    try:
        category = BlogCategory.objects.get(slug=slug)
    except BlogCategory.DoesNotExist:
        category = None

    posts = BlogPage.objects.live().filter(categories__slug=slug).order_by('-date')

    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = BlogCategory.objects.all().order_by('name')
    popular_tags = TaggitTag.objects.all()[:10]

    context = {
        'blog_index': BlogIndexPage.objects.first(),
        'page_obj': page_obj,
        'blogpages': page_obj,
        'categories': categories,
        'popular_tags': popular_tags,
        'current_category': category,
    }
    return render(request, 'blog/blog_index.html', context)


def blog_tag(request, slug):
    """
    Lista posts por tag em rota SEO: /tags/<slug>/
    """
    try:
        tag = TaggitTag.objects.get(slug=slug)
    except TaggitTag.DoesNotExist:
        tag = None

    posts = BlogPage.objects.live().filter(tags__slug=slug).order_by('-date')

    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = BlogCategory.objects.all().order_by('name')
    popular_tags = TaggitTag.objects.all()[:10]

    context = {
        'blog_index': BlogIndexPage.objects.first(),
        'page_obj': page_obj,
        'blogpages': page_obj,
        'categories': categories,
        'popular_tags': popular_tags,
        'current_tag': tag,
    }
    return render(request, 'blog/blog_index.html', context)


def blog_post(request, slug):
    """
    View para exibir um post individual do blog
    """
    try:
        post = BlogPage.objects.get(slug=slug)
        context = {
            'post': post,
        }
        return render(request, 'blog/blog_post.html', context)
    except BlogPage.DoesNotExist:
        return render(request, '404.html', status=404)
