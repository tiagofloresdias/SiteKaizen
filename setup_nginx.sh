#!/bin/bash

# Script de configuração do Nginx para www.agenciakaizen.com.br
# Agência Kaizen - Sistema de Migração WordPress para Wagtail

echo "Configurando Nginx para www.agenciakaizen.com.br..."

# Verificar se o Nginx está instalado
if ! command -v nginx &> /dev/null; then
    echo "Nginx não encontrado. Instalando..."
    sudo apt update
    sudo apt install -y nginx
fi

# Copiar configuração do site
echo "Copiando configuração do site..."
sudo cp /var/www/agenciakaizen/nginx-site2025.conf /etc/nginx/sites-available/www.agenciakaizen.com.br

# Criar link simbólico para habilitar o site
echo "Habilitando site..."
sudo ln -sf /etc/nginx/sites-available/www.agenciakaizen.com.br /etc/nginx/sites-enabled/

# Verificar configuração do Nginx
echo "Verificando configuração do Nginx..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "Configuração válida. Reiniciando Nginx..."
    sudo systemctl reload nginx
    echo "Nginx configurado com sucesso!"
    echo ""
    echo "Site disponível em: https://www.agenciakaizen.com.br"
    echo "Admin do Wagtail: https://www.agenciakaizen.com.br/admin/"
    echo "Usuário: admin"
    echo "Senha: admin123"
else
    echo "Erro na configuração do Nginx. Verifique os logs."
    exit 1
fi

# Verificar status do Nginx
echo ""
echo "Status do Nginx:"
sudo systemctl status nginx --no-pager

echo ""
echo "Configuração concluída!"
