"""
Serviços para gerenciamento de emails e mensagens de contato
Agência Kaizen - Sistema de Email
"""

import logging
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from .models import ContactMessage, EmailTemplate

logger = logging.getLogger(__name__)


class EmailService:
    """
    Serviço para envio de emails com SendGrid
    """
    
    @staticmethod
    def send_contact_notification(contact_message: ContactMessage):
        """
        Envia notificação para o comercial sobre nova mensagem
        """
        try:
            # Template de notificação
            template = EmailTemplate.objects.filter(
                category='contact_notification',
                is_active=True
            ).first()
            
            if template:
                subject = template.subject.format(
                    name=contact_message.name,
                    subject=contact_message.subject
                )
                html_content = template.html_content.format(
                    name=contact_message.name,
                    email=contact_message.email,
                    phone=contact_message.phone,
                    company=contact_message.company,
                    subject=contact_message.subject,
                    message=contact_message.message,
                    created_at=contact_message.created_at.strftime('%d/%m/%Y %H:%M'),
                    ip_address=contact_message.ip_address,
                    page_url=contact_message.page_url
                )
            else:
                # Template padrão se não houver template customizado
                subject = f"Nova mensagem de contato: {contact_message.subject}"
                html_content = f"""
                <h2>Nova mensagem de contato recebida</h2>
                <p><strong>Nome:</strong> {contact_message.name}</p>
                <p><strong>Email:</strong> {contact_message.email}</p>
                <p><strong>Telefone:</strong> {contact_message.phone}</p>
                <p><strong>Empresa:</strong> {contact_message.company}</p>
                <p><strong>Assunto:</strong> {contact_message.subject}</p>
                <p><strong>Mensagem:</strong></p>
                <p>{contact_message.message}</p>
                <hr>
                <p><small>Enviado em: {contact_message.created_at.strftime('%d/%m/%Y %H:%M')}</small></p>
                <p><small>IP: {contact_message.ip_address}</small></p>
                <p><small>Página: {contact_message.page_url}</small></p>
                """
            
            # Enviar email
            msg = EmailMultiAlternatives(
                subject=subject,
                body=f"Nova mensagem de {contact_message.name}: {contact_message.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.COMMERCIAL_EMAIL]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            # Atualizar status
            contact_message.email_sent = True
            contact_message.email_sent_at = timezone.now()
            contact_message.save()
            
            logger.info(f"Email de notificação enviado para {settings.COMMERCIAL_EMAIL}")
            return True
            
        except Exception as e:
            # Salvar erro
            contact_message.email_error = str(e)
            contact_message.save()
            logger.error(f"Erro ao enviar email de notificação: {e}")
            return False
    
    @staticmethod
    def send_contact_confirmation(contact_message: ContactMessage):
        """
        Envia email de confirmação para quem enviou a mensagem
        """
        try:
            # Template de confirmação
            template = EmailTemplate.objects.filter(
                category='contact_confirmation',
                is_active=True
            ).first()
            
            if template:
                subject = template.subject.format(name=contact_message.name)
                html_content = template.html_content.format(
                    name=contact_message.name,
                    subject=contact_message.subject
                )
            else:
                # Template padrão
                subject = "Recebemos sua mensagem - Agência Kaizen"
                html_content = f"""
                <h2>Olá, {contact_message.name}!</h2>
                <p>Recebemos sua mensagem sobre "{contact_message.subject}" e entraremos em contato em breve.</p>
                <p>Nossa equipe comercial analisará sua solicitação e retornará o mais rápido possível.</p>
                <p>Se precisar de atendimento urgente, ligue para nosso 0800-550-8000.</p>
                <br>
                <p>Atenciosamente,<br>
                <strong>Equipe Agência Kaizen</strong></p>
                """
            
            # Enviar email
            msg = EmailMultiAlternatives(
                subject=subject,
                body=f"Olá {contact_message.name}, recebemos sua mensagem e entraremos em contato em breve.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[contact_message.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            logger.info(f"Email de confirmação enviado para {contact_message.email}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar email de confirmação: {e}")
            return False
    
    @staticmethod
    def process_contact_form(form_data, request):
        """
        Processa formulário de contato: salva no banco e envia emails
        """
        try:
            # Capturar metadados
            ip_address = EmailService.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            page_url = request.build_absolute_uri()
            
            # Criar mensagem
            contact_message = ContactMessage.objects.create(
                name=form_data['name'],
                email=form_data['email'],
                phone=form_data.get('phone', ''),
                company=form_data.get('company', ''),
                subject=form_data['subject'],
                message=form_data['message'],
                subject_category=form_data.get('subject_category', 'outro'),
                ip_address=ip_address,
                user_agent=user_agent,
                page_url=page_url
            )
            
            # Enviar emails
            EmailService.send_contact_notification(contact_message)
            EmailService.send_contact_confirmation(contact_message)
            
            logger.info(f"Mensagem de contato processada: {contact_message.id}")
            return contact_message
            
        except Exception as e:
            logger.error(f"Erro ao processar formulário de contato: {e}")
            raise
    
    @staticmethod
    def get_client_ip(request):
        """
        Obtém IP real do cliente
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class NewsletterService:
    """
    Serviço para gerenciamento de newsletter
    """
    
    @staticmethod
    def subscribe_email(email, name=None, source='website'):
        """
        Inscreve email na newsletter
        """
        try:
            # Aqui você pode integrar com ferramentas como Mailchimp, RD Station, etc.
            # Por enquanto, vamos salvar como uma mensagem de contato
            
            contact_message = ContactMessage.objects.create(
                name=name or 'Newsletter',
                email=email,
                subject='Inscrição na Newsletter',
                message=f'Inscrição na newsletter via {source}',
                subject_category='outro'
            )
            
            # Enviar email de boas-vindas
            template = EmailTemplate.objects.filter(
                category='welcome',
                is_active=True
            ).first()
            
            if template:
                subject = template.subject.format(name=name or 'Visitante')
                html_content = template.html_content.format(name=name or 'Visitante')
                
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=f"Bem-vindo à newsletter da Agência Kaizen!",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            
            logger.info(f"Nova inscrição na newsletter: {email}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao processar inscrição na newsletter: {e}")
            return False
