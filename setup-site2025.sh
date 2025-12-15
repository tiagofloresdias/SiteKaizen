#!/bin/bash
# Script para configurar e iniciar o site site2025.agenciakaizen.com.br

SUDO_PASSWORD="680143"

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🚀 Configurando site2025.agenciakaizen.com.br..."
echo ""

# Função para executar comandos sudo
run_sudo() {
    echo "$SUDO_PASSWORD" | sudo -S $1
}

# 1. Coletar arquivos estáticos
echo "1. Coletando arquivos estáticos..."
cd /var/www/agenciakaizen/src
source ../venv/bin/activate
python manage.py collectstatic --noinput --clear
echo -e "${GREEN}✅${NC} Arquivos estáticos coletados"

# 2. Criar diretórios de log se não existirem
echo ""
echo "2. Criando diretórios de log..."
mkdir -p /var/www/agenciakaizen/logs
chmod 755 /var/www/agenciakaizen/logs
echo -e "${GREEN}✅${NC} Diretórios de log criados"

# 3. Copiar arquivo de serviço systemd
echo ""
echo "3. Configurando serviço systemd..."
if run_sudo "cp /var/www/agenciakaizen/agenciakaizen-site2025.service /etc/systemd/system/"; then
    echo -e "${GREEN}✅${NC} Arquivo de serviço copiado"
else
    echo -e "${RED}❌${NC} Erro ao copiar arquivo de serviço"
    exit 1
fi

# 4. Recarregar systemd
echo ""
echo "4. Recarregando systemd..."
if run_sudo "systemctl daemon-reload"; then
    echo -e "${GREEN}✅${NC} Systemd recarregado"
else
    echo -e "${RED}❌${NC} Erro ao recarregar systemd"
    exit 1
fi

# 5. Habilitar serviço
echo ""
echo "5. Habilitando serviço..."
if run_sudo "systemctl enable agenciakaizen-site2025.service"; then
    echo -e "${GREEN}✅${NC} Serviço habilitado"
else
    echo -e "${RED}❌${NC} Erro ao habilitar serviço"
    exit 1
fi

# 6. Iniciar/Reiniciar serviço
echo ""
echo "6. Iniciando serviço..."
if run_sudo "systemctl restart agenciakaizen-site2025.service"; then
    echo -e "${GREEN}✅${NC} Serviço iniciado"
else
    echo -e "${RED}❌${NC} Erro ao iniciar serviço"
    exit 1
fi

# 7. Verificar status do serviço
echo ""
echo "7. Verificando status do serviço..."
sleep 2
if run_sudo "systemctl is-active --quiet agenciakaizen-site2025.service"; then
    echo -e "${GREEN}✅${NC} Serviço está rodando"
    run_sudo "systemctl status agenciakaizen-site2025.service --no-pager | head -10"
else
    echo -e "${RED}❌${NC} Serviço não está rodando"
    run_sudo "systemctl status agenciakaizen-site2025.service --no-pager"
    exit 1
fi

# 8. Verificar porta 8005
echo ""
echo "8. Verificando porta 8005..."
if ss -tlnp | grep -q ":8005"; then
    echo -e "${GREEN}✅${NC} Servidor escutando na porta 8005"
else
    echo -e "${YELLOW}⚠️${NC} Servidor não está escutando na porta 8005"
fi

# 9. Configurar Nginx
echo ""
echo "9. Configurando Nginx..."
if run_sudo "cp /var/www/agenciakaizen/nginx-site2025-agenciakaizen.conf /etc/nginx/sites-available/site2025.agenciakaizen.com.br"; then
    echo -e "${GREEN}✅${NC} Arquivo de configuração do Nginx copiado"
else
    echo -e "${RED}❌${NC} Erro ao copiar configuração do Nginx"
    exit 1
fi

# 10. Criar symlink se não existir
echo ""
echo "10. Habilitando site no Nginx..."
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

# 11. Testar configuração do Nginx
echo ""
echo "11. Testando configuração do Nginx..."
if run_sudo "nginx -t"; then
    echo -e "${GREEN}✅${NC} Configuração do Nginx está válida"
else
    echo -e "${RED}❌${NC} Erro na configuração do Nginx"
    exit 1
fi

# 12. Recarregar Nginx
echo ""
echo "12. Recarregando Nginx..."
if run_sudo "systemctl reload nginx"; then
    echo -e "${GREEN}✅${NC} Nginx recarregado"
else
    echo -e "${RED}❌${NC} Erro ao recarregar Nginx"
    exit 1
fi

# 13. Verificar conectividade
echo ""
echo "13. Verificando conectividade..."
sleep 2
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
echo "  - Serviço: agenciakaizen-site2025.service"
echo "  - Porta: 8005"
echo "  - URL: http://site2025.agenciakaizen.com.br"
echo ""
echo "Comandos úteis:"
echo "  sudo systemctl status agenciakaizen-site2025.service"
echo "  sudo systemctl restart agenciakaizen-site2025.service"
echo "  sudo systemctl logs -f agenciakaizen-site2025.service"
echo "  sudo tail -f /var/www/agenciakaizen/logs/gunicorn-error.log"
echo "=============================================================="


