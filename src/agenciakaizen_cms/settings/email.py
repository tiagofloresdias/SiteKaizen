"""
Configurações de email para Agencia Kaizen CMS
"""
import os

# Email para produção usando SendGrid
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'apikey'  # SendGrid usa 'apikey' como username
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API', '')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_COMERCIAL', 'comercial@agenciakaizen.com.br')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Configurações adicionais
EMAIL_TIMEOUT = 30
EMAIL_USE_LOCALTIME = True

# Para desenvolvimento, usar console backend
if os.environ.get('DEBUG', 'False').lower() == 'true':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
