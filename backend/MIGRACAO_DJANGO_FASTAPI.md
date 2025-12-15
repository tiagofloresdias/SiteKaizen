# Migração Django/Wagtail para FastAPI + PostgreSQL

## ✅ Status da Migração

### Modelos Criados (SQLAlchemy + PostgreSQL)

1. **Blog** (`app/models/blog.py`)
   - ✅ `Article` - Posts do blog (migrado de BlogPage)
   - ✅ `ArticleCategory` - Categorias do blog
   - ✅ `Tag` - Tags para artigos

2. **Portfolio** (`app/models/portfolio.py`)
   - ✅ `PortfolioItem` - Itens do portfolio
   - ✅ `PortfolioCategory` - Categorias do portfolio
   - ✅ `PortfolioGalleryImage` - Imagens da galeria

3. **Pages** (`app/models/page.py`)
   - ✅ `StandardPage` - Páginas padrão/evergreen

4. **Contact** (`app/models/contact.py`)
   - ✅ `Newsletter` - Assinantes da newsletter
   - ✅ `ContactMessage` - Mensagens de contato

5. **Leads** (`app/models/lead.py`)
   - ✅ `Lead` - Leads do formulário multi-passo
   - ✅ `Touchpoint` - Eventos de interação
   - ✅ `UTMParameters` - Parâmetros UTM

6. **Cases** (`app/models/case.py`)
   - ✅ `Case` - Cases de sucesso

7. **Companies** (`app/models/company.py`)
   - ✅ `Company` - Empresas do grupo
   - ✅ `CompanyCategory` - Categorias de empresas
   - ✅ `CompanyFeature` - Características das empresas

8. **Locations** (`app/models/location.py`)
   - ✅ `Location` - Escritórios/localizações

### Configuração

- ✅ `app/config.py` - Configurações atualizadas para PostgreSQL
- ✅ `app/db/session.py` - Sessão SQLAlchemy configurada
- ✅ `requirements.txt` - Dependências atualizadas (Jinja2, autenticação, etc)

### Estrutura Criada

- ✅ `app/core/templates.py` - Sistema de templates Jinja2
- ✅ `app/models/__init__.py` - Importação centralizada de modelos

## 🔄 Próximos Passos

### 1. Criar Migrações Alembic
```bash
cd /var/www/agenciakaizen/backend
source venv/bin/activate
alembic revision --autogenerate -m "Criar todas as tabelas"
alembic upgrade head
```

### 2. Criar Endpoints REST

Criar routers para:
- `/api/v1/blog/` - Endpoints de blog
- `/api/v1/portfolio/` - Endpoints de portfolio
- `/api/v1/pages/` - Endpoints de páginas
- `/api/v1/contact/` - Endpoints de contato
- `/api/v1/leads/` - Endpoints de leads
- `/api/v1/cases/` - Endpoints de cases
- `/api/v1/services/` - Endpoints de serviços

### 3. Sistema de Autenticação

- Criar modelos de usuário
- Implementar JWT authentication
- Middleware de autenticação

### 4. Upload de Arquivos

- Endpoint para upload de imagens
- Processamento de imagens
- Armazenamento em `/media/`

### 5. Templates Jinja2

- Migrar templates Django para Jinja2
- Criar sistema de renderização de páginas
- Manter compatibilidade com templates existentes

### 6. Migração de Dados

- Script para migrar dados do Django para PostgreSQL
- Preservar relacionamentos
- Validar integridade dos dados

### 7. Configuração de Produção

- Serviço systemd para FastAPI
- Configuração Nginx
- Variáveis de ambiente
- Logs e monitoramento

## 📊 Performance

### Vantagens do FastAPI + PostgreSQL

1. **Performance**: FastAPI é assíncrono e muito mais rápido que Django
2. **Type Safety**: Pydantic valida automaticamente os dados
3. **Documentação Automática**: Swagger/OpenAPI automático
4. **PostgreSQL**: Melhor performance e recursos avançados
5. **Menos Overhead**: Sem a complexidade do Wagtail CMS

### Otimizações Implementadas

- ✅ Pool de conexões PostgreSQL configurado
- ✅ Índices nas colunas mais consultadas
- ✅ UUID como primary keys (melhor para distribuição)
- ✅ JSONB para campos complexos (StreamField)

## 🔧 Comandos Úteis

### Instalar dependências
```bash
cd /var/www/agenciakaizen/backend
source venv/bin/activate
pip install -r requirements.txt
```

### Criar migração
```bash
alembic revision --autogenerate -m "Descrição da migração"
```

### Aplicar migração
```bash
alembic upgrade head
```

### Rodar servidor de desenvolvimento
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8005
```

### Rodar servidor de produção
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8005
```

## 📝 Notas Importantes

1. **Banco de Dados**: Usar PostgreSQL exclusivamente (não MongoDB)
2. **Multitenant**: Manter isolamento por clientid
3. **Permissões**: Sistema de permissões deve ser implementado
4. **Templates**: Migrar gradualmente templates Django para Jinja2
5. **API**: Manter compatibilidade com frontend existente

## 🚀 Deploy

Após completar a migração:

1. Criar serviço systemd
2. Configurar Nginx
3. Migrar dados do Django
4. Testar todos os endpoints
5. Atualizar frontend se necessário
6. Monitorar performance

