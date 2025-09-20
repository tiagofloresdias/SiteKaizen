"""
Configurações de produção para Agencia Kaizen CMS
"""
from .base import *

# Debug mode
DEBUG = True

# Security settings - nginx já faz o redirecionamento HTTPS
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Session security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Cache desabilitado - usando configuração do base.py

# Logging para produção
if 'handlers' in LOGGING and 'file' in LOGGING['handlers']:
    LOGGING['handlers']['file']['level'] = 'WARNING'
if 'loggers' in LOGGING and 'django' in LOGGING['loggers']:
    LOGGING['loggers']['django']['level'] = 'WARNING'
if 'loggers' in LOGGING and 'agenciakaizen_cms' in LOGGING['loggers']:
    LOGGING['loggers']['agenciakaizen_cms']['level'] = 'INFO'

# Importar configurações de email
from .email import *

# Allowed hosts
ALLOWED_HOSTS = [
    'new.agenciakaizen.com.br',
    'localhost',
    '127.0.0.1',
]

# Wagtail settings para produção
WAGTAILADMIN_BASE_URL = 'https://new.agenciakaizen.com.br/admin/'
BASE_URL = 'https://new.agenciakaizen.com.br'