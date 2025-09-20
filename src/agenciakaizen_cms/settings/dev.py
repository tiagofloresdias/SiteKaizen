"""
Configurações de desenvolvimento para Agencia Kaizen CMS
"""
from .base import *

# Debug mode
DEBUG = True

# Database para desenvolvimento - usar SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Cache para desenvolvimento
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Email para desenvolvimento - usar SendGrid em produção
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API', '')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_COMERCIAL', 'comercial@agenciakaizen.com.br')

# Debug toolbar
if DEBUG:
    INTERNAL_IPS = [
        '127.0.0.1',
        'localhost',
    ]

# Logging para desenvolvimento
LOGGING['loggers']['django']['level'] = 'DEBUG'
if 'agenciakaizen_cms' not in LOGGING['loggers']:
    LOGGING['loggers']['agenciakaizen_cms'] = {
        'handlers': ['file'],
        'level': 'DEBUG',
        'propagate': True,
    }
else:
    LOGGING['loggers']['agenciakaizen_cms']['level'] = 'DEBUG'