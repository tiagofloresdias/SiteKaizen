#!/bin/bash

echo "🔧 Corrigindo configuração do nginx para agenciakaizen.com.br"

# Criar configuração temporária sem SSL
cat > /tmp/agenciakaizen-temp.conf << 'EOF'
# Configuração temporária para agenciakaizen.com.br (HTTP apenas - sem SSL)

# Redirecionar agenciakaizen.com.br para www.agenciakaizen.com.br
server {
    listen 80;
    server_name agenciakaizen.com.br;
    
    # Redirecionar para www
    return 301 http://www.agenciakaizen.com.br$request_uri;
}

# Site principal - www.agenciakaizen.com.br
server {
    listen 80;
    server_name www.agenciakaizen.com.br;
    
    # Headers de segurança
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Configurações do Django/Wagtail
    client_max_body_size 50M;
    
    # Arquivos estáticos
    location /static/ {
        alias /var/www/agenciakaizen/src/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Arquivos de mídia
    location /media/ {
        alias /var/www/agenciakaizen/src/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Favicon
    location = /favicon.ico {
        alias /var/www/agenciakaizen/src/static/favicon.ico;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Aplicação Django/Wagtail
    location / {
        proxy_pass http://127.0.0.1:8003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Buffer settings
        proxy_buffering on;
        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }
    
    # Logs
    access_log /var/log/nginx/www.agenciakaizen.com.br.access.log;
    error_log /var/log/nginx/www.agenciakaizen.com.br.error.log;
}
EOF

echo "✅ Configuração temporária criada"

# Fazer backup da configuração atual
echo "📦 Fazendo backup da configuração atual..."
sudo cp /etc/nginx/sites-available/agenciakaizen.com.br /etc/nginx/sites-available/agenciakaizen.com.br.backup.$(date +%Y%m%d_%H%M%S)

# Desabilitar site atual
echo "🚫 Desabilitando site atual..."
sudo rm -f /etc/nginx/sites-enabled/agenciakaizen.com.br

# Copiar nova configuração
echo "📝 Instalando nova configuração..."
sudo cp /tmp/agenciakaizen-temp.conf /etc/nginx/sites-available/agenciakaizen.com.br

# Habilitar novo site
echo "✅ Habilitando novo site..."
sudo ln -sf /etc/nginx/sites-available/agenciakaizen.com.br /etc/nginx/sites-enabled/

# Testar configuração
echo "🧪 Testando configuração do nginx..."
if sudo nginx -t; then
    echo "✅ Configuração do nginx está correta!"
    
    # Recarregar nginx
    echo "🔄 Recarregando nginx..."
    sudo systemctl reload nginx
    
    echo "🎉 Site agenciakaizen.com.br configurado com sucesso!"
    echo "🌐 Acesse: http://www.agenciakaizen.com.br"
else
    echo "❌ Erro na configuração do nginx!"
    exit 1
fi