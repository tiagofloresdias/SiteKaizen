#!/bin/bash

# Script para configurar o domínio agenciakaizen.com.br
# Agência Kaizen - Configuração de Domínio

echo "🔧 Configurando domínio agenciakaizen.com.br para Wagtail CMS"
echo "=============================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para executar comandos com sudo
run_sudo() {
    echo "Executando: $1"
    if sudo -S <<< "" $1 2>/dev/null; then
        echo -e "${GREEN}✅${NC} Comando executado com sucesso"
        return 0
    else
        echo -e "${RED}❌${NC} Erro ao executar comando"
        return 1
    fi
}

# 1. Verificar se o Nginx está rodando
echo ""
echo "1. Verificando Nginx..."
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✅${NC} Nginx está rodando"
else
    echo -e "${YELLOW}⚠️${NC} Nginx não está rodando. Iniciando..."
    run_sudo "systemctl start nginx"
fi

# 2. Copiar configuração do domínio
echo ""
echo "2. Copiando configuração do domínio..."
if run_sudo "cp /var/www/agenciakaizen/nginx-agenciakaizen.conf /etc/nginx/sites-available/agenciakaizen.com.br"; then
    echo -e "${GREEN}✅${NC} Configuração copiada"
else
    echo -e "${RED}❌${NC} Erro ao copiar configuração"
    exit 1
fi

# 3. Habilitar site
echo ""
echo "3. Habilitando site..."
if run_sudo "ln -sf /etc/nginx/sites-available/agenciakaizen.com.br /etc/nginx/sites-enabled/"; then
    echo -e "${GREEN}✅${NC} Site habilitado"
else
    echo -e "${RED}❌${NC} Erro ao habilitar site"
    exit 1
fi

# 4. Verificar configuração do Nginx
echo ""
echo "4. Verificando configuração do Nginx..."
if run_sudo "nginx -t"; then
    echo -e "${GREEN}✅${NC} Configuração do Nginx válida"
else
    echo -e "${RED}❌${NC} Erro na configuração do Nginx"
    echo "Verifique os logs: sudo nginx -t"
    exit 1
fi

# 5. Recarregar Nginx
echo ""
echo "5. Recarregando Nginx..."
if run_sudo "systemctl reload nginx"; then
    echo -e "${GREEN}✅${NC} Nginx recarregado"
else
    echo -e "${RED}❌${NC} Erro ao recarregar Nginx"
    exit 1
fi

# 6. Verificar se o servidor Django está rodando
echo ""
echo "6. Verificando servidor Django..."
if ss -tlnp | grep -q ":8745"; then
    echo -e "${GREEN}✅${NC} Servidor Django rodando na porta 8745"
else
    echo -e "${YELLOW}⚠️${NC} Servidor Django não está rodando na porta 8745"
    echo "Iniciando servidor Django..."
    cd /var/www/agenciakaizen/src
    source ../venv/bin/activate
    nohup python manage.py runserver 0.0.0.0:8745 > /var/www/agenciakaizen/logs/django.log 2>&1 &
    sleep 3
    if ss -tlnp | grep -q ":8745"; then
        echo -e "${GREEN}✅${NC} Servidor Django iniciado"
    else
        echo -e "${RED}❌${NC} Erro ao iniciar servidor Django"
    fi
fi

# 7. Verificar configuração de SSL
echo ""
echo "7. Verificando configuração de SSL..."
if [ -f "/etc/letsencrypt/live/agenciakaizen.com.br/fullchain.pem" ]; then
    echo -e "${GREEN}✅${NC} Certificado SSL encontrado"
else
    echo -e "${YELLOW}⚠️${NC} Certificado SSL não encontrado"
    echo "Para configurar SSL, execute:"
    echo "sudo certbot --nginx -d agenciakaizen.com.br -d www.agenciakaizen.com.br"
fi

# 8. Testar conectividade
echo ""
echo "8. Testando conectividade..."
echo "Testando HTTP (deve redirecionar para HTTPS)..."
if curl -s -o /dev/null -w "%{http_code}" http://agenciakaizen.com.br | grep -q "301\|302"; then
    echo -e "${GREEN}✅${NC} Redirecionamento HTTP funcionando"
else
    echo -e "${YELLOW}⚠️${NC} Redirecionamento HTTP não funcionando"
fi

echo "Testando HTTPS..."
if curl -s -o /dev/null -w "%{http_code}" https://www.agenciakaizen.com.br | grep -q "200\|301\|302"; then
    echo -e "${GREEN}✅${NC} HTTPS funcionando"
else
    echo -e "${YELLOW}⚠️${NC} HTTPS não funcionando (pode precisar de certificado SSL)"
fi

echo ""
echo "=============================================================="
echo "🎯 Configuração concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Configurar DNS para apontar agenciakaizen.com.br para este servidor"
echo "2. Configurar SSL: sudo certbot --nginx -d agenciakaizen.com.br -d www.agenciakaizen.com.br"
echo "3. Testar: https://www.agenciakaizen.com.br"
echo ""
echo "🔗 URLs:"
echo "   • Site principal: https://www.agenciakaizen.com.br"
echo "   • Admin: https://www.agenciakaizen.com.br/admin/"
echo "   • Redirecionamento: agenciakaizen.com.br → www.agenciakaizen.com.br"
echo ""
echo "✅ Configuração concluída!"
