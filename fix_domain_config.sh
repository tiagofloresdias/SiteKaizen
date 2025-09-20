#!/bin/bash

# Script para corrigir a configuração do domínio agenciakaizen.com.br
# Este script mostra os comandos que precisam ser executados

echo "🔧 Corrigindo configuração do domínio agenciakaizen.com.br"
echo "=========================================================="

echo ""
echo "O problema identificado:"
echo "• A configuração padrão do Nginx está capturando todos os domínios"
echo "• O domínio agenciakaizen.com.br está sendo interceptado pela configuração padrão"
echo "• Precisamos criar uma configuração específica para o domínio"
echo ""

echo "📋 Comandos que precisam ser executados:"
echo ""

echo "1. Copiar configuração do domínio:"
echo "   sudo cp /var/www/agenciakaizen/nginx-agenciakaizen.conf /etc/nginx/sites-available/agenciakaizen.com.br"
echo ""

echo "2. Habilitar o site:"
echo "   sudo ln -sf /etc/nginx/sites-available/agenciakaizen.com.br /etc/nginx/sites-enabled/"
echo ""

echo "3. Desabilitar a configuração padrão (opcional):"
echo "   sudo rm /etc/nginx/sites-enabled/default"
echo ""

echo "4. Verificar configuração:"
echo "   sudo nginx -t"
echo ""

echo "5. Recarregar Nginx:"
echo "   sudo systemctl reload nginx"
echo ""

echo "6. Configurar SSL (se necessário):"
echo "   sudo certbot --nginx -d agenciakaizen.com.br -d www.agenciakaizen.com.br"
echo ""

echo "7. Iniciar servidor Django (se não estiver rodando):"
echo "   cd /var/www/agenciakaizen/src"
echo "   source ../venv/bin/activate"
echo "   python manage.py runserver 0.0.0.0:8745"
echo ""

echo "🎯 Após executar esses comandos:"
echo "• agenciakaizen.com.br → redirecionará para www.agenciakaizen.com.br"
echo "• www.agenciakaizen.com.br → mostrará o site Wagtail CMS"
echo "• HTTPS será obrigatório para ambos os domínios"
echo ""

echo "📝 Arquivos criados:"
echo "• nginx-agenciakaizen.conf - Configuração do Nginx"
echo "• setup_agenciakaizen_domain.sh - Script de configuração automática"
echo "• fix_domain_config.sh - Este arquivo com instruções"
echo ""

echo "✅ Instruções prontas para execução!"
