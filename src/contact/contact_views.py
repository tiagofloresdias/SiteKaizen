from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
import json
import re

from .models import ContactMessage


def contact_page(request):
    """
    View para a página de contato principal
    """
    if request.method == 'POST':
        return handle_contact_form(request)
    
    return render(request, 'contact/contact_page.html', {
        'request': request
    })


@csrf_exempt
@require_http_methods(["POST"])
def handle_contact_form(request):
    """
    Processa o formulário de contato
    """
    try:
        # Capturar dados do formulário
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()
        faturamento = request.POST.get('faturamento', '').strip()
        area = request.POST.get('area', '').strip()
        website = request.POST.get('website', '').strip()
        
        # Validações obrigatórias
        if not name:
            messages.error(request, 'Nome é obrigatório.')
            return redirect('/contato/')
        
        if not email:
            messages.error(request, 'E-mail é obrigatório.')
            return redirect('/contato/')
        
        if not phone:
            messages.error(request, 'WhatsApp é obrigatório.')
            return redirect('/contato/')
        
        if not message:
            messages.error(request, 'Mensagem é obrigatória.')
            return redirect('/contato/')
        
        if not faturamento:
            messages.error(request, 'Faturamento é obrigatório.')
            return redirect('/contato/')
        
        if not area:
            messages.error(request, 'Área é obrigatória.')
            return redirect('/contato/')
        
        # Validar formato do email
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'E-mail inválido.')
            return redirect('/contato/')
        
        # Validar formato do telefone
        import re
        phone_clean = re.sub(r'\D', '', phone)
        if len(phone_clean) < 10 or len(phone_clean) > 11:
            messages.error(request, 'WhatsApp inválido. Use o formato (XX) XXXXX-XXXX.')
            return redirect('/contato/')
        
        # Validar e formatar URL se fornecida
        if website:
            if not website.startswith(('http://', 'https://')):
                website = 'http://' + website
            try:
                from urllib.parse import urlparse
                parsed = urlparse(website)
                if not parsed.netloc:
                    messages.error(request, 'URL inválida.')
                    return redirect('/contato/')
            except:
                messages.error(request, 'URL inválida.')
                return redirect('/contato/')
        
        # Capturar UTM parameters
        utm_source = request.POST.get('utm_source', '')
        utm_medium = request.POST.get('utm_medium', '')
        utm_campaign = request.POST.get('utm_campaign', '')
        utm_term = request.POST.get('utm_term', '')
        utm_content = request.POST.get('utm_content', '')
        
        # Capturar outros dados de tracking
        subject_category = request.POST.get('subject_category', 'formulario-principal')
        captation_means = request.POST.get('captation_means', '[KAIZEN] Site')
        customer_domain = request.POST.get('customer_domain', '')
        
        # Criar mensagem de contato
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            company=f"{area} - {faturamento}",
            message=f"""
Mensagem: {message}

Área: {area}
Faturamento: {faturamento}
Website: {website or 'Não informado'}

Categoria: {subject_category}
Meio de Captação: {captation_means}
Domínio: {customer_domain}
            """,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            page_url=request.META.get('HTTP_REFERER', ''),
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
            utm_term=utm_term,
            utm_content=utm_content,
        )
        
        # Enviar email de notificação (se configurado)
        if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
            try:
                send_mail(
                    subject=f'[KAIZEN] Novo contato: {name}',
                    message=f"""
Novo contato recebido:

Nome: {name}
Email: {email}
Telefone: {phone}
Área: {area}
Faturamento: {faturamento}
Website: {website or 'Não informado'}

Mensagem:
{message}

UTM Source: {utm_source}
UTM Medium: {utm_medium}
UTM Campaign: {utm_campaign}
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Erro ao enviar email: {e}")
        
        # Sucesso
        messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contato em breve.')
        return redirect('/contato/')
        
    except Exception as e:
        print(f"Erro no formulário de contato: {e}")
        messages.error(request, 'Ocorreu um erro ao enviar sua mensagem. Tente novamente.')
        return redirect('/contato/')


@csrf_exempt
@require_http_methods(["POST"])
def contact_ajax(request):
    """
    View AJAX para formulário de contato
    """
    try:
        # Aceita tanto JSON quanto form-data (FormData)
        if request.META.get('CONTENT_TYPE', '').startswith('application/json'):
            data = json.loads(request.body or b'{}')
        else:
            data = request.POST.dict()
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        message = data.get('message', '').strip()
        faturamento = data.get('faturamento', '').strip()
        area = data.get('area', '').strip()
        website = data.get('website', '').strip()
        
        # Validações
        if not all([name, email, phone, message, faturamento, area]):
            return JsonResponse({
                'success': False, 
                'message': 'Todos os campos obrigatórios devem ser preenchidos'
            }, status=400)
        
        # Validar nome
        if len(name) < 2:
            return JsonResponse({
                'success': False, 
                'message': 'Nome deve ter pelo menos 2 caracteres'
            }, status=400)
        
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', name):
            return JsonResponse({
                'success': False, 
                'message': 'Nome deve conter apenas letras'
            }, status=400)
        
        # Validar email
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'success': False, 
                'message': 'E-mail inválido'
            }, status=400)
        
        # Validar telefone
        phone_clean = re.sub(r'\D', '', phone)
        if len(phone_clean) < 10 or len(phone_clean) > 11:
            return JsonResponse({
                'success': False, 
                'message': 'WhatsApp inválido. Use o formato (XX) XXXXX-XXXX'
            }, status=400)
        
        # Validar mensagem
        if len(message) < 10:
            return JsonResponse({
                'success': False, 
                'message': 'Mensagem deve ter pelo menos 10 caracteres'
            }, status=400)
        
        # Validar e formatar URL se fornecida
        if website:
            if not website.startswith(('http://', 'https://')):
                website = 'http://' + website
            try:
                from urllib.parse import urlparse
                parsed = urlparse(website)
                if not parsed.netloc:
                    return JsonResponse({'success': False, 'message': 'URL inválida'}, status=400)
            except Exception:
                return JsonResponse({'success': False, 'message': 'URL inválida'}, status=400)
        
        # Capturar UTM parameters
        utm_source = data.get('utm_source', '')
        utm_medium = data.get('utm_medium', '')
        utm_campaign = data.get('utm_campaign', '')
        utm_term = data.get('utm_term', '')
        utm_content = data.get('utm_content', '')
        
        # Criar mensagem
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            company=f"{area} - {faturamento}",
            message=f"""
Mensagem: {message}

Área: {area}
Faturamento: {faturamento}
Website: {website or 'Não informado'}
            """,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            page_url=request.META.get('HTTP_REFERER', ''),
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
            utm_term=utm_term,
            utm_content=utm_content,
        )
        
        return JsonResponse({'success': True, 'message': 'Mensagem enviada com sucesso! Entraremos em contato em breve.'})
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Dados inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': 'Erro interno do servidor'
        }, status=500)
