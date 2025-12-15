# 🚀 Site Kaizen - FastAPI + Next.js + PostgreSQL

## 📋 Estrutura do Projeto

```
/var/www/agenciakaizen/
├── backend/          # FastAPI Backend (PostgreSQL)
│   ├── app/
│   │   ├── api/v1/   # Endpoints REST
│   │   ├── core/     # Auth, templates
│   │   ├── models/   # SQLAlchemy models
│   │   └── schemas/  # Pydantic schemas
│   └── scripts/      # Scripts utilitários
├── frontend/         # Next.js Frontend
│   ├── app/          # App Router
│   ├── components/   # Componentes React
│   └── lib/          # Utilitários e API client
└── src/              # Django/Wagtail (legado - em migração)
```

## 🔧 Configuração

### Backend FastAPI

**Sempre usar venv isolado**:
```bash
cd /var/www/agenciakaizen/backend
source ../venv/bin/activate  # ou backend/venv/bin/activate
pip install -r requirements.txt
```

**Variáveis de ambiente** (`.env`):
```env
DB_NAME=agenciakaizen_cms
DB_USER=postgres
DB_PASSWORD=senha
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=seu-secret-key-aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Rodar servidor**:
```bash
cd /var/www/agenciakaizen/backend
source ../venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8006
```

### Frontend Next.js

```bash
cd /var/www/agenciakaizen/frontend
npm install
npm run dev  # Desenvolvimento
npm run build  # Produção
```

**Variáveis de ambiente** (Vercel):
```env
NEXT_PUBLIC_API_URL=https://site2025.agenciakaizen.com.br/api/v1
NEXT_PUBLIC_SITE_URL=https://site2025.agenciakaizen.com.br
```

## 🌐 Nginx - Proxy Reverso

**Configuração**: `/etc/nginx/sites-available/site2025.agenciakaizen.com.br`

- `/api/*` → FastAPI (porta 8006)
- `/*` → Next.js (porta 3000 local ou Vercel)

## 🔐 Autenticação JWT

### Criar Primeiro Admin

```bash
cd /var/www/agenciakaizen/backend
source ../venv/bin/activate
python scripts/create_admin_user.py
```

### Endpoints

- `POST /api/v1/auth/login/json` - Login
- `GET /api/v1/auth/me` - Usuário atual
- `POST /api/v1/auth/register` - Registrar (admin only)
- `GET /api/v1/admin/users` - Listar usuários (admin)

## 📦 Banco de Dados

**PostgreSQL** - Único banco de dados (sem MongoDB)

**Migrações Alembic**:
```bash
cd /var/www/agenciakaizen/backend
source ../venv/bin/activate
alembic revision --autogenerate -m "Descrição"
alembic upgrade head
```

## 🚀 Deploy

### Frontend (Vercel)
1. Conectar repositório GitHub
2. Configurar variáveis de ambiente
3. Deploy automático

### Backend (Servidor)
1. Atualizar código: `git pull`
2. Ativar venv: `source venv/bin/activate`
3. Instalar dependências: `pip install -r backend/requirements.txt`
4. Rodar migrações: `alembic upgrade head`
5. Reiniciar serviço: `systemctl restart agenciakaizen-api.service`

## 📝 Notas Importantes

- ✅ **Sempre usar venv isolado** para Python
- ✅ PostgreSQL como banco único
- ✅ JWT para autenticação
- ✅ Nginx gerencia roteamento
- ✅ Sem conflitos de porta

## 🔗 Links Úteis

- **Repositório**: https://github.com/tiagofloresdias/SiteKaizen
- **Site**: https://site2025.agenciakaizen.com.br
- **API Docs**: https://site2025.agenciakaizen.com.br/api/docs

---

**Desenvolvido com ❤️ pela Agência Kaizen**
