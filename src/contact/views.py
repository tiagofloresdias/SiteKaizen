from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import json

from .models import Newsletter, ContactMessage, ConnectPage


def newsletter_subscribe(request):
    """
    View para processar inscrição no newsletter
    """
    if request.method == 'POST':
        try:
            # Capturar dados do formulário
            email = request.POST.get('email', '').strip()
            name = request.POST.get('name', '').strip()
            source = request.POST.get('source', 'blog_sidebar')
            
            # Validação básica
            if not email:
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({'success': False, 'error': 'Email é obrigatório'}, status=400)
                messages.error(request, 'Email é obrigatório.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            # Validar formato do email
            try:
                validate_email(email)
            except ValidationError:
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({'success': False, 'error': 'Email inválido'}, status=400)
                messages.error(request, 'Email inválido.')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            # Capturar UTM parameters
            utm_source = request.POST.get('utm_source', '')
            utm_medium = request.POST.get('utm_medium', '')
            utm_campaign = request.POST.get('utm_campaign', '')
            utm_term = request.POST.get('utm_term', '')
            utm_content = request.POST.get('utm_content', '')
            
            # Criar ou atualizar newsletter
            newsletter, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={
                    'name': name,
                    'source': source,
                    'page_url': request.META.get('HTTP_REFERER', ''),
                    'ip_address': request.META.get('REMOTE_ADDR'),
                    'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    'utm_source': utm_source,
                    'utm_medium': utm_medium,
                    'utm_campaign': utm_campaign,
                    'utm_term': utm_term,
                    'utm_content': utm_content,
                }
            )
            
            if created:
                # Novo inscrito
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({
                        'success': True, 
                        'message': 'Inscrição realizada com sucesso!',
                        'created': True
                    })
                messages.success(request, 'Inscrição realizada com sucesso! Você receberá nossos insights em breve.')
            else:
                # Já estava inscrito
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({
                        'success': True, 
                        'message': 'Você já estava inscrito no nosso newsletter!',
                        'created': False
                    })
                messages.info(request, 'Você já estava inscrito no nosso newsletter!')
            
            # Redirecionar de volta
            return redirect(request.META.get('HTTP_REFERER', '/'))
            
        except Exception as e:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': False, 'error': 'Erro interno do servidor'}, status=500)
            messages.error(request, 'Ocorreu um erro ao processar sua inscrição. Tente novamente.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # Se não for POST, redirecionar para home
    return redirect('/')


def newsletter_unsubscribe(request, email):
    """
    View para descadastrar do newsletter
    """
    try:
        newsletter = Newsletter.objects.get(email=email, is_active=True)
        newsletter.unsubscribe()
        messages.success(request, 'Descadastro realizado com sucesso!')
    except Newsletter.DoesNotExist:
        messages.error(request, 'Email não encontrado ou já descadastrado.')
    
    return render(request, 'contact/newsletter_unsubscribe.html', {
        'email': email,
        'success': True
    })


@csrf_exempt
@require_http_methods(["POST"])
def newsletter_ajax(request):
    """
    View AJAX para newsletter (para formulários que usam JavaScript)
    """
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        name = data.get('name', '').strip()
        source = data.get('source', 'ajax_form')
        
        # Validação
        if not email:
            return JsonResponse({'success': False, 'error': 'Email é obrigatório'}, status=400)
        
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'error': 'Email inválido'}, status=400)
        
        # Capturar UTM parameters do JavaScript
        utm_source = data.get('utm_source', '')
        utm_medium = data.get('utm_medium', '')
        utm_campaign = data.get('utm_campaign', '')
        utm_term = data.get('utm_term', '')
        utm_content = data.get('utm_content', '')
        
        # Criar newsletter
        newsletter, created = Newsletter.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'source': source,
                'page_url': request.META.get('HTTP_REFERER', ''),
                'ip_address': request.META.get('REMOTE_ADDR'),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'utm_source': utm_source,
                'utm_medium': utm_medium,
                'utm_campaign': utm_campaign,
                'utm_term': utm_term,
                'utm_content': utm_content,
            }
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Inscrição realizada com sucesso!' if created else 'Você já estava inscrito!',
            'created': created
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Dados inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': 'Erro interno do servidor'}, status=500)


def connect_page(request):
    """
    View para a página Conecte-se
    """
    try:
        # Busca a página Conecte-se
        page = ConnectPage.objects.filter(slug='conecte-se', live=True).first()
        if not page:
            # Se não existir, cria uma página padrão
            from wagtail.models import Page
            root_page = Page.objects.filter(slug='home').first()
            if root_page:
                page = ConnectPage(
                    title="Conecte-se",
                    slug="conecte-se",
                    live=True,
                )
                root_page.add_child(instance=page)
                page.save_revision().publish()
        
        return render(request, 'contact/connect_page.html', {
            'page': page,
            'request': request
        })
    except Exception as e:
        # Fallback para uma página simples
        return render(request, 'contact/connect_page.html', {
            'page': None,
            'request': request
        })
