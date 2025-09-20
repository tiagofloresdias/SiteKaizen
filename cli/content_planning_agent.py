#!/usr/bin/env python3
"""
Agente Criador de Pautas de Artigos
Cria pautas estratégicas baseadas em tendências do LinkedIn
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dataclasses import dataclass
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
import openai
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


@dataclass
class ArticleBrief:
    """Estrutura de dados para pauta de artigo"""
    title: str
    topic: str
    target_audience: str
    key_points: List[str]
    seo_keywords: List[str]
    content_structure: Dict[str, Any]
    estimated_word_count: int
    content_angle: str
    call_to_action: str
    publication_priority: int
    expected_engagement: float
    content_format: str
    research_sources: List[str]


class ContentPlanningTool(BaseTool):
    """
    Tool para criação de pautas de artigos
    """
    name: str = "Content Planning Tool"
    description: str = "Ferramenta para criar pautas estratégicas de artigos baseadas em tendências"
    
    def _run(self, trends_data: str, num_articles: int = 5, **kwargs) -> str:
        """
        Cria pautas de artigos baseadas em tendências
        
        Args:
            trends_data: Dados de tendências em JSON
            num_articles: Número de artigos para criar pautas
        """
        try:
            trends = json.loads(trends_data)
            article_briefs = self._create_article_briefs(trends, num_articles)
            
            return json.dumps(article_briefs, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return f"Erro na criação de pautas: {str(e)}"
    
    def _create_article_briefs(self, trends: List[Dict], num_articles: int) -> List[Dict]:
        """Cria pautas de artigos baseadas nas tendências"""
        
        article_briefs = []
        
        # Estratégias de conteúdo para diferentes tipos de tendências
        content_strategies = {
            "tutorial": {
                "format": "Guia Prático",
                "structure": {
                    "intro": "Problema e promessa de solução",
                    "main_content": "Passo a passo detalhado",
                    "conclusion": "Resultados esperados e próximos passos"
                },
                "cta": "Baixe nosso guia completo"
            },
            "analysis": {
                "format": "Análise de Mercado",
                "structure": {
                    "intro": "Contexto e importância do tema",
                    "main_content": "Dados, estatísticas e insights",
                    "conclusion": "Implicações e recomendações"
                },
                "cta": "Agende uma consultoria gratuita"
            },
            "case_study": {
                "format": "Case de Sucesso",
                "structure": {
                    "intro": "Desafio enfrentado",
                    "main_content": "Solução implementada e resultados",
                    "conclusion": "Lições aprendidas"
                },
                "cta": "Conheça nossa metodologia"
            },
            "trend_report": {
                "format": "Relatório de Tendências",
                "structure": {
                    "intro": "Panorama atual do mercado",
                    "main_content": "Tendências identificadas e impactos",
                    "conclusion": "Como se preparar para o futuro"
                },
                "cta": "Receba nosso relatório completo"
            },
            "expert_opinion": {
                "format": "Opinião de Especialista",
                "structure": {
                    "intro": "Contextualização do tema",
                    "main_content": "Análise e perspectivas do especialista",
                    "conclusion": "Recomendações práticas"
                },
                "cta": "Converse com nossos especialistas"
            }
        }
        
        for i, trend in enumerate(trends[:num_articles]):
            # Escolher estratégia baseada no tipo de tendência
            strategy_key = self._choose_strategy(trend)
            strategy = content_strategies[strategy_key]
            
            # Gerar título baseado na tendência
            title = self._generate_title(trend, strategy_key)
            
            # Criar estrutura de conteúdo
            content_structure = self._create_content_structure(trend, strategy)
            
            # Gerar palavras-chave SEO
            seo_keywords = self._generate_seo_keywords(trend, title)
            
            # Estimar engajamento
            expected_engagement = self._estimate_engagement(trend, strategy_key)
            
            article_brief = {
                "title": title,
                "topic": trend["topic"],
                "target_audience": trend["target_audience"],
                "key_points": trend["key_points"][:5],  # Top 5 pontos
                "seo_keywords": seo_keywords,
                "content_structure": content_structure,
                "estimated_word_count": self._estimate_word_count(strategy_key),
                "content_angle": self._generate_content_angle(trend, strategy_key),
                "call_to_action": strategy["cta"],
                "publication_priority": i + 1,
                "expected_engagement": expected_engagement,
                "content_format": strategy["format"],
                "research_sources": trend.get("competitors_insights", [])[:3]
            }
            
            article_briefs.append(article_brief)
        
        return article_briefs
    
    def _choose_strategy(self, trend: Dict) -> str:
        """Escolhe estratégia de conteúdo baseada na tendência"""
        topic_lower = trend["topic"].lower()
        
        if any(word in topic_lower for word in ["como", "guia", "tutorial", "passo"]):
            return "tutorial"
        elif any(word in topic_lower for word in ["análise", "mercado", "dados", "estatísticas"]):
            return "analysis"
        elif any(word in topic_lower for word in ["case", "sucesso", "experiência", "implementação"]):
            return "case_study"
        elif any(word in topic_lower for word in ["tendência", "futuro", "2024", "previsão"]):
            return "trend_report"
        else:
            return "expert_opinion"
    
    def _generate_title(self, trend: Dict, strategy: str) -> str:
        """Gera título atrativo para o artigo"""
        topic = trend["topic"]
        
        title_templates = {
            "tutorial": [
                f"Como Implementar {topic} na Sua Empresa: Guia Completo 2024",
                f"Passo a Passo: {topic} para Resultados Reais",
                f"Guia Definitivo de {topic}: Tudo que Você Precisa Saber"
            ],
            "analysis": [
                f"Análise Completa: {topic} e Seu Impacto nos Negócios",
                f"{topic}: Dados, Tendências e Oportunidades de Mercado",
                f"Panorama Atual de {topic}: O que os Números Revelam"
            ],
            "case_study": [
                f"Case de Sucesso: Como {topic} Transformou Nossa Empresa",
                f"História Real: {topic} em Ação - Resultados Impressionantes",
                f"Implementação de {topic}: Lições Aprendidas e Resultados"
            ],
            "trend_report": [
                f"Tendências de {topic} em 2024: O que Esperar",
                f"Futuro de {topic}: Previsões e Preparação",
                f"Relatório de Tendências: {topic} em Destaque"
            ],
            "expert_opinion": [
                f"Especialista Opina: {topic} e Seu Impacto Real",
                f"Visão de Especialista: {topic} na Prática",
                f"Análise Especializada: {topic} e Oportunidades"
            ]
        }
        
        import random
        return random.choice(title_templates[strategy])
    
    def _create_content_structure(self, trend: Dict, strategy: Dict) -> Dict:
        """Cria estrutura detalhada do conteúdo"""
        return {
            "introduction": {
                "hook": f"Por que {trend['topic']} está revolucionando os negócios",
                "problem_statement": f"Desafios enfrentados por {trend['target_audience']}",
                "promise": f"Como este artigo vai resolver seus problemas"
            },
            "main_sections": [
                {
                    "title": "Contexto e Importância",
                    "content": f"Análise do cenário atual de {trend['topic']}",
                    "key_points": trend["key_points"][:3]
                },
                {
                    "title": "Implementação Prática",
                    "content": "Passos concretos para aplicação",
                    "key_points": ["Estratégia", "Ferramentas", "Métricas"]
                },
                {
                    "title": "Resultados e Benefícios",
                    "content": "O que esperar após implementação",
                    "key_points": ["ROI", "Eficiência", "Competitividade"]
                }
            ],
            "conclusion": {
                "summary": "Principais pontos abordados",
                "next_steps": "Como continuar o aprendizado",
                "cta": strategy["cta"]
            }
        }
    
    def _generate_seo_keywords(self, trend: Dict, title: str) -> List[str]:
        """Gera palavras-chave SEO relevantes"""
        base_keywords = [
            trend["topic"].lower(),
            "negócios",
            "empresas",
            "2024"
        ]
        
        # Adicionar hashtags como keywords
        hashtag_keywords = [tag.replace("#", "").lower() for tag in trend.get("hashtags", [])]
        
        # Adicionar palavras do título
        title_keywords = [word.lower() for word in title.split() if len(word) > 3]
        
        # Combinar e remover duplicatas
        all_keywords = list(set(base_keywords + hashtag_keywords + title_keywords))
        
        return all_keywords[:10]  # Retornar top 10
    
    def _estimate_engagement(self, trend: Dict, strategy: str) -> float:
        """Estima engajamento esperado do artigo"""
        base_engagement = trend.get("engagement_score", 8.0)
        
        # Ajustar baseado na estratégia
        strategy_multipliers = {
            "tutorial": 1.2,
            "case_study": 1.3,
            "analysis": 1.1,
            "trend_report": 1.0,
            "expert_opinion": 1.1
        }
        
        return min(10.0, base_engagement * strategy_multipliers.get(strategy, 1.0))
    
    def _estimate_word_count(self, strategy: str) -> int:
        """Estima número de palavras baseado na estratégia"""
        word_counts = {
            "tutorial": 2000,
            "case_study": 1800,
            "analysis": 2200,
            "trend_report": 2500,
            "expert_opinion": 1600
        }
        
        return word_counts.get(strategy, 1800)
    
    def _generate_content_angle(self, trend: Dict, strategy: str) -> str:
        """Gera ângulo único para o conteúdo"""
        angles = {
            "tutorial": f"Abordagem prática e implementável de {trend['topic']}",
            "case_study": f"Experiência real e resultados comprovados de {trend['topic']}",
            "analysis": f"Análise profunda e dados concretos sobre {trend['topic']}",
            "trend_report": f"Visão estratégica e previsões sobre {trend['topic']}",
            "expert_opinion": f"Perspectiva especializada e insights únicos sobre {trend['topic']}"
        }
        
        return angles.get(strategy, f"Abordagem única sobre {trend['topic']}")


class ContentPlanningAgent:
    """
    Agente especializado em criação de pautas de artigos
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
        
        openai.api_key = self.openai_api_key
        
        # Inicializar tools
        self.planning_tool = ContentPlanningTool()
        
        # Criar agente
        self._create_agent()
    
    def _create_agent(self):
        """Cria o agente de planejamento de conteúdo"""
        self.agent = Agent(
            role='Estrategista de Conteúdo e Planejador Editorial',
            goal='Criar pautas estratégicas de artigos baseadas em tendências, otimizadas para engajamento e SEO',
            backstory="""Você é um estrategista de conteúdo com vasta experiência em:
            - Planejamento editorial estratégico
            - Criação de pautas baseadas em dados
            - Otimização para SEO e engajamento
            - Análise de audiência e personas
            - Estratégias de conteúdo multicanal
            
            Sua expertise permite transformar tendências em:
            - Pautas editoriais estratégicas
            - Conteúdo otimizado para diferentes formatos
            - Estruturas que maximizam engajamento
            - CTAs que convertem
            - Calendários editoriais eficazes""",
            tools=[self.planning_tool],
            verbose=True,
            allow_delegation=False
        )
    
    def create_article_briefs(self, trends_data: List[Dict], num_articles: int = 5) -> List[ArticleBrief]:
        """
        Cria pautas de artigos baseadas em tendências
        
        Args:
            trends_data: Lista de tendências encontradas
            num_articles: Número de artigos para criar pautas
        
        Returns:
            Lista de pautas de artigos
        """
        
        # Task de criação de pautas
        planning_task = Task(
            description=f"""
            Crie {num_articles} pautas estratégicas de artigos baseadas nas tendências fornecidas.
            
            Para cada pauta, inclua:
            1. Título atrativo e otimizado para SEO
            2. Estrutura detalhada do conteúdo
            3. Palavras-chave estratégicas
            4. Ângulo único de abordagem
            5. Call-to-action relevante
            6. Estimativa de engajamento
            7. Formato de conteúdo ideal
            8. Fontes de pesquisa
            
            Priorize:
            - Conteúdo que gera engajamento
            - Diferenciação competitiva
            - Relevância para a audiência
            - Potencial de conversão
            - Otimização para SEO
            
            Garanta que cada pauta seja:
            - Única e diferenciada
            - Estrategicamente posicionada
            - Pronta para produção
            - Alinhada com objetivos de negócio
            """,
            agent=self.agent,
            expected_output=f"Lista de {num_articles} pautas editoriais completas com estruturas detalhadas, estratégias de conteúdo e métricas de sucesso"
        )
        
        # Executar planejamento
        crew = Crew(
            agents=[self.agent],
            tasks=[planning_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Converter trends para formato JSON
        trends_json = json.dumps([trend.__dict__ if hasattr(trend, '__dict__') else trend for trend in trends_data])
        
        result = crew.kickoff()
        
        # Processar resultados (simulação - em produção, processar resultado real)
        article_briefs = self._process_planning_result(trends_data, num_articles)
        
        return article_briefs
    
    def _process_planning_result(self, trends_data: List[Dict], num_articles: int) -> List[ArticleBrief]:
        """Processa o resultado do planejamento de conteúdo"""
        
        # Usar a tool para criar pautas
        trends_json = json.dumps([trend.__dict__ if hasattr(trend, '__dict__') else trend for trend in trends_data])
        briefs_data = json.loads(self.planning_tool._run(trends_json, num_articles))
        
        article_briefs = []
        for brief_data in briefs_data:
            brief = ArticleBrief(
                title=brief_data["title"],
                topic=brief_data["topic"],
                target_audience=brief_data["target_audience"],
                key_points=brief_data["key_points"],
                seo_keywords=brief_data["seo_keywords"],
                content_structure=brief_data["content_structure"],
                estimated_word_count=brief_data["estimated_word_count"],
                content_angle=brief_data["content_angle"],
                call_to_action=brief_data["call_to_action"],
                publication_priority=brief_data["publication_priority"],
                expected_engagement=brief_data["expected_engagement"],
                content_format=brief_data["content_format"],
                research_sources=brief_data["research_sources"]
            )
            article_briefs.append(brief)
        
        return article_briefs


def main():
    """Função principal para teste"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Criador de Pautas de Artigos')
    parser.add_argument('--trends-file', help='Arquivo JSON com tendências')
    parser.add_argument('--num-articles', type=int, default=5, help='Número de artigos')
    
    args = parser.parse_args()
    
    try:
        # Inicializar agente
        agent = ContentPlanningAgent()
        
        # Carregar tendências (simulação)
        trends_data = [
            {
                "topic": "Inteligência Artificial nos Negócios",
                "engagement_score": 9.2,
                "target_audience": "Executivos e gestores",
                "key_points": ["Automação", "Análise preditiva", "Chatbots"],
                "hashtags": ["#IA", "#Negocios", "#Inovacao"]
            }
        ]
        
        # Criar pautas
        briefs = agent.create_article_briefs(trends_data, args.num_articles)
        
        print(f"\n📝 Pautas criadas: {len(briefs)}")
        print("=" * 50)
        
        for i, brief in enumerate(briefs, 1):
            print(f"\n{i}. {brief.title}")
            print(f"   Tópico: {brief.topic}")
            print(f"   Audiência: {brief.target_audience}")
            print(f"   Formato: {brief.content_format}")
            print(f"   Palavras: {brief.estimated_word_count}")
            print(f"   Engajamento esperado: {brief.expected_engagement:.1f}/10")
            print(f"   CTA: {brief.call_to_action}")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

