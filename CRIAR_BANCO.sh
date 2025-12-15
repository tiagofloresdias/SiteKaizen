#!/bin/bash
# Script para criar banco de dados agenciakaizen

SUDO_PASSWORD="680143"

echo "🗄️ Criando banco de dados agenciakaizen..."
echo ""

# Criar banco de dados
echo "$SUDO_PASSWORD" | sudo -S -u postgres psql -c "CREATE DATABASE agenciakaizen;" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Banco 'agenciakaizen' criado com sucesso!"
else
    echo "⚠️ Banco pode já existir ou erro ao criar"
    echo "$SUDO_PASSWORD" | sudo -S -u postgres psql -c "SELECT 1 FROM pg_database WHERE datname='agenciakaizen';" 2>&1 | grep -q "1 row" && echo "✅ Banco já existe"
fi

echo ""
echo "Agora rode as migrations:"
echo "  cd /var/www/agenciakaizen/backend"
echo "  source ../venv/bin/activate"
echo "  alembic upgrade head"



