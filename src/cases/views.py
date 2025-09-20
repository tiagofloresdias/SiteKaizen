from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Case, CaseIndexPage, CaseDetailPage


def case_list_api(request):
    """API para listar cases (para AJAX/filtros)"""
    category = request.GET.get('category')
    cases = Case.objects.filter(is_published=True)
    
    if category:
        cases = cases.filter(category=category)
    
    cases_data = []
    for case in cases:
        cases_data.append({
            'id': case.id,
            'title': case.title,
            'client_name': case.client_name,
            'slug': case.slug,
            'category': case.get_category_display(),
            'short_description': case.short_description,
            'main_metric_value': case.main_metric_value,
            'main_metric_description': case.main_metric_description,
            'hero_image_url': case.hero_image.file.url if case.hero_image else None,
            'client_logo_url': case.client_logo.file.url if case.client_logo else None,
            'is_featured': case.is_featured,
            'created_at': case.created_at.strftime('%d/%m/%Y'),
        })
    
    return JsonResponse({
        'cases': cases_data,
        'total': len(cases_data)
    })


def case_detail_api(request, slug):
    """API para detalhes de um case específico"""
    try:
        case = get_object_or_404(Case, slug=slug, is_published=True)
        
        case_data = {
            'id': case.id,
            'title': case.title,
            'client_name': case.client_name,
            'slug': case.slug,
            'category': case.get_category_display(),
            'short_description': case.short_description,
            'challenge': case.challenge,
            'solution': case.solution,
            'results': case.results,
            'main_metric_value': case.main_metric_value,
            'main_metric_description': case.main_metric_description,
            'hero_image_url': case.hero_image.file.url if case.hero_image else None,
            'client_logo_url': case.client_logo.file.url if case.client_logo else None,
            'is_featured': case.is_featured,
            'created_at': case.created_at.strftime('%d/%m/%Y'),
            'updated_at': case.updated_at.strftime('%d/%m/%Y'),
        }
        
        return JsonResponse({
            'case': case_data,
            'success': True
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'success': False
        }, status=404)