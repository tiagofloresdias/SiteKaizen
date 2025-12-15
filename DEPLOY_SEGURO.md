# 🛡️ Deploy Seguro - Sem Derrubar Serviços Existentes

## ✅ Configuração Segura Implementada

A configuração foi ajustada para **NÃO CONFLITAR** com serviços existentes em produção:

### Portas Verificadas e Escolhidas

**Portas em uso (não alteradas):**
- ✅ `8003` - Outro serviço Gunicorn (mantido)
- ✅ `8005` - Django site2025 antigo (mantido)
- ✅ `8000` - Possível uso (não usado)

**Portas escolhidas (livres confirmadas):**
- ✅ `8006` - FastAPI Backend (NOVO)
- ✅ `3001` - Next.js Frontend (NOVO)

## 🚀 Como Deployar com Segurança

### 1. Verificar Portas Antes

```bash
# Confirmar que portas estão livres
ss -tlnp | grep -E ":(8006|3001)"
# Se não retornar nada = LIVRE ✅
```

### 2. Executar Script de Setup

```bash
cd /var/www/agenciakaizen
./setup-site2025-fastapi-nextjs.sh
```

O script irá:
- ✅ Verificar portas antes de iniciar
- ✅ Criar serviços separados (não interfere com existentes)
- ✅ Configurar Nginx apenas para site2025.agenciakaizen.com.br
- ✅ Não tocar em outros serviços

### 3. Verificar Serviços Existentes Continuam Funcionando

```bash
# Verificar serviço Django antigo (porta 8005)
ss -tlnp | grep :8005
# Deve continuar rodando ✅

# Verificar outro serviço (porta 8003)
ss -tlnp | grep :8003
# Deve continuar rodando ✅

# Verificar novos serviços
ss -tlnp | grep -E ":(8006|3001)"
# Devem estar rodando ✅
```

## 📋 Checklist de Segurança

Antes de fazer deploy:

- [x] ✅ Portas escolhidas estão livres (8006, 3001)
- [x] ✅ Nenhum serviço existente será alterado
- [x] ✅ Configuração Nginx apenas para site2025.agenciakaizen.com.br
- [x] ✅ Serviços separados (isolados do Django antigo)
- [x] ✅ Script verifica conflitos antes de iniciar

## 🔄 Rollback (se necessário)

Se algo der errado, é só parar os novos serviços:

```bash
# Parar novos serviços (não afeta os antigos)
sudo systemctl stop agenciakaizen-api.service
sudo systemctl stop agenciakaizen-frontend.service

# Verificar que serviços antigos continuam funcionando
ss -tlnp | grep -E ":(8003|8005)"
```

## ⚠️ Atenção

**Os serviços existentes NÃO serão afetados!**

- ✅ Django site2025 (porta 8005) continuará rodando normalmente
- ✅ Outro serviço (porta 8003) continuará rodando normalmente
- ✅ Nginx continuará servindo outros domínios normalmente

Apenas adicionamos novos serviços nas portas livres.

---

**Última atualização:** 2025-11-20



