"""
Configurações base para Agencia Kaizen CMS
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,new.agenciakaizen.com.br').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # Wagtail
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    'wagtail.contrib.settings',
    'wagtail.contrib.styleguide',
    'wagtail.contrib.routable_page',
    'wagtail.contrib.frontend_cache',
    'wagtail.contrib.table_block',
    
    # Wagtail AI
    'wagtail_ai',

    # Third party
    'modelcluster',
    'taggit',
    'django_extensions',
    'rest_framework',
    'corsheaders',

    # Local apps
    'common', # Added for common utilities and management commands
    'home',
    'blog',
    'portfolio',
    'services',
    'solutions', # Added for solutions page
    'contact',
    'companies',
    'analytics', # Added for GTM and tracking
    'leads', # Added for smart modal leads
    'franchise', # Added for franchise system
    'search',
    'site_settings', # Added for global site settings
    'pages', # Added for evergreen pages
    'cases', # Added for cases section
    'recruitment', # Added for recruitment system
    'universidade', # Added for universidade kaizen page
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'agenciakaizen_cms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'agenciakaizen_cms.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'agenciakaizen_cms'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Idiomas suportados
LANGUAGES = [
    ('pt-br', 'Português (Brasil)'),
    ('en', 'English'),
    ('es', 'Español'),
]

# Diretório dos arquivos de tradução
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Idioma padrão
DEFAULT_LANGUAGE = 'pt-br'

# Configurações de idioma por domínio
LANGUAGE_DOMAINS = {
    'www.agenciakaizen.com.br': 'pt-br',
    'agenciakaizen.com.br': 'pt-br',
    'en.agenciakaizen.com.br': 'en',
    'es.agenciakaizen.com.br': 'es',
}

# Static files (CSS, JavaScript, Images)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Wagtail settings
WAGTAIL_SITE_NAME = "Agência Kaizen CMS"
WAGTAILADMIN_BASE_URL = '/admin/'

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = os.environ.get('BASE_URL', 'https://new.agenciakaizen.com.br')

# Search
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.search.backends.database',
    }
}

# Cache - Desabilitado completamente
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Desabilitar cache do Wagtail
WAGTAIL_CACHE = False

# Forçar desabilitação do Redis
WAGTAIL_CACHE_BACKEND = 'django.core.cache.backends.dummy.DummyCache'

# Email - SendGrid Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'maquinadevendas@agenciakaizen.com.br')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Email comercial (do .env)
COMMERCIAL_EMAIL = os.environ.get('COMMERCIAL_EMAIL', 'maquinadevendas@agenciakaizen.com.br')

# SendGrid Settings
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')

# OpenAI Configuration for CrewAI
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'https://new.agenciakaizen.com.br',
    'http://localhost:8745',
    'http://127.0.0.1:8745',
]

# CSRF Cookie Settings
CSRF_COOKIE_SECURE = not DEBUG  # Only secure in production
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': str(BASE_DIR.parent / 'logs' / 'django.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'agenciakaizen_cms': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Wagtail specific settings
WAGTAILIMAGES_EXTENSIONS = ['gif', 'jpg', 'jpeg', 'png', 'webp', 'svg']
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

# Rich text settings
WAGTAIL_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'wagtail.admin.rich_text.DraftailRichTextArea',
        'OPTIONS': {
            'features': [
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'bold', 'italic', 'ol', 'ul', 'hr',
                'link', 'document-link', 'image', 'embed',
                'code', 'superscript', 'subscript', 'strikethrough',
                'blockquote',
            ]
        }
    },
}

# Site settings
WAGTAIL_SITE_NAME = "Agência Kaizen"
WAGTAILADMIN_BASE_URL = '/admin/'

# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://new.agenciakaizen.com.br",
]

CORS_ALLOW_CREDENTIALS = True

# CrewAI Configuration
CREWAI_CONFIG = {
    'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY', ''),
    'MODEL_NAME': 'gpt-4o-mini',
    'TEMPERATURE': 0.7,
    'MAX_TOKENS': 4000,
}

# Wagtail AI Configuration
WAGTAIL_AI = {
    'LLM_BACKENDS': {
        'openai': {
            'BACKEND': 'wagtail_ai.llm_backends.openai.OpenAIBackend',
            'CONFIG': {
                'api_key': os.environ.get('OPENAI_API_KEY', ''),
                'model': 'gpt-4o-mini',
                'temperature': 0.7,
                'max_tokens': 2000,
            }
        }
    },
    'DEFAULT_LLM_BACKEND': 'openai',
    'ENABLE_AI_FEATURES': True,
    'AI_PROMOTION_ENABLED': True,
    'AI_SUGGESTIONS_ENABLED': True,
    'AI_CONTENT_GENERATION_ENABLED': True,
}

# Configurações de páginas de erro personalizadas
# Sempre usar páginas personalizadas, mesmo em DEBUG
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django_errors.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Garantir que as páginas de erro sejam usadas
TEMPLATES[0]['OPTIONS']['context_processors'].append('django.template.context_processors.request')