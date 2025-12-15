# 🚀 Deploy site2025.agenciakaizen.com.br

## ⚠️ Problema Identificado

O serviço `agenciakaizen-site2025.service` está configurado para Django antigo, mas agora temos FastAPI + Next.js.

## ✅ Solução: Executar Script de Setup

Execute o script de configuração que cria os serviços corretos:

```bash
cd /var/www/agenciakaizen
./setup-site2025-fastapi-nextjs.sh
```

Este script irá:
1. ✅ Criar venv do backend FastAPI (se não existir)
2. ✅ Instalar dependências do frontend Next.js (se necessário)
3. ✅ Criar serviços systemd para FastAPI e Next.js
4. ✅ Configurar Nginx para site2025.agenciakaizen.com.br
5. ✅ Iniciar os serviços

---

## 📋 Pré-requisitos

Antes de executar o script, certifique-se de:

### 1. Backend FastAPI
```bash
cd /var/www/agenciakaizen/backend

# Criar venv
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar .env
cp .env.example .env
# Editar .env com DATABASE_URL correto

# Criar banco e rodar migrations
createdb agenciakaizen
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 2. Frontend Next.js
```bash
cd /var/www/agenciakaizen/frontend

# Instalar dependências
npm install

# Fazer build
npm run build

# Criar .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
echo "NEXT_PUBLIC_SITE_URL=https://site2025.agenciakaizen.com.br" >> .env.local
```

---

## 🔧 Verificar Logs dos Serviços

Depois de executar o script, verifique os logs:

```bash
# Backend FastAPI
sudo journalctl -u agenciakaizen-api.service -f

# Frontend Next.js
sudo journalctl -u agenciakaizen-frontend.service -f

# Nginx
sudo tail -f /var/log/nginx/site2025.agenciakaizen.com.br.error.log
```

---

## 📊 Status dos Serviços

```bash
# Verificar status
sudo systemctl status agenciakaizen-api.service
sudo systemctl status agenciakaizen-frontend.service

# Reiniciar se necessário
sudo systemctl restart agenciakaizen-api.service
sudo systemctl restart agenciakaizen-frontend.service

# Verificar portas
ss -tlnp | grep -E ":(8000|3000)"
```

---

## 🌐 Verificar Acesso

```bash
# Testar backend API
curl http://localhost:8000/api/v1/companies

# Testar frontend
curl http://localhost:3000

# Testar via nginx
curl http://site2025.agenciakaizen.com.br
```

---

## ⚙️ Configuração dos Serviços

### Backend FastAPI
- **Serviço:** `agenciakaizen-api.service`
- **Porta:** 8000
- **Working Directory:** `/var/www/agenciakaizen/backend`
- **Comando:** `uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4`

### Frontend Next.js
- **Serviço:** `agenciakaizen-frontend.service`
- **Porta:** 3000
- **Working Directory:** `/var/www/agenciakaizen/frontend`
- **Comando:** `npm start` (produção)

---

## 🔍 Troubleshooting

### Porta 8000 ou 3000 em uso
```bash
# Verificar processos
sudo lsof -i :8000
sudo lsof -i :3000

# Matar processo se necessário
sudo kill -9 <PID>
```

### Serviço não inicia
```bash
# Ver logs detalhados
sudo journalctl -u agenciakaizen-api.service -n 100 --no-pager
sudo journalctl -u agenciakaizen-frontend.service -n 100 --no-pager

# Verificar permissões
ls -la /var/www/agenciakaizen/backend
ls -la /var/www/agenciakaizen/frontend
```

### Nginx não redireciona corretamente
```bash
# Testar configuração
sudo nginx -t

# Recarregar
sudo systemctl reload nginx

# Ver logs
sudo tail -f /var/log/nginx/error.log
```

---

**Última atualização:** 2025-11-20



