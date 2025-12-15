# Frontend Next.js - Agência Kaizen

Frontend moderno em Next.js 14+ com App Router para o site da Agência Kaizen.

## 🚀 Iniciando

### Instalar dependências

```bash
npm install
```

### Rodar em desenvolvimento

```bash
npm run dev
```

O site estará disponível em `http://localhost:3000`

### Build para produção

```bash
npm run build
npm start
```

## 📁 Estrutura

```
frontend/
├── app/                    # App Router (Next.js 14+)
│   ├── layout.tsx         # Layout raiz
│   ├── page.tsx           # Homepage
│   ├── globals.css        # Estilos globais
│   ├── nossas-empresas/   # Página de empresas
│   ├── blog/              # Página de blog
│   ├── onde-estamos/      # Página de localizações
│   ├── contato/           # Página de contato
│   ├── sitemap.ts         # Sitemap dinâmico
│   └── robots.ts          # Robots.txt
│
├── components/             # Componentes React
│   ├── layout/            # Header, Footer, Navigation
│   └── seo/               # Componentes SEO (JSON-LD, Breadcrumb)
│
├── lib/                    # Utilities
│   └── api.ts             # Cliente API FastAPI
│
├── theme/                  # Design tokens
│   └── tokens.ts          # Tokens de design (gerado automaticamente)
│
└── public/                 # Assets estáticos
    ├── img/               # Imagens
    └── fonts/            # Fontes
```

## 🎨 Design Tokens

Os design tokens estão definidos em `tailwind.config.ts` e `app/globals.css`.

Cores principais:
- `primary`: #D62042 (rosa Kaizen)
- `primary-light`: #ff6b6b
- `dark`: #0b0b0c
- `text`: #e9eaee

## 🔌 API

O frontend consome a API FastAPI em `http://localhost:8000/api/v1`.

Configure a URL da API em `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

## 📱 SEO

- **JSON-LD**: Schemas Organization, LocalBusiness, Article, BreadcrumbList
- **Meta tags**: OG, Twitter Cards, canonical
- **Sitemap**: Dinâmico via `/sitemap.xml`
- **Robots**: Configurado via `/robots.txt`

## 🛠️ Tecnologias

- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- React 18+



