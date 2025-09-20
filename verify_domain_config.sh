#!/bin/bash

# Script de verificação da configuração de domínio
# Agência Kaizen - Verificação de www.agenciakaizen.com.br

echo "🔍 Verificando configuração de domínio www.agenciakaizen.com.br"
echo "=============================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar se um arquivo contém o domínio correto
check_domain_in_file() {
    local file=$1
    local domain=$2
    local description=$3
    
    if [ -f "$file" ]; then
        if grep -q "$domain" "$file"; then
            echo -e "${GREEN}✅${NC} $description: $domain encontrado em $file"
        else
            echo -e "${RED}❌${NC} $description: $domain NÃO encontrado em $file"
        fi
    else
        echo -e "${YELLOW}⚠️${NC} $description: Arquivo $file não encontrado"
    fi
}

echo ""
echo "1. Verificando configurações Django..."
check_domain_in_file "src/agenciakaizen_cms/settings/base.py" "www.agenciakaizen.com.br" "ALLOWED_HOSTS"
check_domain_in_file "src/agenciakaizen_cms/settings/base.py" "www.agenciakaizen.com.br" "BASE_URL"
check_domain_in_file "src/agenciakaizen_cms/settings/production.py" "www.agenciakaizen.com.br" "ALLOWED_HOSTS (produção)"
check_domain_in_file "src/agenciakaizen_cms/settings/production.py" "www.agenciakaizen.com.br" "BASE_URL (produção)"

echo ""
echo "2. Verificando configuração Nginx..."
check_domain_in_file "nginx-site2025.conf" "www.agenciakaizen.com.br" "Server name principal"
check_domain_in_file "nginx-site2025.conf" "agenciakaizen.com.br" "Redirecionamento para www"

echo ""
echo "3. Verificando templates..."
check_domain_in_file "src/templates/base.html" "www.agenciakaizen.com.br" "URLs nos templates"

echo ""
echo "4. Verificando scripts CLI..."
check_domain_in_file "cli/migrate_wordpress.py" "www.agenciakaizen.com.br" "Exemplos de uso"
check_domain_in_file "cli/setup_cms.py" "www.agenciakaizen.com.br" "Configuração do site"

echo ""
echo "5. Verificando scripts de teste..."
check_domain_in_file "test_migration.sh" "www.agenciakaizen.com.br" "URLs de teste"
check_domain_in_file "setup_nginx.sh" "www.agenciakaizen.com.br" "Configuração Nginx"

echo ""
echo "6. Verificando documentação..."
check_domain_in_file "README.md" "www.agenciakaizen.com.br" "URLs na documentação"

echo ""
echo "7. Testando conectividade..."
echo "Testando www.agenciakaizen.com.br..."
if curl -s -o /dev/null -w "%{http_code}" https://www.agenciakaizen.com.br | grep -q "200\|301\|302"; then
    echo -e "${GREEN}✅${NC} www.agenciakaizen.com.br responde"
else
    echo -e "${YELLOW}⚠️${NC} www.agenciakaizen.com.br não responde (pode estar em desenvolvimento)"
fi

echo "Testando agenciakaizen.com.br..."
if curl -s -o /dev/null -w "%{http_code}" https://agenciakaizen.com.br | grep -q "200\|301\|302"; then
    echo -e "${GREEN}✅${NC} agenciakaizen.com.br responde"
else
    echo -e "${YELLOW}⚠️${NC} agenciakaizen.com.br não responde (pode estar em desenvolvimento)"
fi

echo ""
echo "8. Verificando configuração do servidor local..."
if netstat -tlnp | grep -q ":8745"; then
    echo -e "${GREEN}✅${NC} Servidor Django rodando na porta 8745"
else
    echo -e "${YELLOW}⚠️${NC} Servidor Django não está rodando na porta 8745"
fi

echo ""
echo "=============================================================="
echo "🎯 Resumo da configuração:"
echo "   • Domínio principal: www.agenciakaizen.com.br"
echo "   • Redirecionamento: agenciakaizen.com.br → www.agenciakaizen.com.br"
echo "   • HTTPS: Forçado para ambos os domínios"
echo "   • Servidor: Porta 8745 (Django/Wagtail)"
echo ""
echo "📋 Próximos passos:"
echo "   1. Configurar DNS para apontar para este servidor"
echo "   2. Instalar certificado SSL para *.agenciakaizen.com.br"
echo "   3. Executar: bash setup_nginx.sh"
echo "   4. Testar: bash test_migration.sh"
echo ""
echo "✅ Verificação concluída!"
