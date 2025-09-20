#!/usr/bin/env python3
"""
Agente de IA para Criação de Conteúdos - CrewAI
Sistema integrado com a API do blog da Agência Kaizen
"""

import os
import sys
import json
import requests
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Adicionar o diretório src ao path para importar configurações Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
import openai
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


@dataclass
class BlogPostData:
    """Estrutura de dados para um post do blog"""
    title: str
    intro: str
    body: str
    date: str
    seo_title: Optional[str] = None
    search_description: Optional[str] = None
    live: bool = False


class BlogAPITool(BaseTool):
    """
    Tool para integração com a API do blog da Agência Kaizen
    """
    name: str = "Blog API Tool"
    description: str = "Ferramenta para criar, editar e gerenciar posts do blog via API"
    
    def __init__(self):
        super().__init__()
        self.base_url = "http://localhost:8000/api/blog"  # URL da API local
        self.api_token = os.getenv('BLOG_API_TOKEN', '')  # Token de autenticação
    
    def _run(self, action: str, **kwargs) -> str:
        """
        Executa ações na API do blog
        
        Args:
            action: Ação a ser executada (create, update, publish, etc.)
            **kwargs: Parâmetros específicos da ação
        """
        try:
            headers = {
                'Authorization': f'Token {self.api_token}',
                'Content-Type': 'application/json'
            }
            
            if action == 'create_post':
                return self._create_post(kwargs, headers)
            elif action == 'update_post':
                return self._update_post(kwargs, headers)
            elif action == 'publish_post':
                return self._publish_post(kwargs, headers)
            elif action == 'get_post':
                return self._get_post(kwargs, headers)
            elif action == 'list_posts':
                return self._list_posts(kwargs, headers)
            else:
                return f"Erro: Ação '{action}' não reconhecida"
                
        except Exception as e:
            return f"Erro na API do blog: {str(e)}"
    
    def _create_post(self, data: Dict, headers: Dict) -> str:
        """Cria um novo post no blog"""
        url = f"{self.base_url}/posts/"
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 201:
            post_data = response.json()
            return f"Post criado com sucesso! ID: {post_data['id']}, Título: {post_data['title']}"
        else:
            return f"Erro ao criar post: {response.status_code} - {response.text}"
    
    def _update_post(self, data: Dict, headers: Dict) -> str:
        """Atualiza um post existente"""
        post_id = data.pop('post_id')
        url = f"{self.base_url}/posts/{post_id}/"
        response = requests.patch(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return f"Post {post_id} atualizado com sucesso!"
        else:
            return f"Erro ao atualizar post: {response.status_code} - {response.text}"
    
    def _publish_post(self, data: Dict, headers: Dict) -> str:
        """Publica um post"""
        post_id = data['post_id']
        url = f"{self.base_url}/posts/{post_id}/publish/"
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            return f"Post {post_id} publicado com sucesso!"
        else:
            return f"Erro ao publicar post: {response.status_code} - {response.text}"
    
    def _get_post(self, data: Dict, headers: Dict) -> str:
        """Busca um post específico"""
        post_id = data['post_id']
        url = f"{self.base_url}/posts/{post_id}/"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return json.dumps(response.json(), indent=2, ensure_ascii=False)
        else:
            return f"Erro ao buscar post: {response.status_code} - {response.text}"
    
    def _list_posts(self, data: Dict, headers: Dict) -> str:
        """Lista posts do blog"""
        url = f"{self.base_url}/posts/"
        params = data.get('params', {})
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            return json.dumps(response.json(), indent=2, ensure_ascii=False)
        else:
            return f"Erro ao listar posts: {response.status_code} - {response.text}"


class ContentResearchTool(BaseTool):
    """
    Tool para pesquisa de conteúdo e tendências
    """
    name: str = "Content Research Tool"
    description: str = "Ferramenta para pesquisar tendências, palavras-chave e informações relevantes"
    
    def _run(self, query: str, **kwargs) -> str:
        """
        Pesquisa informações relevantes para criação de conteúdo
        
        Args:
            query: Termo de pesquisa
            **kwargs: Parâmetros adicionais
        """
        try:
            # Simulação de pesquisa (em produção, integrar com APIs reais)
            research_data = {
                "query": query,
                "trending_topics": [
                    "Marketing Digital 2024",
                    "Inteligência Artificial em Marketing",
                    "Automação de Marketing",
                    "SEO Avançado",
                    "Redes Sociais para Empresas"
                ],
                "keywords": [
                    f"{query} estratégia",
                    f"{query} dicas",
                    f"{query} como fazer",
                    f"{query} benefícios",
                    f"{query} tendências 2024"
                ],
                "competitor_insights": [
                    "Conteúdo similar com alta performance",
                    "Palavras-chave em alta",
                    "Formatos de conteúdo populares"
                ]
            }
            
            return json.dumps(research_data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return f"Erro na pesquisa: {str(e)}"


class AIContentAgent:
    """
    Agente principal de IA para criação de conteúdos
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
        
        # Configurar OpenAI
        openai.api_key = self.openai_api_key
        
        # Inicializar tools
        self.blog_tool = BlogAPITool()
        self.research_tool = ContentResearchTool()
        
        # Criar agentes
        self._create_agents()
    
    def _create_agents(self):
        """Cria os agentes especializados"""
        
        # Agente Pesquisador
        self.researcher = Agent(
            role='Pesquisador de Conteúdo',
            goal='Pesquisar e analisar tendências, palavras-chave e informações relevantes para criação de conteúdo',
            backstory="""Você é um especialista em pesquisa de conteúdo digital com anos de experiência 
            em identificar tendências, analisar concorrentes e descobrir oportunidades de conteúdo 
            que geram engajamento e tráfego orgânico.""",
            tools=[self.research_tool],
            verbose=True,
            allow_delegation=False
        )
        
        # Agente Escritor
        self.writer = Agent(
            role='Escritor de Conteúdo Digital',
            goal='Criar conteúdo de alta qualidade, otimizado para SEO e engajamento',
            backstory="""Você é um redator especializado em marketing digital com expertise em:
            - Copywriting persuasivo
            - SEO técnico e semântico
            - Estruturação de conteúdo para web
            - Adaptação de tom e linguagem para diferentes audiências
            - Criação de CTAs efetivos""",
            tools=[self.blog_tool],
            verbose=True,
            allow_delegation=True
        )
        
        # Agente Editor
        self.editor = Agent(
            role='Editor de Conteúdo',
            goal='Revisar, otimizar e finalizar conteúdo para publicação',
            backstory="""Você é um editor experiente especializado em:
            - Revisão gramatical e ortográfica
            - Otimização de SEO
            - Verificação de consistência de tom
            - Melhoria de clareza e fluidez
            - Ajustes finais para publicação""",
            tools=[self.blog_tool],
            verbose=True,
            allow_delegation=False
        )
    
    def create_blog_post(self, topic: str, target_audience: str = "empresários e profissionais de marketing", 
                        word_count: int = 1500, include_seo: bool = True) -> Dict[str, Any]:
        """
        Cria um post completo do blog
        
        Args:
            topic: Tópico principal do post
            target_audience: Audiência alvo
            word_count: Número aproximado de palavras
            include_seo: Se deve incluir otimização SEO
        
        Returns:
            Dict com informações do post criado
        """
        
        # Task 1: Pesquisa
        research_task = Task(
            description=f"""
            Pesquise informações detalhadas sobre o tópico: "{topic}"
            
            Foque em:
            - Tendências atuais relacionadas ao tópico
            - Palavras-chave relevantes e de alta busca
            - Insights sobre a audiência: {target_audience}
            - Dados e estatísticas relevantes
            - Exemplos práticos e cases de sucesso
            - Perguntas frequentes sobre o tópico
            
            Forneça um relatório completo com dados acionáveis para criação de conteúdo.
            """,
            agent=self.researcher,
            expected_output="Relatório detalhado de pesquisa com insights, palavras-chave, tendências e dados relevantes"
        )
        
        # Task 2: Escrita
        writing_task = Task(
            description=f"""
            Com base na pesquisa realizada, crie um post de blog completo sobre: "{topic}"
            
            Especificações:
            - Audiência: {target_audience}
            - Tamanho aproximado: {word_count} palavras
            - Incluir SEO: {include_seo}
            - Tom: Profissional mas acessível
            - Estrutura: Introdução, desenvolvimento, conclusão com CTA
            
            O post deve incluir:
            1. Título atrativo e otimizado para SEO
            2. Introdução envolvente que capte a atenção
            3. Desenvolvimento com subtítulos e seções bem estruturadas
            4. Exemplos práticos e cases reais
            5. Conclusão com call-to-action relevante
            6. Meta description otimizada (se include_seo=True)
            
            Use a ferramenta Blog API Tool para salvar o post no sistema.
            """,
            agent=self.writer,
            expected_output="Post de blog completo salvo no sistema via API",
            context=[research_task]
        )
        
        # Task 3: Edição
        editing_task = Task(
            description=f"""
            Revise e otimize o post criado sobre: "{topic}"
            
            Verifique:
            - Gramática e ortografia
            - Fluidez e clareza do texto
            - Otimização SEO (títulos, meta description, palavras-chave)
            - Consistência de tom e voz
            - Estrutura e formatação
            - Call-to-action efetivo
            
            Faça os ajustes necessários e publique o post se estiver aprovado.
            """,
            agent=self.editor,
            expected_output="Post revisado, otimizado e publicado no blog",
            context=[writing_task]
        )
        
        # Criar e executar crew
        crew = Crew(
            agents=[self.researcher, self.writer, self.editor],
            tasks=[research_task, writing_task, editing_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Executar processo
        result = crew.kickoff()
        
        return {
            "status": "success",
            "topic": topic,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    
    def create_evergreen_content(self, topic: str, focus_keyword: str, 
                               target_audience: str = "empresários") -> Dict[str, Any]:
        """
        Cria conteúdo evergreen otimizado para SEO
        
        Args:
            topic: Tópico principal
            focus_keyword: Palavra-chave principal
            target_audience: Audiência alvo
        
        Returns:
            Dict com informações do conteúdo criado
        """
        
        # Task de pesquisa específica para SEO
        seo_research_task = Task(
            description=f"""
            Pesquise informações específicas para conteúdo evergreen sobre: "{topic}"
            
            Foque em:
            - Palavra-chave principal: "{focus_keyword}"
            - Palavras-chave secundárias relacionadas
            - Perguntas frequentes sobre o tópico
            - Conteúdo que permanece relevante ao longo do tempo
            - Estrutura ideal para SEO
            - Dados e estatísticas atuais
            """,
            agent=self.researcher,
            expected_output="Relatório de pesquisa SEO com palavras-chave e estrutura otimizada"
        )
        
        # Task de criação de conteúdo evergreen
        evergreen_task = Task(
            description=f"""
            Crie uma página evergreen completa sobre: "{topic}"
            
            Especificações:
            - Palavra-chave principal: "{focus_keyword}"
            - Audiência: {target_audience}
            - Tipo: Página evergreen (conteúdo atemporal)
            - Otimização SEO máxima
            - Estrutura: Hero, seções informativas, FAQ, CTA
            
            A página deve incluir:
            1. Hero section com título otimizado
            2. Subtítulo explicativo
            3. Meta description otimizada
            4. Conteúdo estruturado com H2, H3
            5. Seção de FAQ
            6. Call-to-action relevante
            7. Palavras-chave distribuídas naturalmente
            
            Use a ferramenta Blog API Tool para criar como página evergreen.
            """,
            agent=self.writer,
            expected_output="Página evergreen criada e salva no sistema",
            context=[seo_research_task]
        )
        
        # Executar crew
        crew = Crew(
            agents=[self.researcher, self.writer],
            tasks=[seo_research_task, evergreen_task],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff()
        
        return {
            "status": "success",
            "type": "evergreen",
            "topic": topic,
            "focus_keyword": focus_keyword,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }


def main():
    """
    Função principal para execução via CLI
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Agente de IA para Criação de Conteúdos')
    parser.add_argument('--topic', required=True, help='Tópico do conteúdo a ser criado')
    parser.add_argument('--audience', default='empresários e profissionais de marketing', 
                       help='Audiência alvo')
    parser.add_argument('--words', type=int, default=1500, help='Número de palavras')
    parser.add_argument('--type', choices=['blog', 'evergreen'], default='blog',
                       help='Tipo de conteúdo')
    parser.add_argument('--keyword', help='Palavra-chave principal (para evergreen)')
    parser.add_argument('--publish', action='store_true', help='Publicar automaticamente')
    
    args = parser.parse_args()
    
    try:
        # Inicializar agente
        agent = AIContentAgent()
        
        if args.type == 'blog':
            result = agent.create_blog_post(
                topic=args.topic,
                target_audience=args.audience,
                word_count=args.words
            )
        elif args.type == 'evergreen':
            if not args.keyword:
                print("Erro: --keyword é obrigatório para conteúdo evergreen")
                sys.exit(1)
            result = agent.create_evergreen_content(
                topic=args.topic,
                focus_keyword=args.keyword,
                target_audience=args.audience
            )
        
        print(f"\n✅ Conteúdo criado com sucesso!")
        print(f"Tópico: {result['topic']}")
        print(f"Tipo: {result.get('type', 'blog')}")
        print(f"Timestamp: {result['timestamp']}")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

