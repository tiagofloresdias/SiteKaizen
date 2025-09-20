"""
Views para o sistema de franquias
"""
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import uuid
import re
from .models import FranchiseApplication, FranchiseTouchpoint, FranchiseDocument


def validate_cpf(cpf):
    """Valida CPF"""
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    if len(cpf) != 11:
        return False
    
    if cpf == cpf[0] * 11:
        return False
    
    # Validação do primeiro dígito
    sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digit1 = 11 - (sum1 % 11)
    if digit1 >= 10:
        digit1 = 0
    
    if int(cpf[9]) != digit1:
        return False
    
    # Validação do segundo dígito
    sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digit2 = 11 - (sum2 % 11)
    if digit2 >= 10:
        digit2 = 0
    
    return int(cpf[10]) == digit2


def validate_phone(phone):
    """Valida telefone brasileiro"""
    pattern = r'^\(\d{2}\)\s\d{4,5}-\d{4}$'
    return bool(re.match(pattern, phone))


def validate_cep(cep):
    """Valida CEP brasileiro"""
    pattern = r'^\d{5}-\d{3}$'
    return bool(re.match(pattern, cep))


@csrf_exempt
@require_POST
def franchise_step1(request):
    """
    Step 1: Dados pessoais
    """
    try:
        data = json.loads(request.body)
        
        # Validações
        required_fields = ['full_name', 'email', 'phone', 'cpf', 'rg', 'birth_date', 'marital_status']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False, 
                    'error': f'Campo obrigatório: {field}',
                    'field': field
                }, status=400)
        
        # Validação de email
        try:
            validate_email(data['email'])
        except ValidationError:
            return JsonResponse({
                'success': False,
                'error': 'E-mail inválido',
                'field': 'email'
            }, status=400)
        
        # Validação de CPF
        if not validate_cpf(data['cpf']):
            return JsonResponse({
                'success': False,
                'error': 'CPF inválido',
                'field': 'cpf'
            }, status=400)
        
        # Validação de telefone
        if not validate_phone(data['phone']):
            return JsonResponse({
                'success': False,
                'error': 'Telefone inválido. Use o formato (11) 99999-9999',
                'field': 'phone'
            }, status=400)
        
        # Validação de CEP
        if data.get('zipcode') and not validate_cep(data['zipcode']):
            return JsonResponse({
                'success': False,
                'error': 'CEP inválido. Use o formato 00000-000',
                'field': 'zipcode'
            }, status=400)
        
        # Criar ou atualizar aplicação
        application_id = data.get('application_id')
        if application_id:
            try:
                application = FranchiseApplication.objects.get(id=application_id)
            except FranchiseApplication.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Aplicação não encontrada'
                }, status=404)
        else:
            application = FranchiseApplication()
        
        # Preencher dados pessoais
        application.full_name = data['full_name']
        application.email = data['email']
        application.phone = data['phone']
        application.cpf = data['cpf']
        application.rg = data['rg']
        application.birth_date = data['birth_date']
        application.marital_status = data['marital_status']
        application.nationality = data.get('nationality', 'Brasileira')
        application.address = data.get('address', '')
        application.city = data.get('city', '')
        application.state = data.get('state', '')
        application.zipcode = data.get('zipcode', '')
        
        # Dados de tracking
        application.utm_source = data.get('utm_source', '')
        application.utm_medium = data.get('utm_medium', '')
        application.utm_campaign = data.get('utm_campaign', '')
        application.utm_term = data.get('utm_term', '')
        application.utm_content = data.get('utm_content', '')
        application.referrer = data.get('referrer', '')
        application.landing_page = data.get('landing_page', request.META.get('HTTP_REFERER', ''))
        application.user_agent = request.META.get('HTTP_USER_AGENT', '')
        application.ip_address = request.META.get('REMOTE_ADDR')
        application.session_id = data.get('session_id', '')
        
        application.save()
        
        # Criar touchpoint
        FranchiseTouchpoint.objects.create(
            application=application,
            event_type='step1_complete',
            step_number=1,
            event_data=data,
            page_url=request.META.get('HTTP_REFERER', ''),
            timestamp=timezone.now()
        )
        
        return JsonResponse({
            'success': True,
            'application_id': str(application.id),
            'message': 'Dados pessoais salvos com sucesso!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Requisição inválida'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_POST
def franchise_step2(request):
    """
    Step 2: Perfil profissional
    """
    try:
        data = json.loads(request.body)
        application_id = data.get('application_id')
        
        if not application_id:
            return JsonResponse({
                'success': False,
                'error': 'ID da aplicação é obrigatório'
            }, status=400)
        
        try:
            application = FranchiseApplication.objects.get(id=application_id)
        except FranchiseApplication.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Aplicação não encontrada'
            }, status=404)
        
        # Validações
        required_fields = ['profession', 'experience_years', 'education_level', 'management_experience', 'sales_experience', 'marketing_experience']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'Campo obrigatório: {field}',
                    'field': field
                }, status=400)
        
        # Preencher dados profissionais
        application.profession = data['profession']
        application.current_company = data.get('current_company', '')
        application.current_position = data.get('current_position', '')
        application.experience_years = data['experience_years']
        application.education_level = data['education_level']
        application.management_experience = data['management_experience']
        application.sales_experience = data['sales_experience']
        application.marketing_experience = data['marketing_experience']
        
        application.save()
        
        # Criar touchpoint
        FranchiseTouchpoint.objects.create(
            application=application,
            event_type='step2_complete',
            step_number=2,
            event_data=data,
            page_url=request.META.get('HTTP_REFERER', ''),
            timestamp=timezone.now()
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Perfil profissional salvo com sucesso!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Requisição inválida'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_POST
def franchise_step3(request):
    """
    Step 3: Investimento e localização
    """
    try:
        data = json.loads(request.body)
        application_id = data.get('application_id')
        
        if not application_id:
            return JsonResponse({
                'success': False,
                'error': 'ID da aplicação é obrigatório'
            }, status=400)
        
        try:
            application = FranchiseApplication.objects.get(id=application_id)
        except FranchiseApplication.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Aplicação não encontrada'
            }, status=404)
        
        # Validações
        required_fields = ['investment_capacity', 'preferred_city', 'preferred_state', 'expected_start_date', 'team_size', 'business_goals', 'why_franchise', 'available_time', 'risk_tolerance']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'error': f'Campo obrigatório: {field}',
                    'field': field
                }, status=400)
        
        # Preencher dados de investimento e localização
        application.investment_capacity = data['investment_capacity']
        application.preferred_city = data['preferred_city']
        application.preferred_state = data['preferred_state']
        application.preferred_region = data.get('preferred_region', '')
        application.expected_start_date = data['expected_start_date']
        application.team_size = data['team_size']
        application.target_market = data.get('target_market', '')
        application.business_goals = data['business_goals']
        application.why_franchise = data['why_franchise']
        application.expected_revenue = data.get('expected_revenue')
        application.available_time = data['available_time']
        application.risk_tolerance = data['risk_tolerance']
        application.references = data.get('references', '')
        
        application.save()
        
        # Criar touchpoint
        FranchiseTouchpoint.objects.create(
            application=application,
            event_type='step3_complete',
            step_number=3,
            event_data=data,
            page_url=request.META.get('HTTP_REFERER', ''),
            timestamp=timezone.now()
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Informações de investimento salvas com sucesso!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Requisição inválida'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_POST
def franchise_step4(request):
    """
    Step 4: Documentação
    """
    try:
        data = json.loads(request.body)
        application_id = data.get('application_id')
        
        if not application_id:
            return JsonResponse({
                'success': False,
                'error': 'ID da aplicação é obrigatório'
            }, status=400)
        
        try:
            application = FranchiseApplication.objects.get(id=application_id)
        except FranchiseApplication.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Aplicação não encontrada'
            }, status=404)
        
        # Processar uploads de documentos se houver
        documents_uploaded = 0
        if 'documents' in data:
            for doc_data in data['documents']:
                if doc_data.get('file_content') and doc_data.get('filename'):
                    # Simular upload de arquivo (em produção, usar request.FILES)
                    file_content = doc_data['file_content']
                    filename = doc_data['filename']
                    file_type = doc_data.get('file_type', 'other')
                    
                    # Criar documento
                    FranchiseDocument.objects.create(
                        application=application,
                        document_type=file_type,
                        file=ContentFile(file_content.encode(), name=filename),
                        original_filename=filename,
                        file_size=len(file_content),
                        mime_type=doc_data.get('mime_type', 'application/octet-stream')
                    )
                    documents_uploaded += 1
        
        # Criar touchpoint
        FranchiseTouchpoint.objects.create(
            application=application,
            event_type='step4_complete',
            step_number=4,
            event_data={
                'documents_uploaded': documents_uploaded,
                'total_documents': len(data.get('documents', []))
            },
            page_url=request.META.get('HTTP_REFERER', ''),
            timestamp=timezone.now()
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Documentos processados com sucesso!',
            'documents_uploaded': documents_uploaded
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Requisição inválida'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_POST
def franchise_step5(request):
    """
    Step 5: Agendamento
    """
    try:
        data = json.loads(request.body)
        application_id = data.get('application_id')
        
        if not application_id:
            return JsonResponse({
                'success': False,
                'error': 'ID da aplicação é obrigatório'
            }, status=400)
        
        try:
            application = FranchiseApplication.objects.get(id=application_id)
        except FranchiseApplication.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Aplicação não encontrada'
            }, status=404)
        
        # Marcar reunião como agendada
        application.meeting_scheduled = True
        application.meeting_date = data.get('meeting_date')
        application.meeting_notes = data.get('meeting_notes', '')
        application.status = 'scheduled'
        application.save()
        
        # Criar touchpoint
        FranchiseTouchpoint.objects.create(
            application=application,
            event_type='meeting_scheduled',
            step_number=5,
            event_data=data,
            page_url=request.META.get('HTTP_REFERER', ''),
            timestamp=timezone.now()
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Reunião agendada com sucesso!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Requisição inválida'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_POST
def franchise_submit(request):
    """
    Finalizar e enviar aplicação
    """
    try:
        data = json.loads(request.body)
        application_id = data.get('application_id')
        
        if not application_id:
            return JsonResponse({
                'success': False,
                'error': 'ID da aplicação é obrigatório'
            }, status=400)
        
        try:
            application = FranchiseApplication.objects.get(id=application_id)
        except FranchiseApplication.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Aplicação não encontrada'
            }, status=404)
        
        # Marcar como enviada
        application.status = 'submitted'
        application.submitted_at = timezone.now()
        application.save()
        
        # Criar touchpoint
        FranchiseTouchpoint.objects.create(
            application=application,
            event_type='application_submitted',
            step_number=6,
            event_data=data,
            page_url=request.META.get('HTTP_REFERER', ''),
            timestamp=timezone.now()
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Aplicação enviada com sucesso!',
            'application_number': application.application_number
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Requisição inválida'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_POST
def franchise_touchpoint(request):
    """
    Registrar touchpoint
    """
    try:
        data = json.loads(request.body)
        application_id = data.get('application_id')
        event_type = data.get('event_type')
        
        if not application_id or not event_type:
            return JsonResponse({
                'success': False,
                'error': 'application_id e event_type são obrigatórios'
            }, status=400)
        
        try:
            application = FranchiseApplication.objects.get(id=application_id)
        except FranchiseApplication.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Aplicação não encontrada'
            }, status=404)
        
        # Criar touchpoint
        touchpoint = FranchiseTouchpoint.objects.create(
            application=application,
            event_type=event_type,
            event_data=data.get('event_data', {}),
            step_number=data.get('step_number'),
            page_url=data.get('page_url', request.META.get('HTTP_REFERER', '')),
            timestamp=timezone.now()
        )
        
        return JsonResponse({
            'success': True,
            'touchpoint_id': touchpoint.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Requisição inválida'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

