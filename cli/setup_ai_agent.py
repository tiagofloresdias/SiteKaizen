#!/usr/bin/env python3
"""
Script de configuração do Agente de IA para Criação de Conteúdos
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Executa um comando e exibe o resultado"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Concluído")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        if e.stderr:
            print(f"Erro: {e.stderr}")
        return False

def create_env_file():
    """Cria arquivo .env com configurações necessárias"""
    env_file = Path(__file__).parent.parent / '.env'
    
    if env_file.exists():
        print("📄 Arquivo .env já existe")
        return
    
    env_content = """# Configurações do Agente de IA
OPENAI_API_KEY=your_openai_api_key_here
BLOG_API_TOKEN=your_blog_api_token_here

# Configurações do Django
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,www.agenciakaizen.com.br

# Configurações de Email
SENDGRID_API_KEY=your_sendgrid_key_here
DEFAULT_FROM_EMAIL=noreply@www.agenciakaizen.com.br
COMMERCIAL_EMAIL=comercial@www.agenciakaizen.com.br
"""
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"✅ Arquivo .env criado em {env_file}")

def install_dependencies():
    """Instala as dependências necessárias"""
    requirements_file = Path(__file__).parent.parent / 'src' / 'requirements.txt'
    
    if not requirements_file.exists():
        print("❌ Arquivo requirements.txt não encontrado")
        return False
    
    # Ativar ambiente virtual
    venv_path = Path(__file__).parent.parent / 'venv'
    if not venv_path.exists():
        print("❌ Ambiente virtual não encontrado. Execute primeiro: python -m venv venv")
        return False
    
    # Determinar comando pip baseado no OS
    if os.name == 'nt':  # Windows
        pip_cmd = str(venv_path / 'Scripts' / 'pip')
    else:  # Linux/Mac
        pip_cmd = str(venv_path / 'bin' / 'pip')
    
    # Instalar dependências
    return run_command(f"{pip_cmd} install -r {requirements_file}", "Instalando dependências")

def create_django_migrations():
    """Cria e aplica migrações do Django"""
    manage_py = Path(__file__).parent.parent / 'src' / 'manage.py'
    
    if not manage_py.exists():
        print("❌ manage.py não encontrado")
        return False
    
    # Criar migrações
    success1 = run_command(
        f"cd {manage_py.parent} && python manage.py makemigrations",
        "Criando migrações do Django"
    )
    
    # Aplicar migrações
    success2 = run_command(
        f"cd {manage_py.parent} && python manage.py migrate",
        "Aplicando migrações do Django"
    )
    
    return success1 and success2

def create_superuser():
    """Cria superusuário do Django"""
    manage_py = Path(__file__).parent.parent / 'src' / 'manage.py'
    
    print("\n👤 Criando superusuário do Django...")
    print("Execute manualmente: cd src && python manage.py createsuperuser")
    return True

def setup_blog_api_token():
    """Configura token de API para o blog"""
    print("\n🔑 Configuração do Token de API:")
    print("1. Acesse o admin do Django: http://localhost:8000/admin/")
    print("2. Vá em 'Tokens' e crie um novo token")
    print("3. Adicione o token no arquivo .env como BLOG_API_TOKEN")
    return True

def test_ai_agent():
    """Testa o agente de IA"""
    agent_script = Path(__file__).parent / 'ai_content_agent.py'
    
    if not agent_script.exists():
        print("❌ Script do agente não encontrado")
        return False
    
    print("\n🧪 Testando agente de IA...")
    print("Execute: python cli/ai_content_agent.py --topic 'Marketing Digital' --help")
    return True

def main():
    """Função principal de configuração"""
    print("🚀 Configurando Agente de IA para Criação de Conteúdos")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not Path(__file__).parent.parent.name == 'agenciakaizen':
        print("❌ Execute este script a partir do diretório raiz do projeto")
        sys.exit(1)
    
    steps = [
        ("Criando arquivo .env", create_env_file),
        ("Instalando dependências", install_dependencies),
        ("Criando migrações Django", create_django_migrations),
        ("Configurando token de API", setup_blog_api_token),
        ("Testando agente", test_ai_agent),
    ]
    
    success_count = 0
    total_steps = len(steps)
    
    for step_name, step_func in steps:
        if step_func():
            success_count += 1
        else:
            print(f"⚠️  {step_name} falhou, mas continuando...")
    
    print("\n" + "=" * 60)
    print(f"📊 Configuração concluída: {success_count}/{total_steps} passos executados")
    
    if success_count == total_steps:
        print("✅ Configuração completa! O agente está pronto para uso.")
    else:
        print("⚠️  Alguns passos falharam. Verifique os erros acima.")
    
    print("\n📚 Próximos passos:")
    print("1. Configure sua OPENAI_API_KEY no arquivo .env")
    print("2. Crie um superusuário: cd src && python manage.py createsuperuser")
    print("3. Inicie o servidor: cd src && python manage.py runserver")
    print("4. Crie um token de API no admin do Django")
    print("5. Teste o agente: python cli/ai_content_agent.py --topic 'Marketing Digital'")

if __name__ == "__main__":
    main()

