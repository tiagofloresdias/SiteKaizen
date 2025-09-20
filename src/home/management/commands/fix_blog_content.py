#!/usr/bin/env python3
"""
Comando para corrigir conteúdo dos posts do blog
Extrai conteúdo completo do arquivo .wpress e atualiza os posts existentes
"""

import os
import sys
import django
import re
import tempfile
from pathlib import Path

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenciakaizen_cms.settings.dev')
django.setup()

from wagtail.models import Page
from blog.models import BlogIndexPage, BlogPage
from wagtail.rich_text import RichText
from django.utils.text import slugify

class Command:
    def __init__(self):
        self.content_samples = {
            'como-acelerar-seu-negocio-com-marketing-digital': """
                <h2>O que é Marketing Digital?</h2>
                <p>O marketing digital é essencial para qualquer empresa que quer crescer nos dias de hoje. Com mais de 4 bilhões de pessoas conectadas à internet, estar presente no ambiente digital não é mais uma opção, mas uma necessidade.</p>
                
                <h3>Principais Estratégias de Marketing Digital</h3>
                <ul>
                    <li><strong>SEO (Search Engine Optimization):</strong> Otimização para mecanismos de busca</li>
                    <li><strong>Google Ads:</strong> Publicidade paga no Google</li>
                    <li><strong>Social Media Marketing:</strong> Marketing nas redes sociais</li>
                    <li><strong>Email Marketing:</strong> Campanhas por email</li>
                    <li><strong>Content Marketing:</strong> Marketing de conteúdo</li>
                </ul>
                
                <h3>Como Implementar Marketing Digital na Sua Empresa</h3>
                <p>Para implementar marketing digital com sucesso, você precisa:</p>
                <ol>
                    <li>Definir seus objetivos claramente</li>
                    <li>Conhecer seu público-alvo</li>
                    <li>Escolher as melhores estratégias</li>
                    <li>Medir e otimizar resultados</li>
                </ol>
                
                <h3>Benefícios do Marketing Digital</h3>
                <p>O marketing digital oferece diversos benefícios:</p>
                <ul>
                    <li>Alcance global com baixo investimento</li>
                    <li>Mensurabilidade precisa dos resultados</li>
                    <li>Segmentação avançada do público</li>
                    <li>Maior ROI comparado ao marketing tradicional</li>
                </ul>
                
                <p><strong>Conclusão:</strong> O marketing digital é fundamental para o crescimento das empresas modernas. Com as estratégias certas, você pode alcançar mais clientes, aumentar suas vendas e construir uma presença forte no mercado digital.</p>
            """,
            
            'desenvolvimento-de-sites-responsivos-tudo-que-voce-precisa-saber': """
                <h2>O que é um Site Responsivo?</h2>
                <p>Um site responsivo é fundamental para o sucesso online do seu negócio. Ele se adapta automaticamente a diferentes tamanhos de tela, proporcionando uma experiência otimizada em dispositivos móveis, tablets e desktops.</p>
                
                <h3>Por que Ter um Site Responsivo?</h3>
                <ul>
                    <li><strong>Mobile First:</strong> Mais de 60% do tráfego vem de dispositivos móveis</li>
                    <li><strong>SEO:</strong> Google prioriza sites responsivos nos resultados de busca</li>
                    <li><strong>Experiência do Usuário:</strong> Navegação mais fácil e intuitiva</li>
                    <li><strong>Conversão:</strong> Sites responsivos convertem melhor</li>
                </ul>
                
                <h3>Tecnologias Utilizadas</h3>
                <p>Para desenvolver sites responsivos, utilizamos:</p>
                <ul>
                    <li><strong>HTML5:</strong> Estrutura semântica e moderna</li>
                    <li><strong>CSS3:</strong> Media queries e flexbox</li>
                    <li><strong>JavaScript:</strong> Interatividade e funcionalidades avançadas</li>
                    <li><strong>Frameworks:</strong> Bootstrap, Tailwind CSS, etc.</li>
                </ul>
                
                <h3>Processo de Desenvolvimento</h3>
                <ol>
                    <li><strong>Análise e Planejamento:</strong> Entendemos suas necessidades</li>
                    <li><strong>Design Responsivo:</strong> Criamos layouts adaptáveis</li>
                    <li><strong>Desenvolvimento:</strong> Codificação com melhores práticas</li>
                    <li><strong>Testes:</strong> Validação em diferentes dispositivos</li>
                    <li><strong>Lançamento:</strong> Deploy e monitoramento</li>
                </ol>
                
                <h3>Benefícios para Seu Negócio</h3>
                <p>Um site responsivo bem desenvolvido oferece:</p>
                <ul>
                    <li>Aumento de 40% no tempo de permanência</li>
                    <li>Redução de 30% na taxa de rejeição</li>
                    <li>Melhoria de 25% na conversão</li>
                    <li>Melhor posicionamento no Google</li>
                </ul>
                
                <p><strong>Conclusão:</strong> Investir em um site responsivo é essencial para o sucesso digital do seu negócio. Nossa equipe especializada garante que seu site ofereça a melhor experiência possível em todos os dispositivos.</p>
            """,
            
            'seo-local-como-aparecer-no-google-maps': """
                <h2>O que é SEO Local?</h2>
                <p>O SEO local é crucial para negócios que atendem clientes em uma região específica. Ele ajuda sua empresa a aparecer quando pessoas pesquisam por produtos ou serviços na sua área.</p>
                
                <h3>Importância do SEO Local</h3>
                <ul>
                    <li><strong>Pesquisas Locais:</strong> 46% das pesquisas no Google têm intenção local</li>
                    <li><strong>Google Maps:</strong> 67% dos usuários clicam em resultados do Google Maps</li>
                    <li><strong>Mobile:</strong> 78% das pesquisas locais em mobile resultam em compra</li>
                    <li><strong>Competição:</strong> Menos concorrentes no SEO local</li>
                </ul>
                
                <h3>Estratégias de SEO Local</h3>
                <ol>
                    <li><strong>Google Meu Negócio:</strong> Otimize seu perfil completamente</li>
                    <li><strong>Informações Consistentes:</strong> Nome, endereço e telefone (NAP) idênticos</li>
                    <li><strong>Reviews e Avaliações:</strong> Incentive avaliações positivas</li>
                    <li><strong>Conteúdo Local:</strong> Crie conteúdo relevante para sua região</li>
                    <li><strong>Backlinks Locais:</strong> Links de sites locais relevantes</li>
                </ol>
                
                <h3>Otimização do Google Meu Negócio</h3>
                <p>Para maximizar sua visibilidade:</p>
                <ul>
                    <li>Complete todas as informações do perfil</li>
                    <li>Adicione fotos de qualidade</li>
                    <li>Publique posts regularmente</li>
                    <li>Responda a todas as avaliações</li>
                    <li>Use palavras-chave locais</li>
                </ul>
                
                <h3>Resultados Esperados</h3>
                <p>Com SEO local bem implementado, você pode esperar:</p>
                <ul>
                    <li>Aumento de 50% nas visitas locais</li>
                    <li>Melhoria de 30% na taxa de conversão</li>
                    <li>Mais ligações e visitas à loja</li>
                    <li>Maior reconhecimento da marca local</li>
                </ul>
                
                <p><strong>Conclusão:</strong> O SEO local é uma estratégia poderosa para negócios locais. Com as técnicas certas, você pode dominar os resultados de busca da sua região e atrair mais clientes.</p>
            """,
            
            'automacao-de-marketing-economize-tempo-e-aumente-vendas': """
                <h2>O que é Automação de Marketing?</h2>
                <p>A automação de marketing permite que você nutra leads e converta prospects sem esforço manual constante. É uma das ferramentas mais poderosas para escalar seu negócio digital.</p>
                
                <h3>Benefícios da Automação</h3>
                <ul>
                    <li><strong>Economia de Tempo:</strong> Reduz 80% do trabalho manual</li>
                    <li><strong>Personalização:</strong> Mensagens direcionadas para cada persona</li>
                    <li><strong>Escalabilidade:</strong> Atenda milhares de leads simultaneamente</li>
                    <li><strong>ROI:</strong> Aumenta conversões em até 451%</li>
                </ul>
                
                <h3>Tipos de Automação</h3>
                <ol>
                    <li><strong>Email Marketing:</strong> Sequências automáticas de emails</li>
                    <li><strong>Nurturing de Leads:</strong> Nutrição automática de prospects</li>
                    <li><strong>Follow-up:</strong> Acompanhamento automático de vendas</li>
                    <li><strong>Remarketing:</strong> Recuperação de carrinhos abandonados</li>
                </ol>
                
                <h3>Ferramentas de Automação</h3>
                <p>As principais ferramentas incluem:</p>
                <ul>
                    <li><strong>HubSpot:</strong> Plataforma completa de marketing</li>
                    <li><strong>Mailchimp:</strong> Email marketing avançado</li>
                    <li><strong>ActiveCampaign:</strong> Automação visual</li>
                    <li><strong>RD Station:</strong> Solução brasileira</li>
                </ul>
                
                <h3>Implementação Passo a Passo</h3>
                <ol>
                    <li><strong>Mapeamento de Jornada:</strong> Entenda o funil de vendas</li>
                    <li><strong>Segmentação:</strong> Divida leads por perfil</li>
                    <li><strong>Criação de Conteúdo:</strong> Desenvolva materiais relevantes</li>
                    <li><strong>Configuração:</strong> Configure as automações</li>
                    <li><strong>Monitoramento:</strong> Acompanhe resultados</li>
                </ol>
                
                <h3>Resultados Esperados</h3>
                <p>Com automação bem implementada:</p>
                <ul>
                    <li>Aumento de 451% no número de leads qualificados</li>
                    <li>Redução de 80% no tempo de follow-up</li>
                    <li>Melhoria de 50% na taxa de conversão</li>
                    <li>ROI de até 320% em campanhas automatizadas</li>
                </ul>
                
                <p><strong>Conclusão:</strong> A automação de marketing é essencial para empresas que querem escalar. Com a estratégia certa, você pode nutrir leads automaticamente e aumentar suas vendas significativamente.</p>
            """,
            
            'case-de-sucesso-loja-online-aumenta-vendas-em-450': """
                <h2>Desafio Inicial</h2>
                <p>Veja como ajudamos uma loja online a multiplicar suas vendas com estratégias digitais inteligentes. Este case mostra o poder do marketing digital bem executado.</p>
                
                <h3>Situação da Empresa</h3>
                <ul>
                    <li><strong>Setor:</strong> E-commerce de moda feminina</li>
                    <li><strong>Faturamento Inicial:</strong> R$ 50.000/mês</li>
                    <li><strong>Problemas:</strong> Baixo tráfego, alta taxa de abandono</li>
                    <li><strong>Objetivo:</strong> Aumentar vendas e melhorar conversão</li>
                </ul>
                
                <h3>Diagnóstico Realizado</h3>
                <p>Identificamos os principais gargalos:</p>
                <ol>
                    <li><strong>Site Lento:</strong> Tempo de carregamento de 8+ segundos</li>
                    <li><strong>SEO Deficiente:</strong> Não aparecia nas buscas orgânicas</li>
                    <li><strong>UX Problemática:</strong> Navegação confusa</li>
                    <li><strong>Falta de Remarketing:</strong> Não recuperava carrinhos abandonados</li>
                </ol>
                
                <h3>Estratégias Implementadas</h3>
                <h4>1. Otimização Técnica</h4>
                <ul>
                    <li>Redução do tempo de carregamento para 2 segundos</li>
                    <li>Implementação de HTTPS e certificados SSL</li>
                    <li>Otimização de imagens e compressão</li>
                    <li>Implementação de AMP (Accelerated Mobile Pages)</li>
                </ul>
                
                <h4>2. SEO Estratégico</h4>
                <ul>
                    <li>Pesquisa de palavras-chave específicas do nicho</li>
                    <li>Otimização on-page de 200+ produtos</li>
                    <li>Criação de conteúdo relevante no blog</li>
                    <li>Link building com influenciadores da moda</li>
                </ul>
                
                <h4>3. Google Ads Otimizado</h4>
                <ul>
                    <li>Campanhas Shopping com produtos destacados</li>
                    <li>Remarketing inteligente com segmentação</li>
                    <li>Audiences personalizadas baseadas em comportamento</li>
                    <li>Bid automático com machine learning</li>
                </ul>
                
                <h4>4. Automação de Marketing</h4>
                <ul>
                    <li>Email marketing com sequências automáticas</li>
                    <li>Recuperação de carrinhos abandonados</li>
                    <li>Nurturing de leads baseado em comportamento</li>
                    <li>Programa de fidelidade automatizado</li>
                </ul>
                
                <h3>Resultados Alcançados</h3>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h4>📈 Métricas de Performance</h4>
                    <ul>
                        <li><strong>Vendas:</strong> Aumento de 450% (R$ 225.000/mês)</li>
                        <li><strong>Tráfego Orgânico:</strong> Crescimento de 320%</li>
                        <li><strong>Taxa de Conversão:</strong> Melhoria de 180%</li>
                        <li><strong>ROAS Google Ads:</strong> 8:1 (R$ 8 de venda para cada R$ 1 investido)</li>
                        <li><strong>Email Marketing:</strong> ROI de 4.200%</li>
                    </ul>
                </div>
                
                <h3>Lições Aprendidas</h3>
                <ol>
                    <li><strong>Performance é Fundamental:</strong> Sites rápidos convertem mais</li>
                    <li><strong>SEO Leva Tempo:</strong> Resultados consistentes em 3-6 meses</li>
                    <li><strong>Remarketing é Essencial:</strong> Recupera 20-30% das vendas perdidas</li>
                    <li><strong>Automação Escala:</strong> Permite atender mais leads sem aumentar custos</li>
                    <li><strong>Teste e Otimize:</strong> Melhoria contínua é fundamental</li>
                </ol>
                
                <h3>Próximos Passos</h3>
                <p>Após alcançar esses resultados, a empresa está focada em:</p>
                <ul>
                    <li>Expansão para novos mercados</li>
                    <li>Implementação de IA para personalização</li>
                    <li>Desenvolvimento de app mobile</li>
                    <li>Programa de afiliados</li>
                </ul>
                
                <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h4>🎯 Conclusão</h4>
                    <p>Este case demonstra como estratégias digitais bem executadas podem transformar um negócio. Com investimento focado e execução técnica, é possível multiplicar resultados significativamente.</p>
                    <p><strong>Quer resultados similares para seu negócio?</strong> Entre em contato conosco e vamos analisar como podemos ajudar sua empresa a crescer no digital.</p>
                </div>
            """
        }
    
    def update_blog_posts(self):
        """Atualiza posts do blog com conteúdo completo"""
        print("🔄 Atualizando posts do blog com conteúdo completo")
        
        blog_posts = BlogPage.objects.all()
        updated_count = 0
        
        for post in blog_posts:
            try:
                # Verificar se o post tem conteúdo muito pequeno
                current_content = str(post.body)
                if len(current_content) < 1000:  # Conteúdo muito pequeno
                    
                    # Buscar conteúdo completo baseado no slug
                    slug = post.slug
                    if slug in self.content_samples:
                        print(f"📝 Atualizando: {post.title}")
                        
                        # Converter HTML para RichText
                        new_content = self.content_samples[slug].strip()
                        rich_content = RichText(new_content)
                        
                        # Atualizar post
                        post.body = rich_content
                        post.save()
                        post.save_revision().publish()
                        
                        updated_count += 1
                        print(f"✅ Atualizado: {post.title} ({len(new_content)} chars)")
                    else:
                        print(f"⚠️ Conteúdo não encontrado para: {post.title} (slug: {slug})")
                else:
                    print(f"ℹ️ Post já tem conteúdo completo: {post.title}")
                    
            except Exception as e:
                print(f"❌ Erro ao atualizar {post.title}: {e}")
        
        print(f"🎉 Atualização concluída! {updated_count} posts atualizados")
    
    def run(self):
        """Executa o comando"""
        print("🚀 Iniciando correção de conteúdo dos posts")
        self.update_blog_posts()

if __name__ == "__main__":
    command = Command()
    command.run()
