#!/usr/bin/env python3
"""
Pipeline Completo de Criação de Conteúdo Baseado em Tendências
Integra pesquisa de tendências, criação de pautas e geração de artigos
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from pathlib import Path

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Importar agentes
from trend_research_agent import TrendResearchAgent, TrendData
from content_planning_agent import ContentPlanningAgent, ArticleBrief
from batch_content_generator import BatchContentGeneratorAgent, GeneratedArticle

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()


@dataclass
class PipelineConfig:
    """Configurações do pipeline"""
    # Pesquisa de tendências
    trend_query: str = "business trends"
    days_back: int = 7
    min_engagement: float = 8.0
    
    # Criação de pautas
    num_articles: int = 5
    
    # Geração de artigos
    auto_publish: bool = False
    delay_between_articles: int = 30
    
    # Configurações gerais
    output_dir: str = "output"
    save_intermediate: bool = True
    verbose: bool = True


@dataclass
class PipelineResult:
    """Resultado do pipeline"""
    trends_found: int
    briefs_created: int
    articles_generated: int
    articles_published: int
    errors: int
    execution_time: float
    trends_data: List[TrendData]
    article_briefs: List[ArticleBrief]
    generated_articles: List[GeneratedArticle]


class TrendContentPipeline:
    """
    Pipeline completo de criação de conteúdo baseado em tendências
    """
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Inicializar agentes
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Inicializa todos os agentes necessários"""
        try:
            print("🤖 Inicializando agentes...")
            
            self.trend_agent = TrendResearchAgent()
            self.planning_agent = ContentPlanningAgent()
            self.generator_agent = BatchContentGeneratorAgent()
            
            print("✅ Agentes inicializados com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar agentes: {str(e)}")
            raise
    
    def run_pipeline(self) -> PipelineResult:
        """
        Executa o pipeline completo
        
        Returns:
            Resultado do pipeline com todas as métricas
        """
        start_time = datetime.now()
        
        print("\n🚀 INICIANDO PIPELINE DE CRIAÇÃO DE CONTEÚDO")
        print("=" * 60)
        print(f"📊 Configurações:")
        print(f"   Query de tendências: {self.config.trend_query}")
        print(f"   Período: {self.config.days_back} dias")
        print(f"   Número de artigos: {self.config.num_articles}")
        print(f"   Auto-publicação: {self.config.auto_publish}")
        print("=" * 60)
        
        try:
            # Etapa 1: Pesquisa de tendências
            trends_data = self._research_trends()
            
            # Etapa 2: Criação de pautas
            article_briefs = self._create_article_briefs(trends_data)
            
            # Etapa 3: Geração de artigos
            generated_articles = self._generate_articles(article_briefs)
            
            # Calcular tempo de execução
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Criar resultado
            result = PipelineResult(
                trends_found=len(trends_data),
                briefs_created=len(article_briefs),
                articles_generated=len(generated_articles),
                articles_published=sum(1 for a in generated_articles if a.published),
                errors=sum(1 for a in generated_articles if a.status == 'error'),
                execution_time=execution_time,
                trends_data=trends_data,
                article_briefs=article_briefs,
                generated_articles=generated_articles
            )
            
            # Salvar resultados
            if self.config.save_intermediate:
                self._save_results(result)
            
            # Exibir resumo
            self._display_summary(result)
            
            return result
            
        except Exception as e:
            print(f"❌ Erro no pipeline: {str(e)}")
            raise
    
    def _research_trends(self) -> List[TrendData]:
        """Etapa 1: Pesquisa de tendências"""
        print("\n🔍 ETAPA 1: PESQUISANDO TENDÊNCIAS DO LINKEDIN")
        print("-" * 40)
        
        try:
            trends = self.trend_agent.research_trends(
                query=self.config.trend_query,
                days_back=self.config.days_back,
                min_engagement=self.config.min_engagement
            )
            
            print(f"✅ {len(trends)} tendências encontradas")
            
            for i, trend in enumerate(trends, 1):
                print(f"   {i}. {trend.topic} (Engajamento: {trend.engagement_score}/10)")
            
            return trends
            
        except Exception as e:
            print(f"❌ Erro na pesquisa de tendências: {str(e)}")
            raise
    
    def _create_article_briefs(self, trends_data: List[TrendData]) -> List[ArticleBrief]:
        """Etapa 2: Criação de pautas de artigos"""
        print("\n📝 ETAPA 2: CRIANDO PAUTAS DE ARTIGOS")
        print("-" * 40)
        
        try:
            # Converter TrendData para dict para compatibilidade
            trends_dict = [asdict(trend) for trend in trends_data]
            
            briefs = self.planning_agent.create_article_briefs(
                trends_data=trends_dict,
                num_articles=self.config.num_articles
            )
            
            print(f"✅ {len(briefs)} pautas criadas")
            
            for i, brief in enumerate(briefs, 1):
                print(f"   {i}. {brief.title}")
                print(f"      Formato: {brief.content_format}")
                print(f"      Palavras: {brief.estimated_word_count}")
                print(f"      Engajamento esperado: {brief.expected_engagement:.1f}/10")
            
            return briefs
            
        except Exception as e:
            print(f"❌ Erro na criação de pautas: {str(e)}")
            raise
    
    def _generate_articles(self, article_briefs: List[ArticleBrief]) -> List[GeneratedArticle]:
        """Etapa 3: Geração de artigos"""
        print("\n✍️ ETAPA 3: GERANDO ARTIGOS")
        print("-" * 40)
        
        try:
            # Converter ArticleBrief para dict para compatibilidade
            briefs_dict = [asdict(brief) for brief in article_briefs]
            
            articles = self.generator_agent.generate_articles_batch(
                article_briefs=briefs_dict,
                auto_publish=self.config.auto_publish,
                delay_between_articles=self.config.delay_between_articles
            )
            
            print(f"✅ {len(articles)} artigos gerados")
            
            for i, article in enumerate(articles, 1):
                status_icon = "✅" if article.published else "📝" if article.status == "generated" else "❌"
                print(f"   {i}. {status_icon} {article.title}")
                print(f"      Palavras: {article.word_count}")
                print(f"      Status: {article.status}")
            
            return articles
            
        except Exception as e:
            print(f"❌ Erro na geração de artigos: {str(e)}")
            raise
    
    def _save_results(self, result: PipelineResult):
        """Salva resultados intermediários"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Salvar tendências
        trends_file = self.output_dir / f"trends_{timestamp}.json"
        with open(trends_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(trend) for trend in result.trends_data], f, indent=2, ensure_ascii=False)
        
        # Salvar pautas
        briefs_file = self.output_dir / f"briefs_{timestamp}.json"
        with open(briefs_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(brief) for brief in result.article_briefs], f, indent=2, ensure_ascii=False)
        
        # Salvar artigos
        articles_file = self.output_dir / f"articles_{timestamp}.json"
        with open(articles_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(article) for article in result.generated_articles], f, indent=2, ensure_ascii=False)
        
        # Salvar resumo
        summary_file = self.output_dir / f"summary_{timestamp}.json"
        summary_data = {
            "execution_time": result.execution_time,
            "trends_found": result.trends_found,
            "briefs_created": result.briefs_created,
            "articles_generated": result.articles_generated,
            "articles_published": result.articles_published,
            "errors": result.errors,
            "timestamp": timestamp
        }
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados salvos em: {self.output_dir}")
        print(f"   Tendências: {trends_file.name}")
        print(f"   Pautas: {briefs_file.name}")
        print(f"   Artigos: {articles_file.name}")
        print(f"   Resumo: {summary_file.name}")
    
    def _display_summary(self, result: PipelineResult):
        """Exibe resumo final do pipeline"""
        print("\n🎉 PIPELINE CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print(f"⏱️  Tempo de execução: {result.execution_time:.1f} segundos")
        print(f"🔍 Tendências encontradas: {result.trends_found}")
        print(f"📝 Pautas criadas: {result.briefs_created}")
        print(f"✍️  Artigos gerados: {result.articles_generated}")
        print(f"📢 Artigos publicados: {result.articles_published}")
        print(f"❌ Erros: {result.errors}")
        
        if result.articles_generated > 0:
            success_rate = ((result.articles_generated - result.errors) / result.articles_generated) * 100
            print(f"📊 Taxa de sucesso: {success_rate:.1f}%")
        
        print("\n📚 Próximos passos:")
        if not result.articles_published and result.articles_generated > 0:
            print("   1. Revisar artigos gerados")
            print("   2. Publicar manualmente via admin do Django")
            print("   3. Monitorar performance e engajamento")
        else:
            print("   1. Monitorar performance dos artigos publicados")
            print("   2. Analisar métricas de engajamento")
            print("   3. Ajustar estratégias baseado nos resultados")


def create_config_from_args(args) -> PipelineConfig:
    """Cria configuração a partir dos argumentos da linha de comando"""
    return PipelineConfig(
        trend_query=args.query,
        days_back=args.days,
        min_engagement=args.min_engagement,
        num_articles=args.num_articles,
        auto_publish=args.auto_publish,
        delay_between_articles=args.delay,
        output_dir=args.output_dir,
        save_intermediate=not args.no_save,
        verbose=not args.quiet
    )


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Pipeline Completo de Criação de Conteúdo Baseado em Tendências',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Configuração básica (5 artigos)
  python cli/trend_content_pipeline.py

  # Configuração personalizada
  python cli/trend_content_pipeline.py --query "marketing digital" --num-articles 10 --auto-publish

  # Configuração para produção
  python cli/trend_content_pipeline.py --query "tendências 2024" --num-articles 15 --auto-publish --delay 60

  # Configuração de teste
  python cli/trend_content_pipeline.py --num-articles 3 --no-save --quiet
        """
    )
    
    # Argumentos de pesquisa de tendências
    parser.add_argument('--query', default='business trends', 
                       help='Query para pesquisa de tendências (padrão: "business trends")')
    parser.add_argument('--days', type=int, default=7, 
                       help='Número de dias para pesquisar tendências (padrão: 7)')
    parser.add_argument('--min-engagement', type=float, default=8.0, 
                       help='Score mínimo de engajamento (padrão: 8.0)')
    
    # Argumentos de criação de pautas
    parser.add_argument('--num-articles', type=int, default=5, 
                       help='Número de artigos para criar (padrão: 5)')
    
    # Argumentos de geração de artigos
    parser.add_argument('--auto-publish', action='store_true', 
                       help='Publicar artigos automaticamente')
    parser.add_argument('--delay', type=int, default=30, 
                       help='Delay entre artigos em segundos (padrão: 30)')
    
    # Argumentos gerais
    parser.add_argument('--output-dir', default='output', 
                       help='Diretório para salvar resultados (padrão: output)')
    parser.add_argument('--no-save', action='store_true', 
                       help='Não salvar resultados intermediários')
    parser.add_argument('--quiet', action='store_true', 
                       help='Modo silencioso (menos output)')
    
    args = parser.parse_args()
    
    try:
        # Criar configuração
        config = create_config_from_args(args)
        
        # Executar pipeline
        pipeline = TrendContentPipeline(config)
        result = pipeline.run_pipeline()
        
        # Exit code baseado no sucesso
        if result.errors > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n⏹️  Pipeline interrompido pelo usuário")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Erro fatal: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

