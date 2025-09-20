"""
Views personalizadas para o projeto Agência Kaizen
Inclui handlers de erro 404 e 500 otimizados para SEO
"""
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


def custom_404(request, exception=None):
    """
    Handler personalizado para erro 404
    Retorna uma página 404 otimizada para SEO
    """
    try:
        # Log do erro 404 para análise
        logger.warning(f"404 Error: {request.path} - User: {request.user} - IP: {request.META.get('REMOTE_ADDR')}")
        
        # Renderizar template 404 personalizado
        context = {
            'request': request,
            'exception': exception,
            'timestamp': timezone.now(),
            'path': request.path,
        }
        
        return render(request, '404.html', context, status=404)
        
    except Exception as e:
        # Se houver erro ao renderizar a página 404, usar fallback
        logger.error(f"Error rendering 404 page: {e}")
        return HttpResponseNotFound(
            render_to_string('404.html', {'request': request}, request=request)
        )


def custom_500(request):
    """
    Handler personalizado para erro 500
    Retorna uma página 500 otimizada para SEO
    """
    try:
        # Log do erro 500 para análise
        logger.error(f"500 Error: {request.path} - User: {request.user} - IP: {request.META.get('REMOTE_ADDR')}")
        
        # Renderizar template 500 personalizado
        context = {
            'request': request,
            'timestamp': timezone.now(),
            'path': request.path,
        }
        
        return render(request, '500.html', context, status=500)
        
    except Exception as e:
        # Se houver erro ao renderizar a página 500, usar fallback
        logger.error(f"Error rendering 500 page: {e}")
        return HttpResponseServerError(
            render_to_string('500.html', {'request': request}, request=request)
        )


def custom_403(request, exception=None):
    """
    Handler personalizado para erro 403 (Forbidden)
    """
    try:
        logger.warning(f"403 Error: {request.path} - User: {request.user} - IP: {request.META.get('REMOTE_ADDR')}")
        
        context = {
            'request': request,
            'exception': exception,
            'timestamp': timezone.now(),
            'path': request.path,
        }
        
        return render(request, '403.html', context, status=403)
        
    except Exception as e:
        logger.error(f"Error rendering 403 page: {e}")
        return HttpResponseNotFound(
            render_to_string('403.html', {'request': request}, request=request)
        )


def custom_400(request, exception=None):
    """
    Handler personalizado para erro 400 (Bad Request)
    """
    try:
        logger.warning(f"400 Error: {request.path} - User: {request.user} - IP: {request.META.get('REMOTE_ADDR')}")
        
        context = {
            'request': request,
            'exception': exception,
            'timestamp': timezone.now(),
            'path': request.path,
        }
        
        return render(request, '400.html', context, status=400)
        
    except Exception as e:
        logger.error(f"Error rendering 400 page: {e}")
        return HttpResponseNotFound(
            render_to_string('400.html', {'request': request}, request=request)
        )

