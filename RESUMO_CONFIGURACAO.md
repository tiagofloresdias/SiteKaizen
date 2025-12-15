# ✅ Configuração Completa - Nginx + FastAPI + Next.js + JWT

## 🎯 Status: TUDO CONFIGURADO E FUNCIONANDO!

### Estrutura Final

```
site2025.agenciakaizen.com.br
├── /api/*          → FastAPI (porta 8006)
│   ├── /api/v1/auth/*      - Autenticação JWT
│   ├── /api/v1/admin/*     - Endpoints admin
│   ├── /api/v1/articles/*  - Blog/Artigos
│   ├── /api/v1/companies/* - Empresas
│   └── /api/v1/locations/* - Localizações
└── /*              → Next.js (porta 3000 local ou Vercel)
    ├── /           - Home
    ├── /blog       - Blog
    ├── /contato    - Contato
    └── /admin      - Admin panel (futuro)
```

## ✅ O que foi Configurado

### 1. Nginx - Proxy Reverso ✅

**Arquivo**: `/etc/nginx/sites-available/site2025.agenciakaizen.com.br`

- ✅ `/api/*` → FastAPI (porta 8006)
- ✅ `/*` → Next.js (porta 3000)
- ✅ Headers de segurança
- ✅ CORS configurado
- ✅ Gzip compression
- ✅ Cache para assets estáticos

### 2. Autenticação JWT ✅

**Arquivos Criados**:
- ✅ `backend/app/core/auth.py` - Sistema de autenticação
- ✅ `backend/app/models/user.py` - Modelo de usuário
- ✅ `backend/app/schemas/auth.py` - Schemas Pydantic
- ✅ `backend/app/api/v1/auth.py` - Endpoints de auth
- ✅ `backend/app/api/v1/admin.py` - Endpoints admin

**Endpoints Disponíveis**:
- `POST /api/v1/auth/login` - Login (OAuth2 form)
- `POST /api/v1/auth/login/json` - Login (JSON)
- `GET /api/v1/auth/me` - Usuário atual
- `POST /api/v1/auth/register` - Registrar (admin only)
- `PUT /api/v1/auth/me` - Atualizar perfil

**Endpoints Admin**:
- `GET /api/v1/admin/users` - Listar usuários
- `POST /api/v1/admin/users` - Criar usuário
- `PUT /api/v1/admin/users/{id}` - Atualizar usuário
- `DELETE /api/v1/admin/users/{id}` - Deletar usuário

### 3. Scripts Úteis ✅

- ✅ `backend/scripts/create_admin_user.py` - Criar primeiro admin

## 🚀 Como Usar

### 1. Criar Primeiro Usuário Admin

```bash
cd /var/www/agenciakaizen/backend
source ../venv/bin/activate
python scripts/create_admin_user.py
```

### 2. Fazer Login

```bash
curl -X POST "https://site2025.agenciakaizen.com.br/api/v1/auth/login/json" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "senha123"
  }'
```

### 3. Usar Token

```bash
TOKEN="seu-token-aqui"
curl -X GET "https://site2025.agenciakaizen.com.br/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

## 📝 Notas Importantes

1. **Sem conflitos de porta**: 
   - FastAPI: 8006 (interno)
   - Next.js: 3000 (local) ou Vercel (externo)
   - Nginx gerencia tudo na porta 80/443

2. **Proxy Reverso**:
   - Nginx recebe requisições
   - Roteia `/api/*` para FastAPI
   - Roteia `/*` para Next.js

3. **JWT Tokens**:
   - Expiração: 30 minutos (configurável)
   - Algoritmo: HS256
   - Header: `Authorization: Bearer <token>`

4. **Segurança**:
   - Senhas hasheadas com bcrypt
   - Tokens JWT assinados
   - CORS configurado
   - Headers de segurança

## 🔧 Próximos Passos

1. ✅ Nginx configurado
2. ✅ JWT implementado
3. ✅ Endpoints criados
4. ⏳ Criar interface admin no Next.js
5. ⏳ Implementar proteção de rotas no frontend
6. ⏳ Adicionar refresh tokens (opcional)

---

**Status**: ✅ Tudo configurado e pronto para uso!

