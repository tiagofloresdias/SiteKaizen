# Documentação: Migração Django/Wagtail → FastAPI + Next.js

## 📋 Visão Geral

Este documento descreve a migração completa do site da Agência Kaizen de Django/Wagtail para uma arquitetura moderna com FastAPI + Next.js.

---

## 🗂️ Estrutura do Projeto

```
/var/www/agenciakaizen/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # Entry point FastAPI
│   │   ├── config.py          # Configurações
│   │   ├── db/                # Database (SQLAlchemy)
│   │   ├── models/            # Modelos SQLAlchemy
│   │   ├── schemas/           # Schemas Pydantic
│   │   └── api/v1/            # Endpoints
│   ├── alembic/               # Migrations
│   └── scripts/               # Scripts utilitários
│
└── frontend/                   # Next.js Frontend
    ├── app/                    # App Router (Next.js 14+)
    ├── components/             # Componentes React
    ├── lib/                    # Utilities
    ├── theme/                  # Design tokens
    └── public/                 # Assets estáticos
```

---

## 🚀 Como Rodar

### 1. Backend FastAPI

```bash
cd backend

# Criar venv
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Editar .env com suas configurações

# Criar banco de dados
createdb agenciakaizen  # PostgreSQL

# Rodar migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload --port 8000
```

**Backend rodará em:** `http://localhost:8000`  
**Documentação API:** `http://localhost:8000/docs`

### 2. Frontend Next.js

```bash
cd frontend

# Instalar dependências
npm install

# Configurar .env.local (opcional)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
echo "NEXT_PUBLIC_SITE_URL=http://localhost:3000" >> .env.local

# Rodar em desenvolvimento
npm run dev

# Build para produção
npm run build
npm start
```

**Frontend rodará em:** `http://localhost:3000`

### 3. Scripts Utilitários

```bash
# Clonar assets do site antigo
cd backend
python scripts/scrape_assets.py

# Extrair design tokens
python scripts/extract_theme.py
```

---

## 📦 Estrutura de Assets

### Assets no Frontend

Os assets ficam em `frontend/public/`:

```
frontend/public/
├── img/
│   ├── backgrounds/    # Imagens de fundo
│   ├── icons/          # Ícones
│   ├── logos/          # Logos
│   └── companies/      # Imagens de empresas
└── fonts/              # Fontes customizadas
```

---

## 🎨 Design Tokens

Os design tokens estão em `frontend/theme/tokens.ts`:

```typescript
import { theme } from '@/theme/tokens'

// Cores
theme.colors.primary      // #D62042
theme.colors.primaryLight // #ff6b6b

// Tipografia
theme.typography.fontFamilyBase
theme.typography.fontSizes.base

// Botões
theme.buttons.primary
```

**Tailwind Config:** Os tokens estão integrados ao `tailwind.config.ts` e podem ser usados diretamente com classes Tailwind.

---

## 🗄️ Modelos de Banco de Dados

### Tabelas Principais

#### `companies`
- Informações das empresas do Grupo Kaizen
- Relacionamento com `company_categories` e `company_features`

#### `articles`
- Posts do blog
- Relacionamento com `article_categories`

#### `locations`
- Escritórios/unidades da Kaizen
- Inclui geolocalização e dados do Google Maps

### Migrations Alembic

```bash
# Criar nova migration
alembic revision --autogenerate -m "Descrição da migration"

# Aplicar migrations
alembic upgrade head

# Reverter última migration
alembic downgrade -1
```

---

## 🔌 Endpoints FastAPI

### Base URL: `http://localhost:8000/api/v1`

#### Companies
- `GET /companies` - Lista empresas (filtros: `category`, `is_active`, `page`, `limit`)
- `GET /companies/{slug}` - Detalhes da empresa

#### Articles
- `GET /articles` - Lista artigos (filtros: `category`, `is_featured`, `is_published`, `page`, `limit`)
- `GET /articles/{slug}` - Artigo completo

#### Locations
- `GET /locations` - Lista localizações (filtros: `is_active`, `is_main_office`)

#### Sitemap
- `GET /sitemap-data` - Dados para sitemap dinâmico

**Documentação completa:** `http://localhost:8000/docs` (Swagger UI)

---

## 🔍 SEO e JSON-LD

### Componentes SEO

Componentes em `frontend/components/seo/`:

- **`Seo.tsx`** - Meta tags dinâmicas (title, description, OG, Twitter Cards)
- **`JsonLd.tsx`** - Helper para JSON-LD
- **`Breadcrumb.tsx`** - BreadcrumbList schema

### Schemas Implementados

1. **Organization** - Global (homepage)
2. **LocalBusiness** - Por localização
3. **Article** - Por artigo do blog
4. **BreadcrumbList** - Páginas internas

### Sitemap e Robots

- **`app/sitemap.ts`** - Sitemap dinâmico Next.js
- **`app/robots.ts`** - Robots.txt dinâmico

---

## 📝 Adicionar Novo Conteúdo

### Adicionar Empresa

1. Inserir no PostgreSQL:
```sql
INSERT INTO companies (name, slug, category_id, ...) 
VALUES ('Nova Empresa', 'nova-empresa', 'uuid-categoria', ...);
```

2. A empresa aparecerá automaticamente em `/nossas-empresas`
3. JSON-LD `Organization` será gerado automaticamente

### Adicionar Artigo

1. Inserir no PostgreSQL:
```sql
INSERT INTO articles (title, slug, content, published_at, ...) 
VALUES ('Novo Artigo', 'novo-artigo', '<p>Conteúdo...</p>', NOW(), ...);
```

2. O artigo aparecerá em `/blog`
3. JSON-LD `Article` será gerado automaticamente em `/blog/novo-artigo`

---

## 🔧 Configuração de Produção

### Backend (Systemd)

Criar serviço systemd:

```ini
[Unit]
Description=Agência Kaizen API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/agenciakaizen/backend
Environment="PATH=/var/www/agenciakaizen/backend/venv/bin"
ExecStart=/var/www/agenciakaizen/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Frontend (Next.js)

Build para produção:

```bash
cd frontend
npm run build
npm start
```

Ou usar PM2:

```bash
pm2 start npm --name "kaizen-frontend" -- start
```

### Nginx

Configurar Nginx para reverse proxy:

```nginx
# Backend
location /api/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

# Frontend
location / {
    proxy_pass http://127.0.0.1:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

---

## 📚 Referências

- **Next.js**: https://nextjs.org/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Alembic**: https://alembic.sqlalchemy.org/
- **Schema.org**: https://schema.org/
- **Tailwind CSS**: https://tailwindcss.com/docs

---

## ✅ Checklist de Migração

- [x] Estrutura de pastas criada
- [x] Backend FastAPI configurado
- [x] Modelos SQLAlchemy criados
- [x] Migrations Alembic configuradas
- [x] Endpoints FastAPI implementados
- [x] Scripts de scraping criados
- [x] Design tokens extraídos
- [x] Frontend Next.js inicializado
- [ ] Componentes React criados
- [ ] Páginas Next.js implementadas
- [ ] SEO e JSON-LD integrados
- [ ] Testes realizados
- [ ] Deploy em produção

---

**Última atualização:** 2025-11-20  
**Versão:** 1.0.0



