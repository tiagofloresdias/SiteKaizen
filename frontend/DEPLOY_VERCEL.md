# 🚀 Guia de Deploy na Vercel - Frontend Next.js

## ✅ Status: Pronto para Deploy!

O frontend está **100% configurado** para deploy na Vercel com:
- ✅ Next.js 14 com App Router
- ✅ Tailwind CSS moderno
- ✅ TypeScript
- ✅ Integração com API FastAPI
- ✅ **SEM CONFLITOS DE PORTA** (Vercel gerencia automaticamente)

## 🎯 Passo a Passo para Deploy

### 1. Preparar Repositório

```bash
cd /var/www/agenciakaizen/frontend
git init  # Se ainda não tiver
git add .
git commit -m "Frontend Next.js pronto para Vercel"
git remote add origin <seu-repositorio>
git push -u origin main
```

### 2. Conectar na Vercel

1. Acesse [vercel.com](https://vercel.com) e faça login
2. Clique em **"Add New Project"**
3. Importe o repositório do GitHub/GitLab
4. Configure:
   - **Framework Preset**: Next.js (detectado automaticamente)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (automático)
   - **Output Directory**: `.next` (automático)

### 3. Configurar Variáveis de Ambiente

Na Vercel Dashboard → Settings → Environment Variables, adicione:

```env
NEXT_PUBLIC_API_URL=https://site2025.agenciakaizen.com.br/api/v1
NEXT_PUBLIC_SITE_URL=https://site2025.agenciakaizen.com.br
```

**Importante**: Configure para **Production**, **Preview** e **Development**

### 4. Deploy!

Clique em **"Deploy"** e aguarde. A Vercel vai:
- ✅ Instalar dependências
- ✅ Fazer build do projeto
- ✅ Deploy automático
- ✅ Gerar URL de produção

## 🎨 Características do Frontend

### Design System Moderno

- **Cores**: Rosa Kaizen (#D62042) com gradientes
- **Tipografia**: Inter + Poppins (Google Fonts)
- **Componentes**: Reutilizáveis e modulares
- **Animações**: Framer Motion para transições suaves

### Performance

- ✅ **ISR** (Incremental Static Regeneration)
- ✅ **Image Optimization** automático
- ✅ **Code Splitting** automático
- ✅ **Font Optimization**
- ✅ **Compression** habilitado

### SEO

- ✅ Metadata dinâmica
- ✅ Open Graph tags
- ✅ Twitter Cards
- ✅ JSON-LD Schema
- ✅ Sitemap automático

## 🔗 Integração com Backend

O frontend consome a **API FastAPI** que está no servidor:

```
Frontend (Vercel) → API FastAPI (Servidor) → PostgreSQL
```

**Sem conflitos de porta** porque:
- Vercel usa HTTPS na porta 443 (padrão)
- API FastAPI no servidor na porta 8005 (interno)
- Comunicação via HTTPS externo

## 📱 Responsividade

- ✅ Mobile First
- ✅ Breakpoints: sm, md, lg, xl, 2xl
- ✅ Imagens otimizadas
- ✅ Touch-friendly

## 🔒 Segurança

- ✅ Headers de segurança configurados
- ✅ XSS Protection
- ✅ Content Type Options
- ✅ Frame Options
- ✅ Referrer Policy

## 🚀 Comandos Úteis

```bash
# Desenvolvimento local
npm run dev

# Build
npm run build

# Type check
npm run type-check

# Lint
npm run lint
```

## 📊 Monitoramento

Após o deploy, você terá:
- ✅ Analytics na Vercel Dashboard
- ✅ Logs em tempo real
- ✅ Performance metrics
- ✅ Error tracking

## 🆘 Troubleshooting

### Build falha

1. Verificar variáveis de ambiente
2. Verificar logs na Vercel
3. Testar build local: `npm run build`

### API não responde

1. Verificar `NEXT_PUBLIC_API_URL`
2. Verificar CORS no backend
3. Testar API diretamente

### Imagens não carregam

1. Verificar domínios em `next.config.js`
2. Usar componente `Image` do Next.js
3. Verificar se estão em `public/`

## ✨ Próximos Passos

1. ✅ Deploy na Vercel
2. ⏳ Configurar domínio customizado
3. ⏳ Adicionar mais componentes UI
4. ⏳ Implementar animações avançadas
5. ⏳ Otimizar ainda mais performance

## 🎉 Resultado Final

Você terá um frontend **impecável** com:
- Interface moderna e responsiva
- Performance otimizada
- SEO completo
- Deploy automático
- **Zero conflitos de porta**

---

**Pronto para decolar! 🚀**

