#!/usr/bin/env python3
"""
Script de teste para o Pipeline de Criação de Conteúdo
Testa todos os componentes do sistema de tendências
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_environment():
    """Testa se o ambiente está configurado"""
    print("🔍 Testando ambiente...")
    
    # Verificar Python
    print(f"✅ Python: {sys.version}")
    
    # Verificar arquivo .env
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        print("✅ Arquivo .env encontrado")
    else:
        print("❌ Arquivo .env não encontrado")
        return False
    
    # Verificar variáveis de ambiente
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print("✅ OPENAI_API_KEY configurada")
    else:
        print("❌ OPENAI_API_KEY não configurada")
        return False
    
    return True

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    print("\n📦 Testando importações...")
    
    try:
        from trend_research_agent import TrendResearchAgent
        print("✅ TrendResearchAgent importado")
    except Exception as e:
        print(f"❌ Erro ao importar TrendResearchAgent: {e}")
        return False
    
    try:
        from content_planning_agent import ContentPlanningAgent
        print("✅ ContentPlanningAgent importado")
    except Exception as e:
        print(f"❌ Erro ao importar ContentPlanningAgent: {e}")
        return False
    
    try:
        from batch_content_generator import BatchContentGeneratorAgent
        print("✅ BatchContentGeneratorAgent importado")
    except Exception as e:
        print(f"❌ Erro ao importar BatchContentGeneratorAgent: {e}")
        return False
    
    try:
        from trend_content_pipeline import TrendContentPipeline, PipelineConfig
        print("✅ TrendContentPipeline importado")
    except Exception as e:
        print(f"❌ Erro ao importar TrendContentPipeline: {e}")
        return False
    
    return True

def test_agents_initialization():
    """Testa se os agentes podem ser inicializados"""
    print("\n🤖 Testando inicialização dos agentes...")
    
    try:
        from trend_research_agent import TrendResearchAgent
        agent = TrendResearchAgent()
        print("✅ TrendResearchAgent inicializado")
    except Exception as e:
        print(f"❌ Erro ao inicializar TrendResearchAgent: {e}")
        return False
    
    try:
        from content_planning_agent import ContentPlanningAgent
        agent = ContentPlanningAgent()
        print("✅ ContentPlanningAgent inicializado")
    except Exception as e:
        print(f"❌ Erro ao inicializar ContentPlanningAgent: {e}")
        return False
    
    try:
        from batch_content_generator import BatchContentGeneratorAgent
        agent = BatchContentGeneratorAgent()
        print("✅ BatchContentGeneratorAgent inicializado")
    except Exception as e:
        print(f"❌ Erro ao inicializar BatchContentGeneratorAgent: {e}")
        return False
    
    return True

def test_trend_research():
    """Testa pesquisa de tendências"""
    print("\n🔍 Testando pesquisa de tendências...")
    
    try:
        from trend_research_agent import TrendResearchAgent
        
        agent = TrendResearchAgent()
        trends = agent.research_trends(
            query="business trends",
            days_back=7,
            min_engagement=8.0
        )
        
        print(f"✅ {len(trends)} tendências encontradas")
        
        for i, trend in enumerate(trends[:3], 1):  # Mostrar apenas as 3 primeiras
            print(f"   {i}. {trend.topic} (Engajamento: {trend.engagement_score}/10)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na pesquisa de tendências: {e}")
        return False

def test_content_planning():
    """Testa criação de pautas"""
    print("\n📝 Testando criação de pautas...")
    
    try:
        from content_planning_agent import ContentPlanningAgent
        
        agent = ContentPlanningAgent()
        
        # Dados de teste
        trends_data = [
            {
                "topic": "Inteligência Artificial nos Negócios",
                "engagement_score": 9.2,
                "target_audience": "Executivos e gestores",
                "key_points": ["Automação", "Análise preditiva", "Chatbots"],
                "hashtags": ["#IA", "#Negocios", "#Inovacao"]
            }
        ]
        
        briefs = agent.create_article_briefs(trends_data, num_articles=2)
        
        print(f"✅ {len(briefs)} pautas criadas")
        
        for i, brief in enumerate(briefs, 1):
            print(f"   {i}. {brief.title}")
            print(f"      Formato: {brief.content_format}")
            print(f"      Palavras: {brief.estimated_word_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na criação de pautas: {e}")
        return False

def test_pipeline_config():
    """Testa configuração do pipeline"""
    print("\n⚙️ Testando configuração do pipeline...")
    
    try:
        from trend_content_pipeline import PipelineConfig
        
        config = PipelineConfig(
            trend_query="test trends",
            num_articles=2,
            auto_publish=False
        )
        
        print("✅ Configuração criada com sucesso")
        print(f"   Query: {config.trend_query}")
        print(f"   Artigos: {config.num_articles}")
        print(f"   Auto-publicação: {config.auto_publish}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

def test_pipeline_execution():
    """Testa execução do pipeline (modo teste)"""
    print("\n🚀 Testando execução do pipeline...")
    
    try:
        from trend_content_pipeline import TrendContentPipeline, PipelineConfig
        
        # Configuração de teste
        config = PipelineConfig(
            trend_query="test trends",
            num_articles=2,
            auto_publish=False,
            save_intermediate=True,
            output_dir="test_output"
        )
        
        pipeline = TrendContentPipeline(config)
        print("✅ Pipeline inicializado")
        
        # Executar pipeline
        result = pipeline.run_pipeline()
        
        print("✅ Pipeline executado com sucesso")
        print(f"   Tendências: {result.trends_found}")
        print(f"   Pautas: {result.briefs_created}")
        print(f"   Artigos: {result.articles_generated}")
        print(f"   Publicados: {result.articles_published}")
        print(f"   Erros: {result.errors}")
        print(f"   Tempo: {result.execution_time:.1f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na execução do pipeline: {e}")
        return False

def test_django_integration():
    """Testa integração com Django"""
    print("\n🌐 Testando integração com Django...")
    
    try:
        import requests
        
        # Testar se o servidor Django está rodando
        response = requests.get('http://localhost:8000/api/blog/stats/', timeout=5)
        
        if response.status_code == 200:
            print("✅ Servidor Django respondendo")
            stats = response.json()
            print(f"   Posts totais: {stats.get('total_posts', 0)}")
            return True
        else:
            print(f"⚠️ Servidor Django retornou status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Servidor Django não está rodando")
        print("   Execute: cd src && python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Erro na integração Django: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 TESTE DO PIPELINE DE CRIAÇÃO DE CONTEÚDO")
    print("=" * 60)
    
    tests = [
        ("Ambiente", test_environment),
        ("Importações", test_imports),
        ("Inicialização dos Agentes", test_agents_initialization),
        ("Pesquisa de Tendências", test_trend_research),
        ("Criação de Pautas", test_content_planning),
        ("Configuração do Pipeline", test_pipeline_config),
        ("Integração Django", test_django_integration),
        ("Execução do Pipeline", test_pipeline_execution),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"⚠️ {test_name} falhou")
        except Exception as e:
            print(f"❌ {test_name} erro: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! O sistema está funcionando.")
        print("\n📚 Próximos passos:")
        print("1. Execute o pipeline: python cli/trend_content_pipeline.py")
        print("2. Configure auto-publicação: --auto-publish")
        print("3. Ajuste o número de artigos: --num-articles 10")
        print("4. Monitore os resultados em output/")
    else:
        print("⚠️ Alguns testes falharam. Verifique os erros acima.")
        print("\n🔧 Soluções comuns:")
        print("1. Configure OPENAI_API_KEY no .env")
        print("2. Execute: cd src && python manage.py runserver")
        print("3. Instale dependências: pip install -r src/requirements.txt")
        print("4. Consulte: docs/troubleshooting.md")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

