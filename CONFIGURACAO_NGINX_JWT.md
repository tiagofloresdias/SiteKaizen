# ✅ Configuração Nginx + FastAPI + Next.js + JWT

## 🎯 Configuração Completa

### Nginx - Proxy Reverso

**Arquivo**: `/etc/nginx/sites-available/site2025.agenciakaizen.com.br`

#### Estrutura de Roteamento

```
site2025.agenciakaizen.com.br
├── /api/*          → FastAPI (porta 8006)
└── /*              → Next.js (porta 3000 local ou Vercel)
```

#### Como Funciona

1. **`/api/*`** → Proxy reverso para FastAPI
   - Remove `/api` do path antes de passar para FastAPI
   - FastAPI recebe apenas `/v1/*`
   - Exemplo: `/api/v1/auth/login` → FastAPI recebe `/v1/auth/login`

2. **`/*`** (todas as outras rotas) → Next.js
   - Rotas principais do site
   - Admin panel (se implementado no Next.js)
   - Páginas estáticas

### Autenticação JWT

#### Endpoints Disponíveis

**Base URL**: `https://site2025.agenciakaizen.com.br/api/v1`

1. **Login**
   - `POST /api/v1/auth/login` - Login com OAuth2 (form-data)
   - `POST /api/v1/auth/login/json` - Login com JSON
   - Retorna: `{access_token, token_type, expires_in}`

2. **Usuário Atual**
   - `GET /api/v1/auth/me` - Informações do usuário logado
   - Requer: Bearer token no header

3. **Registro** (apenas admin)
   - `POST /api/v1/auth/register` - Criar novo usuário
   - Requer: Bearer token de admin

4. **Atualizar Perfil**
   - `PUT /api/v1/auth/me` - Atualizar dados do usuário atual
   - Requer: Bearer token

#### Endpoints Admin

1. **Listar Usuários**
   - `GET /api/v1/admin/users` - Lista todos os usuários
   - Requer: Bearer token de admin

2. **Criar Usuário**
   - `POST /api/v1/admin/users` - Criar novo usuário
   - Requer: Bearer token de admin

3. **Atualizar Usuário**
   - `PUT /api/v1/admin/users/{user_id}` - Atualizar usuário
   - Requer: Bearer token de admin

4. **Deletar Usuário**
   - `DELETE /api/v1/admin/users/{user_id}` - Deletar usuário
   - Requer: Bearer token de admin

### Como Usar

#### 1. Criar Primeiro Usuário Admin

```bash
cd /var/www/agenciakaizen/backend
source ../venv/bin/activate
python scripts/create_admin_user.py
```

#### 2. Fazer Login

```bash
curl -X POST "https://site2025.agenciakaizen.com.br/api/v1/auth/login/json" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "senha123"
  }'
```

Resposta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### 3. Usar Token nas Requisições

```bash
curl -X GET "https://site2025.agenciakaizen.com.br/api/v1/auth/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Frontend Next.js

O frontend deve fazer requisições para:
- **API**: `https://site2025.agenciakaizen.com.br/api/v1/*`
- **Páginas**: `https://site2025.agenciakaizen.com.br/*`

#### Exemplo de Login no Frontend

```typescript
// lib/api.ts
export async function login(username: string, password: string) {
  const response = await fetch('https://site2025.agenciakaizen.com.br/api/v1/auth/login/json', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });
  
  if (!response.ok) throw new Error('Login failed');
  
  const data = await response.json();
  // Salvar token no localStorage
  localStorage.setItem('token', data.access_token);
  return data;
}

// Usar token em requisições autenticadas
export async function getMe() {
  const token = localStorage.getItem('token');
  const response = await fetch('https://site2025.agenciakaizen.com.br/api/v1/auth/me', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  return response.json();
}
```

### Variáveis de Ambiente

**Backend FastAPI** (`.env`):
```env
SECRET_KEY=seu-secret-key-aqui
DB_NAME=agenciakaizen_cms
DB_USER=postgres
DB_PASSWORD=senha
DB_HOST=localhost
DB_PORT=5432
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend Next.js** (Vercel):
```env
NEXT_PUBLIC_API_URL=https://site2025.agenciakaizen.com.br/api/v1
NEXT_PUBLIC_SITE_URL=https://site2025.agenciakaizen.com.br
```

### Segurança

- ✅ JWT tokens com expiração
- ✅ Senhas hasheadas com bcrypt
- ✅ CORS configurado
- ✅ Headers de segurança no Nginx
- ✅ Validação de permissões (admin/superuser)

### Próximos Passos

1. ✅ Nginx configurado
2. ✅ JWT implementado
3. ✅ Endpoints de auth criados
4. ✅ Endpoints de admin criados
5. ⏳ Criar interface de admin no Next.js
6. ⏳ Implementar proteção de rotas no frontend
7. ⏳ Adicionar refresh tokens (opcional)

---

**Status**: ✅ Configuração completa e funcionando!

