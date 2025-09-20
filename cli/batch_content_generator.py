#!/usr/bin/env python3
"""
Agente Gerador de Artigos em Lote
Cria múltiplos artigos baseados nas pautas geradas
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
import openai
from dotenv import load_dotenv

# Adicionar src ao path para importar configurações Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Carregar variáveis de ambiente
load_dotenv()


@dataclass
class GeneratedArticle:
    """Estrutura de dados para artigo gerado"""
    title: str
    content: str
    seo_title: str
    meta_description: str
    word_count: int
    status: str
    article_brief_id: int
    created_at: str
    published: bool = False
    api_response: Dict = None


class BlogAPITool(BaseTool):
    """
    Tool para integração com a API do blog (reutilizada do sistema anterior)
    """
    name: str = "Blog API Tool"
    description: str = "Ferramenta para criar, editar e gerenciar posts do blog via API"
    
    def __init__(self):
        super().__init__()
        self.base_url = "http://localhost:8000/api/blog"
        self.api_token = os.getenv('BLOG_API_TOKEN', '')
    
    def _run(self, action: str, **kwargs) -> str:
        """Executa ações na API do blog"""
        try:
            import requests
            
            headers = {
                'Authorization': f'Token {self.api_token}',
                'Content-Type': 'application/json'
            }
            
            if action == 'create_post':
                return self._create_post(kwargs, headers)
            elif action == 'publish_post':
                return self._publish_post(kwargs, headers)
            elif action == 'get_post':
                return self._get_post(kwargs, headers)
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
            return json.dumps({
                "success": True,
                "post_id": post_data['id'],
                "title": post_data['title'],
                "message": f"Post criado com sucesso! ID: {post_data['id']}"
            })
        else:
            return json.dumps({
                "success": False,
                "error": f"Erro ao criar post: {response.status_code} - {response.text}"
            })
    
    def _publish_post(self, data: Dict, headers: Dict) -> str:
        """Publica um post"""
        post_id = data['post_id']
        url = f"{self.base_url}/posts/{post_id}/publish/"
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            return json.dumps({
                "success": True,
                "message": f"Post {post_id} publicado com sucesso!"
            })
        else:
            return json.dumps({
                "success": False,
                "error": f"Erro ao publicar post: {response.status_code} - {response.text}"
            })
    
    def _get_post(self, data: Dict, headers: Dict) -> str:
        """Busca um post específico"""
        post_id = data['post_id']
        url = f"{self.base_url}/posts/{post_id}/"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return json.dumps(response.json())
        else:
            return json.dumps({
                "success": False,
                "error": f"Erro ao buscar post: {response.status_code} - {response.text}"
            })


class ContentGeneratorTool(BaseTool):
    """
    Tool para geração de conteúdo usando OpenAI
    """
    name: str = "Content Generator Tool"
    description: str = "Ferramenta para gerar conteúdo de artigos usando OpenAI"
    
    def __init__(self):
        super().__init__()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY não encontrada")
        
        openai.api_key = self.openai_api_key
    
    def _run(self, article_brief: str, **kwargs) -> str:
        """
        Gera conteúdo completo do artigo
        
        Args:
            article_brief: Pauta do artigo em JSON
        """
        try:
            brief_data = json.loads(article_brief)
            
            # Gerar conteúdo usando OpenAI
            content = self._generate_article_content(brief_data)
            
            return json.dumps(content, ensure_ascii=False)
            
        except Exception as e:
            return f"Erro na geração de conteúdo: {str(e)}"
    
    def _generate_article_content(self, brief: Dict) -> Dict:
        """Gera o conteúdo completo do artigo"""
        
        # Prompt para geração de conteúdo
        prompt = f"""
        Crie um artigo completo baseado na seguinte pauta:
        
        Título: {brief['title']}
        Tópico: {brief['topic']}
        Audiência: {brief['target_audience']}
        Formato: {brief['content_format']}
        Palavras estimadas: {brief['estimated_word_count']}
        Ângulo: {brief['content_angle']}
        Palavras-chave SEO: {', '.join(brief['seo_keywords'])}
        
        Estrutura do conteúdo:
        {json.dumps(brief['content_structure'], indent=2, ensure_ascii=False)}
        
        Pontos-chave a abordar:
        {chr(10).join(f"- {point}" for point in brief['key_points'])}
        
        Call-to-action: {brief['call_to_action']}
        
        Instruções:
        1. Crie um artigo envolvente e informativo
        2. Use a estrutura fornecida como guia
        3. Inclua as palavras-chave SEO naturalmente
        4. Mantenha o tom profissional mas acessível
        5. Inclua exemplos práticos e cases
        6. Termine com o call-to-action fornecido
        7. Use formatação HTML para títulos, listas e destaques
        8. Mantenha aproximadamente {brief['estimated_word_count']} palavras
        
        Retorne o conteúdo em formato HTML bem estruturado.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um redator especializado em conteúdo empresarial e marketing digital. Crie artigos envolventes, informativos e otimizados para SEO."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Gerar meta description
            meta_description = self._generate_meta_description(brief, content)
            
            # Contar palavras
            word_count = len(content.split())
            
            return {
                "title": brief['title'],
                "content": content,
                "seo_title": brief['title'][:60],  # Limitar para SEO
                "meta_description": meta_description,
                "word_count": word_count,
                "status": "generated",
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "title": brief['title'],
                "content": f"Erro ao gerar conteúdo: {str(e)}",
                "seo_title": brief['title'][:60],
                "meta_description": brief['title'],
                "word_count": 0,
                "status": "error",
                "created_at": datetime.now().isoformat()
            }
    
    def _generate_meta_description(self, brief: Dict, content: str) -> str:
        """Gera meta description otimizada"""
        # Extrair primeiras frases do conteúdo
        sentences = content.split('.')[:2]
        meta_desc = '. '.join(sentences).strip()
        
        # Limitar a 160 caracteres
        if len(meta_desc) > 160:
            meta_desc = meta_desc[:157] + "..."
        
        return meta_desc


class BatchContentGeneratorAgent:
    """
    Agente especializado em geração de artigos em lote
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
        
        openai.api_key = self.openai_api_key
        
        # Inicializar tools
        self.content_tool = ContentGeneratorTool()
        self.blog_tool = BlogAPITool()
        
        # Criar agentes
        self._create_agents()
    
    def _create_agents(self):
        """Cria os agentes especializados"""
        
        # Agente Escritor
        self.writer = Agent(
            role='Escritor de Conteúdo Empresarial',
            goal='Criar artigos de alta qualidade baseados em pautas editoriais, otimizados para SEO e engajamento',
            backstory="""Você é um redator especializado em conteúdo empresarial com expertise em:
            - Criação de artigos envolventes e informativos
            - Otimização para SEO sem comprometer a qualidade
            - Adaptação de tom para diferentes audiências
            - Estruturação de conteúdo para máxima legibilidade
            - Integração de call-to-actions efetivos
            
            Sua especialidade é transformar pautas editoriais em:
            - Artigos que engajam e convertem
            - Conteúdo otimizado para mecanismos de busca
            - Textos que estabelecem autoridade
            - Conteúdo que gera leads qualificados""",
            tools=[self.content_tool],
            verbose=True,
            allow_delegation=False
        )
        
        # Agente Editor
        self.editor = Agent(
            role='Editor de Conteúdo e Revisor',
            goal='Revisar, otimizar e finalizar artigos para publicação, garantindo qualidade e consistência',
            backstory="""Você é um editor experiente especializado em:
            - Revisão gramatical e ortográfica
            - Otimização de SEO e estrutura
            - Verificação de consistência de tom
            - Melhoria de clareza e fluidez
            - Ajustes finais para publicação
            
            Sua expertise garante que cada artigo:
            - Esteja livre de erros
            - Tenha estrutura otimizada
            - Mantenha consistência de qualidade
            - Esteja pronto para publicação""",
            tools=[self.blog_tool],
            verbose=True,
            allow_delegation=True
        )
    
    def generate_articles_batch(self, article_briefs: List[Dict], 
                               auto_publish: bool = False, 
                               delay_between_articles: int = 30) -> List[GeneratedArticle]:
        """
        Gera múltiplos artigos baseados nas pautas
        
        Args:
            article_briefs: Lista de pautas de artigos
            auto_publish: Se deve publicar automaticamente
            delay_between_articles: Delay entre artigos (segundos)
        
        Returns:
            Lista de artigos gerados
        """
        
        generated_articles = []
        
        print(f"\n🚀 Iniciando geração de {len(article_briefs)} artigos...")
        print("=" * 60)
        
        for i, brief in enumerate(article_briefs, 1):
            print(f"\n📝 Gerando artigo {i}/{len(article_briefs)}: {brief['title']}")
            
            try:
                # Task 1: Escrita
                writing_task = Task(
                    description=f"""
                    Crie um artigo completo baseado na seguinte pauta:
                    
                    Título: {brief['title']}
                    Tópico: {brief['topic']}
                    Audiência: {brief['target_audience']}
                    Formato: {brief['content_format']}
                    Palavras estimadas: {brief['estimated_word_count']}
                    Ângulo: {brief['content_angle']}
                    
                    Estrutura fornecida:
                    {json.dumps(brief['content_structure'], indent=2, ensure_ascii=False)}
                    
                    Pontos-chave:
                    {chr(10).join(f"- {point}" for point in brief['key_points'])}
                    
                    Palavras-chave SEO: {', '.join(brief['seo_keywords'])}
                    Call-to-action: {brief['call_to_action']}
                    
                    Instruções:
                    1. Crie um artigo envolvente e informativo
                    2. Use a estrutura fornecida como guia
                    3. Inclua as palavras-chave SEO naturalmente
                    4. Mantenha o tom profissional mas acessível
                    5. Inclua exemplos práticos e cases
                    6. Termine com o call-to-action fornecido
                    7. Use formatação HTML para títulos, listas e destaques
                    8. Mantenha aproximadamente {brief['estimated_word_count']} palavras
                    
                    Retorne o conteúdo em formato HTML bem estruturado.
                    """,
                    agent=self.writer,
                    expected_output="Artigo completo em HTML com título, conteúdo estruturado, meta description e otimização SEO"
                )
                
                # Task 2: Edição e Publicação
                editing_task = Task(
                    description=f"""
                    Revise e publique o artigo gerado sobre: {brief['title']}
                    
                    Verifique:
                    1. Gramática e ortografia
                    2. Estrutura e formatação HTML
                    3. Otimização SEO (título, meta description)
                    4. Consistência de tom
                    5. Call-to-action efetivo
                    
                    Se aprovado, publique no blog usando a API.
                    Auto-publicação: {auto_publish}
                    """,
                    agent=self.editor,
                    expected_output="Artigo revisado, otimizado e publicado no blog",
                    context=[writing_task]
                )
                
                # Executar crew
                crew = Crew(
                    agents=[self.writer, self.editor],
                    tasks=[writing_task, editing_task],
                    process=Process.sequential,
                    verbose=True
                )
                
                result = crew.kickoff()
                
                # Processar resultado
                article = self._process_generated_article(brief, result, auto_publish)
                generated_articles.append(article)
                
                print(f"✅ Artigo {i} gerado com sucesso!")
                print(f"   Título: {article.title}")
                print(f"   Palavras: {article.word_count}")
                print(f"   Status: {article.status}")
                
                # Delay entre artigos
                if i < len(article_briefs) and delay_between_articles > 0:
                    print(f"⏳ Aguardando {delay_between_articles}s antes do próximo artigo...")
                    time.sleep(delay_between_articles)
                
            except Exception as e:
                print(f"❌ Erro ao gerar artigo {i}: {str(e)}")
                
                # Criar artigo de erro
                error_article = GeneratedArticle(
                    title=brief['title'],
                    content=f"Erro na geração: {str(e)}",
                    seo_title=brief['title'][:60],
                    meta_description=brief['title'],
                    word_count=0,
                    status="error",
                    article_brief_id=i,
                    created_at=datetime.now().isoformat(),
                    published=False
                )
                generated_articles.append(error_article)
        
        print(f"\n🎉 Geração concluída! {len(generated_articles)} artigos processados.")
        return generated_articles
    
    def _process_generated_article(self, brief: Dict, result: str, auto_publish: bool) -> GeneratedArticle:
        """Processa o resultado da geração de artigo"""
        
        # Em produção, processar o resultado real do agente
        # Por enquanto, simular geração usando a tool
        
        try:
            # Gerar conteúdo usando a tool
            brief_json = json.dumps(brief)
            content_data = json.loads(self.content_tool._run(brief_json))
            
            # Criar artigo
            article = GeneratedArticle(
                title=content_data['title'],
                content=content_data['content'],
                seo_title=content_data['seo_title'],
                meta_description=content_data['meta_description'],
                word_count=content_data['word_count'],
                status=content_data['status'],
                article_brief_id=brief.get('publication_priority', 1),
                created_at=content_data['created_at'],
                published=False
            )
            
            # Se auto_publish, tentar publicar
            if auto_publish and content_data['status'] == 'generated':
                try:
                    # Dados para criação do post
                    post_data = {
                        'title': article.title,
                        'intro': article.meta_description[:250],
                        'body': article.content,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'seo_title': article.seo_title,
                        'search_description': article.meta_description,
                        'live': True
                    }
                    
                    # Criar post via API
                    api_response = self.blog_tool._run('create_post', **post_data)
                    api_data = json.loads(api_response)
                    
                    if api_data.get('success'):
                        article.published = True
                        article.api_response = api_data
                        article.status = 'published'
                        
                        # Publicar se necessário
                        if not auto_publish:
                            publish_response = self.blog_tool._run('publish_post', post_id=api_data['post_id'])
                            publish_data = json.loads(publish_response)
                            if publish_data.get('success'):
                                article.status = 'published'
                    
                except Exception as e:
                    print(f"⚠️  Erro ao publicar via API: {str(e)}")
                    article.api_response = {"error": str(e)}
            
            return article
            
        except Exception as e:
            return GeneratedArticle(
                title=brief['title'],
                content=f"Erro na geração: {str(e)}",
                seo_title=brief['title'][:60],
                meta_description=brief['title'],
                word_count=0,
                status="error",
                article_brief_id=brief.get('publication_priority', 1),
                created_at=datetime.now().isoformat(),
                published=False,
                api_response={"error": str(e)}
            )


def main():
    """Função principal para teste"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gerador de Artigos em Lote')
    parser.add_argument('--briefs-file', help='Arquivo JSON com pautas')
    parser.add_argument('--auto-publish', action='store_true', help='Publicar automaticamente')
    parser.add_argument('--delay', type=int, default=30, help='Delay entre artigos (segundos)')
    
    args = parser.parse_args()
    
    try:
        # Inicializar agente
        agent = BatchContentGeneratorAgent()
        
        # Carregar pautas (simulação)
        article_briefs = [
            {
                "title": "Como Implementar IA na Sua Empresa: Guia Completo 2024",
                "topic": "Inteligência Artificial nos Negócios",
                "target_audience": "Executivos e gestores",
                "content_format": "Guia Prático",
                "estimated_word_count": 2000,
                "content_angle": "Abordagem prática e implementável",
                "key_points": ["Automação", "Análise preditiva", "Chatbots"],
                "seo_keywords": ["ia", "inteligencia artificial", "negocios", "2024"],
                "call_to_action": "Baixe nosso guia completo",
                "publication_priority": 1,
                "content_structure": {
                    "introduction": {"hook": "Por que IA está revolucionando os negócios"},
                    "main_sections": [
                        {"title": "Contexto e Importância", "content": "Análise do cenário atual"},
                        {"title": "Implementação Prática", "content": "Passos concretos"}
                    ],
                    "conclusion": {"summary": "Principais pontos", "cta": "Baixe nosso guia"}
                }
            }
        ]
        
        # Gerar artigos
        articles = agent.generate_articles_batch(
            article_briefs, 
            auto_publish=args.auto_publish,
            delay_between_articles=args.delay
        )
        
        print(f"\n📊 Resumo da geração:")
        print(f"   Total de artigos: {len(articles)}")
        print(f"   Artigos publicados: {sum(1 for a in articles if a.published)}")
        print(f"   Artigos com erro: {sum(1 for a in articles if a.status == 'error')}")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

