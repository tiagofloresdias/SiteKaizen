#!/usr/bin/env python3
"""
Script para popular dados de exemplo na HomePage
Resolve o problema das seções em branco criando conteúdo dinâmico via StreamField
"""

import os
import sys
import django
import json

# Adiciona o diretório src ao path
sys.path.append('/var/www/agenciakaizen/src')

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenciakaizen_cms.settings.dev')
django.setup()

from wagtail.models import Site, Page
from home.models import HomePage
from wagtail.images.models import Image
from wagtail.documents.models import Document

def create_sample_images():
    """Cria imagens de exemplo se não existirem"""
    # Para este exemplo, vamos usar imagens placeholder
    # Em produção, você deve fazer upload de imagens reais
    print("📸 Criando imagens de exemplo...")
    
    # Você pode fazer upload de imagens reais via admin ou usar placeholders
    # Por agora, vamos deixar como None para não quebrar
    return None

def populate_homepage():
    """Popula a HomePage com dados de exemplo"""
    print("🏠 Populando HomePage com dados dinâmicos...")
    
    try:
        # Busca a HomePage existente
        homepage = HomePage.objects.first()
        
        if not homepage:
            print("❌ HomePage não encontrada. Execute primeiro: python manage.py migrate")
            return False
        
        # Atualiza campos básicos
        homepage.hero_title = "Aceleramos negócios e lançamos foguetes"
        homepage.hero_subtitle = "<p>Desde 2014, ajudamos empresas a crescer com estratégias afiadas, dados precisos e um time de elite. Se sua meta é escalar, nós temos o combustível.</p>"
        
        homepage.about_title = "Somos uma aceleradora de vendas."
        homepage.about_text = "<p>Com processos, metodologia e execução prática, ajudamos empresas a crescer de forma sustentável e escalável.</p>"
        
        # Cria dados para StreamField
        stream_data = []
        
        # Seção de Resultados
        results_data = {
            "type": "results_section",
            "value": {
                "title": "Resultados falam mais do que promessas.",
                "subtitle": "Nós entregamos performance de verdade. Confira alguns dos nossos resultados:",
                "results": [
                    {
                        "type": "result_card",
                        "value": {
                            "title": "Dashboard de Vendas",
                            "description": "Aumento de 300% nas vendas em 6 meses",
                            "icon": "fas fa-chart-line"
                        }
                    },
                    {
                        "type": "result_card", 
                        "value": {
                            "title": "Analytics Avançado",
                            "description": "ROI de 450% em campanhas digitais",
                            "icon": "fas fa-chart-bar"
                        }
                    },
                    {
                        "type": "result_card",
                        "value": {
                            "title": "Gestão de Leads",
                            "description": "Conversão de 25% em oportunidades",
                            "icon": "fas fa-chart-pie"
                        }
                    }
                ]
            }
        }
        stream_data.append(results_data)
        
        # Seção de Soluções
        solutions_data = {
            "type": "solutions_section",
            "value": {
                "title": "Criamos máquinas de vendas.",
                "subtitle": "Para cada desafio temos uma solução própria...",
                "solutions": [
                    {
                        "type": "solution_card",
                        "value": {
                            "title": "Leadspot",
                            "description": "CRM exclusivo para negócios locais",
                            "icon": "fas fa-rocket"
                        }
                    },
                    {
                        "type": "solution_card",
                        "value": {
                            "title": "Launcher",
                            "description": "Lançamento e vendas previsíveis",
                            "icon": "fas fa-play"
                        }
                    },
                    {
                        "type": "solution_card",
                        "value": {
                            "title": "Fluxo",
                            "description": "Implementação de funis e automações",
                            "icon": "fas fa-cogs"
                        }
                    },
                    {
                        "type": "solution_card",
                        "value": {
                            "title": "Hacker das Vendas",
                            "description": "Mentoria de vendas",
                            "icon": "fas fa-user-tie"
                        }
                    }
                ]
            }
        }
        stream_data.append(solutions_data)
        
        # Seção de Competências
        competences_data = {
            "type": "competences_section",
            "value": {
                "title": "Escalar um negócio requer mais do que apenas tráfego pago",
                "competences": [
                    {
                        "type": "competence_card",
                        "value": {
                            "title": "Geração de Oportunidades de Venda",
                            "icon": "fas fa-bullseye"
                        }
                    },
                    {
                        "type": "competence_card",
                        "value": {
                            "title": "Assessoria de Mídia Paga",
                            "icon": "fas fa-ad"
                        }
                    },
                    {
                        "type": "competence_card",
                        "value": {
                            "title": "Branding",
                            "icon": "fas fa-palette"
                        }
                    },
                    {
                        "type": "competence_card",
                        "value": {
                            "title": "Neuromarketing",
                            "icon": "fas fa-brain"
                        }
                    }
                ]
            }
        }
        stream_data.append(competences_data)
        
        # Seção de Call-to-Action
        cta_data = {
            "type": "cta_section",
            "value": {
                "title": "Avaliação Gratuita",
                "subtitle": "Consulte um de nossos especialistas em menos de 5 minutos",
                "phone": "0800-550-8000",
                "whatsapp_text": "Olá! Vim pelo site da Agência Kaizen e gostaria de saber mais sobre os serviços."
            }
        }
        stream_data.append(cta_data)
        
        # Atualiza o StreamField
        homepage.body = json.dumps(stream_data)
        
        # Salva as alterações
        homepage.save()
        
        print("✅ HomePage atualizada com sucesso!")
        print("📊 Dados populados:")
        print(f"   - Hero: {homepage.hero_title}")
        print(f"   - Sobre: {homepage.about_title}")
        print(f"   - Seções dinâmicas: {len(stream_data)} seções")
        print("")
        print("🌐 Acesse o admin em: http://localhost:8000/admin/")
        print("📝 Edite a HomePage para personalizar o conteúdo")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao popular HomePage: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Iniciando população de dados da HomePage...")
    print("=" * 50)
    
    success = populate_homepage()
    
    print("=" * 50)
    if success:
        print("🎉 Processo concluído com sucesso!")
        print("")
        print("📋 Próximos passos:")
        print("1. Acesse o admin do Wagtail")
        print("2. Vá em Páginas > Home Page")
        print("3. Edite o conteúdo conforme necessário")
        print("4. Visualize no frontend")
    else:
        print("❌ Processo falhou. Verifique os logs acima.")
        sys.exit(1)

if __name__ == "__main__":
    main()
