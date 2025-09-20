from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json
import logging

from .models import RecruitmentApplication, FoguetePage

logger = logging.getLogger(__name__)


def recruitment_page(request):
    """
    View para a página de recrutamento principal
    """
    return render(request, 'recruitment/recruitment_simple.html', {
        'request': request,
    })


def foguete_page(request):
    """
    View para a página FoguetePage
    """
    try:
        page = FoguetePage.objects.filter(slug='quero-ser-um-foguete', live=True).first()
        
        if not page:
            # Se a página não existir, cria uma com conteúdo padrão
            from wagtail.models import Page
            root_page = Page.objects.filter(slug='home').first()
            if root_page:
                page = FoguetePage(
                    title="Quero Ser um Foguete",
                    slug="quero-ser-um-foguete",
                    live=True,
                    hero_title="Quero Ser um Foguete Kaizen",
                    hero_subtitle="Faça parte de uma equipe que acredita na melhoria contínua e na excelência operacional.",
                    culture_title="Nossa Cultura Kaizen",
                    culture_content="<p>A filosofia Kaizen está no DNA da nossa empresa. Acreditamos que pequenas melhorias constantes levam a grandes transformações. Aqui, cada foguete contribui para a evolução contínua da equipe e dos resultados.</p><p><strong>Nossos valores fundamentais:</strong></p><ul><li><strong>Trabalho em equipe sem mim:</strong> O sucesso é coletivo, não individual</li><li><strong>Feito é melhor do que perfeito:</strong> Agimos com velocidade e eficiência</li><li><strong>Os resultados são determinantes:</strong> Focamos no que realmente importa</li><li><strong>Melhoria contínua:</strong> Sempre buscamos evoluir</li></ul>",
                    five_s_title="Os 5S da Kaizen",
                    five_s_content="<p>A metodologia 5S é a base da nossa organização e eficiência. Cada foguete aplica esses princípios no dia a dia:</p>",
                    benefits_title="Por que ser um Foguete?",
                    benefits_content="<p>Ser um Foguete Kaizen é mais que um trabalho, é uma missão. Você fará parte de uma equipe que transforma negócios e vidas através do marketing digital de alta performance.</p>",
                    cta_title="Pronto para Decolar?",
                    cta_subtitle="Junte-se à nossa equipe de foguetes e faça parte da revolução do marketing digital."
                )
                root_page.add_child(instance=page)
                page.save_revision().publish()
    except Exception as e:
        # Fallback para página padrão
        page = None
    
    return render(request, 'recruitment/foguete_page.html', {
        'page': page,
        'request': request,
    })


@method_decorator(csrf_exempt, name='dispatch')
class RecruitmentAPIView(View):
    """
    API para processar candidaturas de recrutamento
    """
    
    def post(self, request):
        try:
            # Verificar se é FormData ou JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                files = {}
            else:
                # FormData
                data = request.POST.dict()
                files = request.FILES
            
            # Validar campos obrigatórios
            required_fields = [
                'full_name', 'email', 'phone',
                'cpf', 'position_interest', 'salary_expectation',
                'work_modality_preference', 'motivation', 'state', 'city',
                'instagram_profile'
            ]
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({
                        'success': False,
                        'message': f'Campo obrigatório: {field}'
                    }, status=400)
            
            # Processar arquivo de currículo (obrigatório)
            resume_file = files.get('resume') if files else None
            if not resume_file:
                return JsonResponse({
                    'success': False,
                    'message': 'Campo obrigatório: resume (Currículo)'
                }, status=400)
            
            # Mapear position_interest para desired_area
            position_mapping = {
                'desenvolvedor': 'desenvolvimento',
                'designer': 'design',
                'marketing': 'marketing_digital',
                'vendas': 'vendas',
                'rh': 'rh',
                'financeiro': 'financeiro',
                'atendimento': 'atendimento',
                'operacional': 'operacional',
                'gestao': 'gestao',
                'outro': 'outro'
            }
            desired_area = position_mapping.get(data.get('position_interest', 'outro'), 'outro')
            
            # Criar candidatura com todos os campos obrigatórios
            application = RecruitmentApplication.objects.create(
                full_name=data.get('full_name'),
                email=data.get('email'),
                phone=data.get('phone'),
                birth_date=data.get('birth_date'),
                cpf=data.get('cpf', ''),
                rg=data.get('rg', ''),
                address=data.get('address', ''),
                city=data.get('city', ''),
                state=data.get('state', ''),
                zip_code=data.get('zip_code', ''),
                current_position=data.get('current_position', ''),
                current_company=data.get('current_company', ''),
                experience_years=int(data.get('experience_years', 0)) if str(data.get('experience_years', '')).isdigit() else 0,
                education_level=data.get('education_level', 'medio'),
                desired_area=desired_area,
                availability=data.get('availability', 'imediata'),
                technical_skills=data.get('skills', ''),
                languages=data.get('languages', ''),
                crm_experience=data.get('crm_experience', False),
                social_media_experience=data.get('social_media_experience', False),
                google_ads_experience=data.get('google_ads_experience', False),
                facebook_ads_experience=data.get('facebook_ads_experience', False),
                analytics_experience=data.get('analytics_experience', False),
                seo_experience=data.get('seo_experience', False),
                content_creation_experience=data.get('content_creation_experience', False),
                motivation=data.get('motivation'),
                salary_expectation=data.get('salary_expectation', ''),
                career_goals=data.get('career_goals', ''),
                referral_source=data.get('referral_source', 'site'),
                linkedin_profile=data.get('linkedin_profile', ''),
                instagram_profile=data.get('instagram_profile', ''),
                portfolio_url=data.get('portfolio_url', ''),
                work_modality_preference=data.get('work_modality_preference', 'remoto'),
                resume_file=resume_file,
            )
            
            # Enviar emails
            self._send_confirmation_email(application)
            self._send_rh_notification_email(application)
            
            return JsonResponse({
                'success': True,
                'application_id': application.id,
                'message': 'Candidatura enviada com sucesso!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro: {str(e)}'
            }, status=500)
    
    def _send_confirmation_email(self, application):
        """Enviar email de confirmação para o candidato"""
        try:
            subject = f'Candidatura Recebida - {application.full_name}'
            
            context = {
                'application': application,
                'company_name': 'Agência Kaizen',
            }
            
            html_message = render_to_string('recruitment/email_confirmation.html', context)
            
            send_mail(
                subject=subject,
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[application.email],
                html_message=html_message,
                fail_silently=False,
            )
            
        except Exception as e:
            logger.error(f"Erro ao enviar email de confirmação: {str(e)}")
    
    def _send_rh_notification_email(self, application):
        """Enviar notificação para RH sobre nova candidatura"""
        try:
            subject = f'Nova Candidatura - {application.full_name} - {application.desired_area}'
            
            context = {
                'application': application,
                'company_name': 'Agência Kaizen',
            }
            
            html_message = render_to_string('recruitment/rh_notification_email.html', context)
            
            send_mail(
                subject=subject,
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['rh@agenciakaizen.com.br'],
                html_message=html_message,
                fail_silently=False,
            )
            
        except Exception as e:
            logger.error(f"Erro ao enviar email para RH: {str(e)}")