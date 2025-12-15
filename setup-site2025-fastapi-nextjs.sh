#!/bin/bash
# Script para configurar e iniciar o site site2025.agenciakaizen.com.br
# FastAPI Backend + Next.js Frontend

SUDO_PASSWORD="680143"

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🚀 Configurando site2025.agenciakaizen.com.br (FastAPI + Next.js)..."
echo ""

# Função para executar comandos sudo
run_sudo() {
    echo "$SUDO_PASSWORD" | sudo -S $1
}

# 1. Verificar se venv existe (usar venv da raiz)
echo "1. Verificando venv..."
if [ ! -d "/var/www/agenciakaizen/venv" ]; then
    echo -e "${YELLOW}⚠️${NC} Criando venv na raiz..."
    cd /var/www/agenciakaizen
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}✅${NC} Venv criado"
else
    echo -e "${GREEN}✅${NC} Venv existe (usando /var/www/agenciakaizen/venv)"
fi

# Instalar dependências do FastAPI no venv existente
echo ""
echo "1.1. Instalando dependências do FastAPI..."
cd /var/www/agenciakaizen/backend
source ../venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅${NC} Dependências do FastAPI instaladas no venv"
else
    echo -e "${YELLOW}⚠️${NC} Alguns pacotes podem não ter sido instalados"
fi

# 2. Verificar se node_modules do frontend existe
echo ""
echo "2. Verificando frontend..."
if [ ! -d "/var/www/agenciakaizen/frontend/node_modules" ]; then
    echo -e "${YELLOW}⚠️${NC} Instalando dependências do frontend..."
    cd /var/www/agenciakaizen/frontend
    npm install
    echo -e "${GREEN}✅${NC} Dependências do frontend instaladas"
else
    echo -e "${GREEN}✅${NC} Dependências do frontend existem"
fi

# 3. Criar diretórios de log se não existirem
echo ""
echo "3. Criando diretórios de log..."
mkdir -p /var/www/agenciakaizen/logs
chmod 755 /var/www/agenciakaizen/logs
echo -e "${GREEN}✅${NC} Diretórios de log criados"

# 4. Copiar arquivos de serviço systemd
echo ""
echo "4. Configurando serviços systemd..."

# Backend FastAPI
if run_sudo "cp /var/www/agenciakaizen/agenciakaizen-api.service /etc/systemd/system/"; then
    echo -e "${GREEN}✅${NC} Serviço FastAPI copiado"
else
    echo -e "${RED}❌${NC} Erro ao copiar serviço FastAPI"
    exit 1
fi

# Frontend Next.js
if run_sudo "cp /var/www/agenciakaizen/agenciakaizen-frontend.service /etc/systemd/system/"; then
    echo -e "${GREEN}✅${NC} Serviço Next.js copiado"
else
    echo -e "${RED}❌${NC} Erro ao copiar serviço Next.js"
    exit 1
fi

# 5. Recarregar systemd
echo ""
echo "5. Recarregando systemd..."
if run_sudo "systemctl daemon-reload"; then
    echo -e "${GREEN}✅${NC} Systemd recarregado"
else
    echo -e "${RED}❌${NC} Erro ao recarregar systemd"
    exit 1
fi

# 6. Habilitar serviços
echo ""
echo "6. Habilitando serviços..."
if run_sudo "systemctl enable agenciakaizen-api.service agenciakaizen-frontend.service"; then
    echo -e "${GREEN}✅${NC} Serviços habilitados"
else
    echo -e "${RED}❌${NC} Erro ao habilitar serviços"
    exit 1
fi

# 7. Build do Next.js (se necessário)
echo ""
echo "7. Fazendo build do Next.js..."
cd /var/www/agenciakaizen/frontend
if [ ! -d ".next" ]; then
    npm run build
    echo -e "${GREEN}✅${NC} Build do Next.js concluído"
else
    echo -e "${GREEN}✅${NC} Build do Next.js já existe"
fi

# 8. Iniciar/Reiniciar serviços
echo ""
echo "8. Iniciando serviços..."

# Backend FastAPI
if run_sudo "systemctl restart agenciakaizen-api.service"; then
    echo -e "${GREEN}✅${NC} Serviço FastAPI iniciado"
else
    echo -e "${RED}❌${NC} Erro ao iniciar serviço FastAPI"
    exit 1
fi

sleep 2

# Frontend Next.js
if run_sudo "systemctl restart agenciakaizen-frontend.service"; then
    echo -e "${GREEN}✅${NC} Serviço Next.js iniciado"
else
    echo -e "${RED}❌${NC} Erro ao iniciar serviço Next.js"
    exit 1
fi

# 9. Verificar status dos serviços
echo ""
echo "9. Verificando status dos serviços..."
sleep 3

# Backend
if run_sudo "systemctl is-active --quiet agenciakaizen-api.service"; then
    echo -e "${GREEN}✅${NC} FastAPI está rodando"
else
    echo -e "${RED}❌${NC} FastAPI não está rodando"
    run_sudo "systemctl status agenciakaizen-api.service --no-pager | head -15"
fi

# Frontend
if run_sudo "systemctl is-active --quiet agenciakaizen-frontend.service"; then
    echo -e "${GREEN}✅${NC} Next.js está rodando"
else
    echo -e "${RED}❌${NC} Next.js não está rodando"
    run_sudo "systemctl status agenciakaizen-frontend.service --no-pager | head -15"
fi

# 10. Verificar portas
echo ""
echo "10. Verificando portas..."
echo "🔍 Portas escolhidas (para evitar conflitos):"
echo "   - FastAPI: 8006 (porta livre)"
echo "   - Next.js: 3001 (porta livre)"
echo ""
if ss -tlnp | grep -q ":8006"; then
    echo -e "${GREEN}✅${NC} FastAPI escutando na porta 8006"
else
    echo -e "${YELLOW}⚠️${NC} FastAPI não está escutando na porta 8006"
fi

if ss -tlnp | grep -q ":3001"; then
    echo -e "${GREEN}✅${NC} Next.js escutando na porta 3001"
else
    echo -e "${YELLOW}⚠️${NC} Next.js não está escutando na porta 3001"
fi

# Verificar se há conflito com portas existentes
echo ""
echo "📊 Portas em uso no sistema:"
ss -tlnp | grep -E ":(800[0-9]|300[0-9])" | awk '{print "   Porta " $4}' | cut -d: -f2

# 11. Configurar Nginx
echo ""
echo "11. Configurando Nginx..."
if run_sudo "cp /var/www/agenciakaizen/nginx-site2025-fastapi-nextjs.conf /etc/nginx/sites-available/site2025.agenciakaizen.com.br"; then
    echo -e "${GREEN}✅${NC} Arquivo de configuração do Nginx copiado"
else
    echo -e "${RED}❌${NC} Erro ao copiar configuração do Nginx"
    exit 1
fi

# 12. Criar symlink se não existir
echo ""
echo "12. Habilitando site no Nginx..."
if [ ! -L /etc/nginx/sites-enabled/site2025.agenciakaizen.com.br ]; then
    if run_sudo "ln -s /etc/nginx/sites-available/site2025.agenciakaizen.com.br /etc/nginx/sites-enabled/"; then
        echo -e "${GREEN}✅${NC} Site habilitado no Nginx"
    else
        echo -e "${RED}❌${NC} Erro ao habilitar site no Nginx"
        exit 1
    fi
else
    echo -e "${GREEN}✅${NC} Site já está habilitado no Nginx"
fi

# 13. Testar configuração do Nginx
echo ""
echo "13. Testando configuração do Nginx..."
if run_sudo "nginx -t"; then
    echo -e "${GREEN}✅${NC} Configuração do Nginx está válida"
else
    echo -e "${RED}❌${NC} Erro na configuração do Nginx"
    exit 1
fi

# 14. Recarregar Nginx
echo ""
echo "14. Recarregando Nginx..."
if run_sudo "systemctl reload nginx"; then
    echo -e "${GREEN}✅${NC} Nginx recarregado"
else
    echo -e "${RED}❌${NC} Erro ao recarregar Nginx"
    exit 1
fi

# 15. Verificar conectividade
echo ""
echo "15. Verificando conectividade..."
sleep 3
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://site2025.agenciakaizen.com.br || echo "000")
if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ]; then
    echo -e "${GREEN}✅${NC} Site respondendo (HTTP $HTTP_CODE)"
else
    echo -e "${YELLOW}⚠️${NC} Site retornou HTTP $HTTP_CODE (pode levar alguns segundos para iniciar)"
fi

echo ""
echo "=============================================================="
echo -e "${GREEN}✅${NC} Configuração concluída!"
echo ""
echo "Informações:"
echo "  - Backend (FastAPI): agenciakaizen-api.service (porta 8006 - escolhida para evitar conflitos)"
echo "  - Frontend (Next.js): agenciakaizen-frontend.service (porta 3001 - escolhida para evitar conflitos)"
echo "  - URL: http://site2025.agenciakaizen.com.br"
echo ""
echo "Comandos úteis:"
echo "  sudo systemctl status agenciakaizen-api.service"
echo "  sudo systemctl status agenciakaizen-frontend.service"
echo "  sudo journalctl -u agenciakaizen-api.service -f"
echo "  sudo journalctl -u agenciakaizen-frontend.service -f"
echo "  sudo systemctl restart agenciakaizen-api.service"
echo "  sudo systemctl restart agenciakaizen-frontend.service"
echo "=============================================================="

