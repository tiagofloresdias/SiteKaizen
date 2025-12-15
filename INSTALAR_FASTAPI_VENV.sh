#!/bin/bash
# Script para instalar dependências do FastAPI no venv existente

echo "🔧 Instalando dependências do FastAPI no venv existente..."
echo ""

cd /var/www/agenciakaizen

# Ativar venv existente
source venv/bin/activate

# Verificar Python
echo "📦 Python: $(python --version)"
echo "📍 Venv: $(which python)"
echo ""

# Instalar dependências do FastAPI
echo "📥 Instalando dependências do backend FastAPI..."
cd backend
pip install -r requirements.txt

echo ""
echo "✅ Dependências instaladas!"
echo ""
echo "Verificando instalação:"
pip list | grep -E "(fastapi|uvicorn|sqlalchemy|alembic)"

echo ""
echo "Para testar:"
echo "  cd /var/www/agenciakaizen/backend"
echo "  source ../venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8006"



