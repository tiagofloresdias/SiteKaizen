#!/usr/bin/env python3
"""
Script de teste para o Agente de IA
Verifica se todos os componentes estão funcionando corretamente
"""

import os
import sys
import requests
import json
from pathlib import Path

def test_environment():
    """Testa se o ambiente está configurado corretamente"""
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

def test_django_server():
    """Testa se o servidor Django está rodando"""
    print("\n🌐 Testando servidor Django...")
    
    try:
        response = requests.get('http://localhost:8000/api/blog/stats/', timeout=5)
        if response.status_code == 200:
            print("✅ Servidor Django rodando")
            print(f"✅ API respondendo: {response.status_code}")
            return True
        else:
            print(f"❌ API retornou status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Servidor Django não está rodando")
        print("   Execute: cd src && python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False

def test_ai_agent_import():
    """Testa se o agente de IA pode ser importado"""
    print("\n🤖 Testando importação do agente...")
    
    try:
        # Adicionar src ao path
        src_path = Path(__file__).parent.parent / 'src'
        sys.path.insert(0, str(src_path))
        
        # Importar módulos necessários
        from cli.ai_content_agent import AIContentAgent, BlogAPITool, ContentResearchTool
        print("✅ Módulos do agente importados com sucesso")
        
        # Testar inicialização das tools
        blog_tool = BlogAPITool()
        research_tool = ContentResearchTool()
        print("✅ Tools inicializadas com sucesso")
        
        return True
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_blog_api():
    """Testa a API do blog"""
    print("\n📝 Testando API do blog...")
    
    try:
        # Testar endpoint de estatísticas (público)
        response = requests.get('http://localhost:8000/api/blog/stats/')
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Estatísticas: {stats['total_posts']} posts, {stats['published_posts']} publicados")
        else:
            print(f"❌ Erro ao buscar estatísticas: {response.status_code}")
            return False
        
        # Testar endpoint de posts (requer autenticação)
        response = requests.get('http://localhost:8000/api/blog/posts/')
        if response.status_code == 401:
            print("✅ Autenticação necessária (esperado)")
        elif response.status_code == 200:
            print("✅ API de posts acessível")
        else:
            print(f"⚠️  Status inesperado: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao testar API: {e}")
        return False

def test_ai_agent_creation():
    """Testa a criação do agente de IA"""
    print("\n🚀 Testando criação do agente...")
    
    try:
        from cli.ai_content_agent import AIContentAgent
        
        # Inicializar agente
        agent = AIContentAgent()
        print("✅ Agente de IA inicializado com sucesso")
        
        # Verificar se os agentes foram criados
        if hasattr(agent, 'researcher') and hasattr(agent, 'writer') and hasattr(agent, 'editor'):
            print("✅ Agentes especializados criados")
        else:
            print("❌ Agentes especializados não encontrados")
            return False
        
        # Verificar tools
        if hasattr(agent, 'blog_tool') and hasattr(agent, 'research_tool'):
            print("✅ Tools configuradas")
        else:
            print("❌ Tools não encontradas")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Erro ao criar agente: {e}")
        return False

def test_ai_agent_help():
    """Testa o comando de ajuda do agente"""
    print("\n❓ Testando comando de ajuda...")
    
    try:
        import subprocess
        
        result = subprocess.run([
            sys.executable, 
            str(Path(__file__).parent / 'ai_content_agent.py'),
            '--help'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Comando de ajuda funcionando")
            return True
        else:
            print(f"❌ Erro no comando de ajuda: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Timeout no comando de ajuda")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar comando: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 Teste do Agente de IA - Agência Kaizen")
    print("=" * 50)
    
    tests = [
        ("Ambiente", test_environment),
        ("Servidor Django", test_django_server),
        ("Importação do Agente", test_ai_agent_import),
        ("API do Blog", test_blog_api),
        ("Criação do Agente", test_ai_agent_creation),
        ("Comando de Ajuda", test_ai_agent_help),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"⚠️  {test_name} falhou")
        except Exception as e:
            print(f"❌ {test_name} erro: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! O sistema está funcionando.")
        print("\n📚 Próximos passos:")
        print("1. Crie um post: python cli/ai_content_agent.py --topic 'Teste'")
        print("2. Acesse o admin: http://localhost:8000/admin/")
        print("3. Consulte a documentação: docs/")
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
        print("\n🔧 Soluções comuns:")
        print("1. Verifique se o servidor Django está rodando")
        print("2. Configure as variáveis de ambiente no .env")
        print("3. Execute: python cli/setup_ai_agent.py")
        print("4. Consulte: docs/troubleshooting.md")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

