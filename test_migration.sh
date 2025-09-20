#!/bin/bash

# Script de teste da migração WordPress para Wagtail
# Agência Kaizen - Sistema de Migração

echo "Testando migração do WordPress para Wagtail..."
echo "=============================================="

# Ativar ambiente virtual
cd /var/www/agenciakaizen
source venv/bin/activate

# Teste 1: Dry run da migração
echo ""
echo "1. Testando migração com dry-run..."
python cli/migrate_wordpress.py https://www.agenciakaizen.com.br --dry-run --log-level INFO

# Teste 2: Verificar conexão com WordPress
echo ""
echo "2. Testando conexão com WordPress..."
curl -s -o /dev/null -w "%{http_code}" https://www.agenciakaizen.com.br/wp-json/wp/v2/

# Teste 3: Verificar estrutura do site
echo ""
echo "3. Verificando estrutura do site Wagtail..."
cd src
python manage.py check

# Teste 4: Verificar se o servidor está rodando
echo ""
echo "4. Verificando se o servidor está rodando na porta 8745..."
netstat -tlnp | grep :8745

echo ""
echo "Testes concluídos!"
echo ""
echo "Para executar a migração real:"
echo "python cli/migrate_wordpress.py https://www.agenciakaizen.com.br"
echo ""
echo "Para configurar o Nginx:"
echo "bash setup_nginx.sh"
