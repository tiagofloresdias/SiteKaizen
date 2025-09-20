# 🤖 Agência Kaizen CMS + Agente de IA

Sistema completo de gerenciamento de conteúdo com **Agente de IA avançado** para criação automática de posts e páginas evergreen, construído com Django, Wagtail e CrewAI.

## ✨ Principais Funcionalidades

### 🤖 Agente de IA Inteligente
- **Criação Automática de Conteúdo**: Posts de blog e páginas evergreen
- **3 Agentes Especializados**: Pesquisador, Escritor e Editor
- **Otimização SEO**: Conteúdo otimizado para mecanismos de busca
- **Integração Completa**: API REST integrada com o sistema de blog

### 📝 Sistema de Blog Completo
- **Gerenciamento de Posts**: Criação, edição e publicação
- **Páginas Evergreen**: Conteúdo atemporal otimizado para SEO
- **API REST**: Endpoints completos para integração
- **Categorias e Tags**: Organização inteligente de conteúdo

### 🎯 SEO e Performance
- **Otimização Automática**: Meta tags, títulos e descrições
- **Estrutura Semântica**: H1, H2, H3 otimizados
- **Call-to-Actions**: CTAs relevantes e estratégicos
- **Analytics Integrado**: Acompanhamento de performance

## 🚀 Instalação Rápida

### 1. Clone e Configure
```bash
git clone <repository-url>
cd agenciakaizen
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

### 2. Instale Dependências
```bash
pip install -r src/requirements.txt
```

### 3. Configure o Sistema
```bash
# Configure o agente de IA
python cli/setup_ai_agent.py

# Configure variáveis de ambiente
cp env.example .env
# Edite .env com suas chaves de API
```

### 4. Execute o Sistema
```bash
cd src
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🤖 Como Usar o Agente de IA

### Criar um Post de Blog
```bash
python cli/ai_content_agent.py \
  --topic "Marketing Digital 2024" \
  --audience "empresários" \
  --words 1500
```

### Criar Página Evergreen
```bash
python cli/ai_content_agent.py \
  --topic "Guia Completo de SEO" \
  --type evergreen \
  --keyword "seo" \
  --audience "pequenos empresários"
```

### Testar o Sistema
```bash
python cli/test_ai_agent.py
```

## 🔌 API REST

### Endpoints Principais
- `GET /api/blog/posts/` - Listar posts
- `POST /api/blog/posts/` - Criar post
- `GET /api/blog/evergreen/` - Listar páginas evergreen
- `GET /api/blog/stats/` - Estatísticas do blog

### Exemplo de Uso
```bash
# Listar posts
curl -H "Authorization: Token your_token" \
     http://localhost:8000/api/blog/posts/

# Criar post via API
curl -X POST \
     -H "Authorization: Token your_token" \
     -H "Content-Type: application/json" \
     -d '{"title": "Novo Post", "intro": "Introdução", "body": "<p>Conteúdo</p>"}' \
     http://localhost:8000/api/blog/posts/
```

## 🏗️ Arquitetura

```
Agência Kaizen CMS
├── 🤖 Agente de IA (CrewAI)
│   ├── 🔍 Pesquisador de Conteúdo
│   ├── ✍️ Escritor de Conteúdo
│   └── 📝 Editor de Conteúdo
├── 📝 Sistema de Blog (Wagtail)
│   ├── Posts do Blog
│   ├── Páginas Evergreen
│   └── Categorias e Tags
├── 🔌 API REST (Django REST Framework)
│   ├── Endpoints de Posts
│   ├── Endpoints de Páginas
│   └── Estatísticas e Analytics
└── 🎨 Frontend Responsivo
    ├── Templates Otimizados
    ├── Design Moderno
    └── SEO-Friendly
```

## 📚 Documentação Completa

### 🚀 Início Rápido
- [Instalação e Configuração](docs/instalacao.md)
- [Primeiros Passos](docs/primeiros-passos.md)
- [Configuração do Agente de IA](docs/agente-ia-setup.md)

### 🤖 Agente de IA
- [Visão Geral do Agente](docs/agente-ia-overview.md)
- [Como Usar o Agente](docs/agente-ia-uso.md)
- [API do Blog](docs/api-blog.md)
- [Tools e Integrações](docs/tools-integracao.md)

### 🔧 Desenvolvimento
- [Troubleshooting](docs/troubleshooting.md)
- [Contribuindo](docs/contribuindo.md)
- [Deploy](docs/deploy.md)

## 🎯 Casos de Uso

### Para Agências de Marketing
- Criação automática de conteúdo para clientes
- Páginas evergreen para SEO
- Integração com sistemas existentes

### Para Empresas
- Blog corporativo automatizado
- Conteúdo otimizado para SEO
- Redução de custos com criação de conteúdo

### Para Desenvolvedores
- API REST completa
- Integração com sistemas externos
- Automação de workflows de conteúdo

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```env
# OpenAI (obrigatório)
OPENAI_API_KEY=sk-your-key-here

# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Email
SENDGRID_API_KEY=your-sendgrid-key
DEFAULT_FROM_EMAIL=noreply@www.agenciakaizen.com.br

# API do Blog
BLOG_API_TOKEN=your-blog-token
```

### Personalização do Agente
```python
# Configurações personalizadas
CREWAI_CONFIG = {
    'MODEL_NAME': 'gpt-4o-mini',
    'TEMPERATURE': 0.7,
    'MAX_TOKENS': 4000,
}
```

## 📊 Métricas e Analytics

- **Posts Criados**: Contagem automática
- **Performance SEO**: Otimização contínua
- **Engajamento**: CTAs e conversões
- **Qualidade**: Revisão automática

## 🚨 Suporte e Troubleshooting

### Problemas Comuns
- [Troubleshooting Completo](docs/troubleshooting.md)
- [Teste do Sistema](cli/test_ai_agent.py)
- [Logs e Monitoramento](docs/monitoramento.md)

### Contato
- **Email**: comercial@www.agenciakaizen.com.br
- **Documentação**: [docs/](docs/)
- **Issues**: Repositório do projeto

## 🎉 Próximos Passos

1. **Configure sua chave da OpenAI** no arquivo `.env`
2. **Execute o teste** com `python cli/test_ai_agent.py`
3. **Crie seu primeiro post** com o agente de IA
4. **Explore a API** em `http://localhost:8000/api/blog/`
5. **Consulte a documentação** em `docs/`

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Desenvolvido com ❤️ pela Agência Kaizen**  
**Powered by CrewAI + OpenAI GPT-4**

