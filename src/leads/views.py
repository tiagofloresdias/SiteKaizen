from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import json
import logging

from .models import Lead

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class LeadAPIView(View):
    """
    API para gerenciar leads do formulário multi-passo
    """
    
    def post(self, request):
        try:
            # Verificar se é FormData (franqueados) ou JSON (negócios)
            if request.content_type == 'application/x-www-form-urlencoded':
                data = request.POST.dict()
                lead_type = data.get('type', 'business')
            else:
                data = json.loads(request.body)
                lead_type = data.get('type', 'business')
            
            # Se for lead de franquia, usar endpoint específico
            if lead_type == 'franchise_lead':
                return self._handle_franchise_lead(data)
            
            # Lógica original para leads de negócio
            step = data.get('step')
            
            if step == '1':
                return self._handle_step1(data)
            elif step == '2':
                return self._handle_step2(data)
            elif step == '3':
                return self._handle_step3(data)
            else:
                return JsonResponse({'error': 'Step inválido'}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        except Exception as e:
            logger.error(f"Erro na API de leads: {str(e)}")
            return JsonResponse({'error': 'Erro interno do servidor'}, status=500)
    
    def _handle_step1(self, data):
        """Passo 1: Salvar dados básicos"""
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        
        if not all([name, email, phone]):
            return JsonResponse({'error': 'Todos os campos são obrigatórios'}, status=400)
        
        # Criar ou atualizar lead
        lead, created = Lead.objects.get_or_create(
            email=email,
            defaults={
                'name': name,
                'phone': phone,
                'status': 'step1'
            }
        )
        
        if not created:
            # Atualizar dados existentes
            lead.name = name
            lead.phone = phone
            lead.status = 'step1'
            lead.save()
        
        return JsonResponse({
            'success': True,
            'lead_id': lead.id,
            'message': 'Dados salvos com sucesso!'
        })
    
    def _handle_step2(self, data):
        """Passo 2: Salvar informações do negócio"""
        lead_id = data.get('lead_id')
        monthly_revenue = data.get('monthly_revenue', '')
        business_area = data.get('business_area', '')
        main_challenge = data.get('main_challenge', '').strip()
        website_social = data.get('website_social', '').strip()
        
        if not lead_id:
            return JsonResponse({'error': 'Lead ID é obrigatório'}, status=400)
        
        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            return JsonResponse({'error': 'Lead não encontrado'}, status=404)
        
        # Atualizar dados do negócio
        lead.monthly_revenue = monthly_revenue
        lead.business_area = business_area
        lead.main_challenge = main_challenge
        lead.website_social = website_social
        lead.status = 'step2'
        lead.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Informações do negócio salvas!'
        })
    
    def _handle_step3(self, data):
        """Passo 3: Finalizar lead e enviar email de confirmação"""
        lead_id = data.get('lead_id')
        calendly_event_id = data.get('calendly_event_id', '')
        scheduled_date = data.get('scheduled_date')
        
        if not lead_id:
            return JsonResponse({'error': 'Lead ID é obrigatório'}, status=400)
        
        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            return JsonResponse({'error': 'Lead não encontrado'}, status=404)
        
        # Atualizar dados do agendamento
        lead.calendly_event_id = calendly_event_id
        if scheduled_date:
            from datetime import datetime
            lead.scheduled_date = datetime.fromisoformat(scheduled_date.replace('Z', '+00:00'))
        lead.status = 'completed'
        lead.save()
        
        # Enviar email de confirmação
        try:
            self._send_confirmation_email(lead)
            lead.confirmation_email_sent = True
            lead.save()
        except Exception as e:
            logger.error(f"Erro ao enviar email: {str(e)}")
            # Não falhar o processo por causa do email
        
        return JsonResponse({
            'success': True,
            'message': 'Lead finalizado com sucesso!'
        })
    
    def _handle_franchise_lead(self, data):
        """Processar lead de franqueado completo"""
        try:
            # Dados básicos
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            phone = data.get('phone', '').strip()
            
            # Dados específicos de franqueados
            current_activity = data.get('current_activity', '')
            experience_years = data.get('experience_years', '')
            franchise_timeline = data.get('franchise_timeline', '')
            franchise_type = data.get('franchise_type', '')
            investment_range = data.get('investment_range', '')
            additional_info = data.get('additional_info', '').strip()
            
            if not all([name, email, phone]):
                return JsonResponse({'error': 'Nome, email e telefone são obrigatórios'}, status=400)
            
            # Criar lead de franquia
            lead = Lead.objects.create(
                name=name,
                email=email,
                phone=phone,
                lead_type='franchise',
                current_activity=current_activity,
                experience_years=experience_years,
                franchise_timeline=franchise_timeline,
                franchise_type=franchise_type,
                investment_range=investment_range,
                additional_info=additional_info,
                status='completed'
            )
            
            # Enviar email de confirmação
            try:
                self._send_franchise_confirmation_email(lead)
                lead.confirmation_email_sent = True
                lead.save()
            except Exception as e:
                logger.error(f"Erro ao enviar email de franquia: {str(e)}")
                # Não falhar o processo por causa do email
            
            return JsonResponse({
                'success': True,
                'lead_id': lead.id,
                'message': 'Dados de franqueado salvos com sucesso!'
            })
            
        except Exception as e:
            logger.error(f"Erro ao processar lead de franquia: {str(e)}")
            return JsonResponse({'error': 'Erro ao processar dados de franqueado'}, status=500)
    
    def _send_confirmation_email(self, lead):
        """Enviar email de confirmação de agendamento"""
        subject = f"Confirmação de Agendamento - {lead.name}"
        
        # Renderizar template do email
        context = {
            'lead': lead,
            'site_url': getattr(settings, 'SITE_URL', 'https://www.agenciakaizen.com.br')
        }
        
        html_message = render_to_string('leads/email_confirmation.html', context)
        plain_message = f"""
        Olá {lead.name},
        
        Obrigado por agendar uma reunião conosco!
        
        Dados do agendamento:
        - Nome: {lead.name}
        - Email: {lead.email}
        - Telefone: {lead.phone}
        - Faturamento: {lead.get_monthly_revenue_display()}
        - Área: {lead.get_business_area_display()}
        
        Nossa equipe entrará em contato em breve para confirmar os detalhes.
        
        Atenciosamente,
        Equipe Agência Kaizen
        """
        
        # Email para o comercial
        commercial_email = getattr(settings, 'COMMERCIAL_EMAIL', 'comercial@agenciakaizen.com.br')
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[commercial_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Email de confirmação para o lead
        send_mail(
            subject=f"Confirmação de Agendamento - Agência Kaizen",
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[lead.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    def _send_franchise_confirmation_email(self, lead):
        """Enviar email de confirmação para franqueados"""
        subject = f"Interesse em Franquia - {lead.name}"
        
        # Renderizar template do email
        context = {
            'lead': lead,
            'site_url': getattr(settings, 'SITE_URL', 'https://www.agenciakaizen.com.br')
        }
        
        html_message = render_to_string('leads/franchise_email_confirmation.html', context)
        plain_message = f"""
        Olá {lead.name},
        
        Obrigado pelo seu interesse em se tornar um franqueado da Agência Kaizen!
        
        Dados recebidos:
        - Nome: {lead.name}
        - Email: {lead.email}
        - Telefone: {lead.phone}
        - Área de Atuação: {lead.get_current_activity_display() if lead.current_activity else 'Não informado'}
        - Experiência: {lead.get_experience_years_display() if lead.experience_years else 'Não informado'}
        - Prazo para Início: {lead.get_franchise_timeline_display() if lead.franchise_timeline else 'Não informado'}
        - Tipo de Franquia: {lead.get_franchise_type_display() if lead.franchise_type else 'Não informado'}
        - Faixa de Investimento: {lead.get_investment_range_display() if lead.investment_range else 'Não informado'}
        - Informações Adicionais: {lead.additional_info or 'Nenhuma'}
        
        Nossa equipe de franquias entrará em contato em breve para apresentar as oportunidades disponíveis.
        
        Atenciosamente,
        Equipe Agência Kaizen
        """
        
        # Email para o comercial/franquias
        franchise_email = getattr(settings, 'FRANCHISE_EMAIL', 'franquias@agenciakaizen.com.br')
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[franchise_email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Email de confirmação para o lead
        send_mail(
            subject=f"Confirmação de Interesse em Franquia - Agência Kaizen",
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[lead.email],
            html_message=html_message,
            fail_silently=False,
        )


@csrf_exempt
@require_http_methods(["GET"])
def get_lead_data(request, lead_id):
    """Retornar dados de um lead específico"""
    try:
        lead = Lead.objects.get(id=lead_id)
        return JsonResponse({
            'success': True,
            'data': {
                'id': lead.id,
                'name': lead.name,
                'email': lead.email,
                'phone': lead.phone,
                'monthly_revenue': lead.monthly_revenue,
                'business_area': lead.business_area,
                'main_challenge': lead.main_challenge,
                'website_social': lead.website_social,
                'status': lead.status,
            }
        })
    except Lead.DoesNotExist:
        return JsonResponse({'error': 'Lead não encontrado'}, status=404)
    except Exception as e:
        logger.error(f"Erro ao buscar lead: {str(e)}")
        return JsonResponse({'error': 'Erro interno do servidor'}, status=500)
