# 📚 Documentação - Agência Kaizen CMS

Bem-vindo à documentação completa do sistema Agência Kaizen CMS com Agente de IA para Criação de Conteúdos.

## 🗂️ Índice da Documentação

### 🚀 Início Rápido
- [Instalação e Configuração](instalacao.md)
- [Primeiros Passos](primeiros-passos.md)
- [Configuração do Agente de IA](agente-ia-setup.md)

### 🤖 Agente de IA
- [Visão Geral do Agente](agente-ia-overview.md)
- [Como Usar o Agente](agente-ia-uso.md)
- [API do Blog](api-blog.md)
- [Tools e Integrações](tools-integracao.md)

### 🏗️ Arquitetura
- [Estrutura do Projeto](arquitetura.md)
- [Sistema de Blog](sistema-blog.md)
- [API REST](api-rest.md)
- [Configurações](configuracoes.md)

### 📖 Guias de Uso
- [Criação de Posts](criacao-posts.md)
- [SEO e Otimização](seo-otimizacao.md)
- [Gerenciamento de Conteúdo](gerenciamento-conteudo.md)
- [Troubleshooting](troubleshooting.md)

### 🔧 Desenvolvimento
- [Contribuindo](contribuindo.md)
- [Testes](testes.md)
- [Deploy](deploy.md)
- [Changelog](changelog.md)

## 🎯 Visão Geral

O **Agência Kaizen CMS** é um sistema completo de gerenciamento de conteúdo construído com Django e Wagtail, integrado com um **Agente de IA avançado** para criação automática de conteúdos usando CrewAI.

### ✨ Principais Funcionalidades

- **🤖 Agente de IA Inteligente**: Criação automática de posts e páginas evergreen
- **📝 Sistema de Blog Completo**: Gerenciamento de posts com Wagtail CMS
- **🔌 API REST Integrada**: Endpoints para integração com sistemas externos
- **🎯 SEO Otimizado**: Criação de conteúdo otimizado para mecanismos de busca
- **📊 Analytics Integrado**: Acompanhamento de performance do conteúdo
- **🌐 Multilíngue**: Suporte a múltiplos idiomas

### 🏛️ Arquitetura

```
Agência Kaizen CMS
├── 🤖 Agente de IA (CrewAI)
│   ├── Pesquisador de Conteúdo
│   ├── Escritor de Conteúdo
│   └── Editor de Conteúdo
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

## 🚀 Início Rápido

### 1. Instalação
```bash
# Clone o repositório
git clone <repository-url>
cd agenciakaizen

# Configure o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r src/requirements.txt

# Configure o agente de IA
python cli/setup_ai_agent.py
```

### 2. Configuração
```bash
# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas chaves de API

# Execute as migrações
cd src
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

### 3. Uso do Agente de IA
```bash
# Criar um post de blog
python cli/ai_content_agent.py --topic "Marketing Digital" --audience "empresários"

# Criar conteúdo evergreen
python cli/ai_content_agent.py --topic "SEO Avançado" --type evergreen --keyword "seo"

# Ver todas as opções
python cli/ai_content_agent.py --help
```

## 📞 Suporte

- **Documentação**: Consulte os guias específicos nesta pasta
- **Issues**: Reporte problemas no repositório
- **Contato**: comercial@www.agenciakaizen.com.br

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](../LICENSE) para mais detalhes.

---

**Desenvolvido com ❤️ pela Agência Kaizen**

