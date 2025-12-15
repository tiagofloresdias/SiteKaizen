# ✅ Configuração Final - site2025.agenciakaizen.com.br

## 📋 Resumo da Configuração

### Venv Utilizado
- **Localização:** `/var/www/agenciakaizen/venv` (venv existente da raiz)
- **Python:** 3.11.8
- **Status:** ✅ FastAPI e uvicorn já instalados

### Portas Escolhidas (Seguras - Sem Conflitos)
- **FastAPI Backend:** `8006` (porta livre ✅)
- **Next.js Frontend:** `3001` (porta livre ✅)

### Portas em Uso (Não Alteradas)
- **8003:** Outro serviço Gunicorn (mantido)
- **8005:** Django site2025 antigo (mantido)

---

## 🚀 Próximos Passos

### 1. Instalar Dependências do FastAPI no Venv

```bash
cd /var/www/agenciakaizen
source venv/bin/activate
cd backend
pip install -r requirements.txt
```

Ou execute o script:
```bash
./INSTALAR_FASTAPI_VENV.sh
```

### 2. Configurar Backend

```bash
cd /var/www/agenciakaizen/backend

# Criar .env
cp .env.example .env

# Editar .env com:
# DATABASE_URL=postgresql://postgres:senha@localhost:5432/agenciakaizen
# CORS_ORIGINS=http://localhost:3001,https://site2025.agenciakaizen.com.br
```

### 3. Executar Setup Completo

```bash
cd /var/www/agenciakaizen
./setup-site2025-fastapi-nextjs.sh
```

Este script irá:
- ✅ Verificar e instalar dependências
- ✅ Criar serviços systemd
- ✅ Configurar Nginx
- ✅ Iniciar FastAPI (porta 8006) e Next.js (porta 3001)
- ✅ Verificar que tudo está funcionando

---

## 📁 Estrutura de Serviços

### Backend FastAPI
- **Serviço:** `agenciakaizen-api.service`
- **Venv:** `/var/www/agenciakaizen/venv`
- **Working Directory:** `/var/www/agenciakaizen/backend`
- **Porta:** `8006`
- **Comando:** `/var/www/agenciakaizen/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8006`

### Frontend Next.js
- **Serviço:** `agenciakaizen-frontend.service`
- **Working Directory:** `/var/www/agenciakaizen/frontend`
- **Porta:** `3001`
- **Comando:** `npm start`

### Nginx
- **Config:** `/etc/nginx/sites-available/site2025.agenciakaizen.com.br`
- **Proxy API:** `/api/` → `http://127.0.0.1:8006`
- **Proxy Frontend:** `/` → `http://127.0.0.1:3001`

---

## ✅ Checklist de Segurança

- [x] ✅ Venv existente sendo usado (não cria novo)
- [x] ✅ Portas escolhidas estão livres (8006, 3001)
- [x] ✅ Serviços existentes não serão afetados
- [x] ✅ Configuração isolada para site2025.agenciakaizen.com.br
- [x] ✅ Script verifica conflitos antes de iniciar

---

## 🔍 Verificar Status

```bash
# Verificar serviços
sudo systemctl status agenciakaizen-api.service
sudo systemctl status agenciakaizen-frontend.service

# Ver logs
sudo journalctl -u agenciakaizen-api.service -f
sudo journalctl -u agenciakaizen-frontend.service -f

# Verificar portas
ss -tlnp | grep -E ":(8006|3001)"
```

---

**Última atualização:** 2025-11-20



