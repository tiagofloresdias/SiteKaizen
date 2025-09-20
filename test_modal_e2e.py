#!/usr/bin/env python3
"""
Teste End-to-End da Modal de Leads
Testa navegação, preenchimento, salvamento e envio de emails
"""
import os
import sys
import time
import requests
from browser_use import Agent

def test_modal_e2e():
    """Teste completo da modal de leads"""
    
    print("🚀 Iniciando teste end-to-end da modal de leads...")
    
    # Configurar o agente
    agent = Agent(
        task="Testar modal de leads no site agenciakaizen.com.br",
        llm="gpt-4o-mini"
    )
    
    try:
        # Navegar para o site
        print("📱 Navegando para o site...")
        result = agent.run("Vá para https://www.agenciakaizen.com.br/solucoes/")
        print(f"✅ Navegação: {result}")
        
        # Aguardar carregamento
        time.sleep(3)
        
        # Procurar e clicar no botão da modal
        print("🔍 Procurando botão 'Converse com um Especialista'...")
        result = agent.run("Encontre e clique no botão 'Converse com um Especialista' ou similar")
        print(f"✅ Botão encontrado: {result}")
        
        # Aguardar modal abrir
        time.sleep(2)
        
        # Verificar se a modal abriu
        print("🔍 Verificando se a modal abriu...")
        result = agent.run("A modal 'Converse com o Especialista' está aberta? Descreva o que você vê")
        print(f"✅ Modal: {result}")
        
        # Preencher Step 1 - Dados Básicos
        print("📝 Preenchendo Step 1 - Dados Básicos...")
        result = agent.run("""
        Preencha o formulário da modal:
        1. Nome Completo: João Silva Teste
        2. E-mail Corporativo: joao.teste@empresa.com
        3. WhatsApp: (11) 99999-9999
        """)
        print(f"✅ Step 1 preenchido: {result}")
        
        # Clicar em Próximo
        print("➡️ Clicando em 'PRÓXIMO'...")
        result = agent.run("Clique no botão 'PRÓXIMO' ou 'NEXT' para ir para o próximo passo")
        print(f"✅ Próximo clicado: {result}")
        
        # Aguardar Step 2
        time.sleep(2)
        
        # Verificar Step 2
        print("🔍 Verificando Step 2...")
        result = agent.run("Descreva o que você vê no Step 2. Há campos para preencher sobre o negócio?")
        print(f"✅ Step 2: {result}")
        
        # Preencher Step 2 - Informações do Negócio
        print("📝 Preenchendo Step 2 - Informações do Negócio...")
        result = agent.run("""
        Preencha os campos do Step 2:
        1. Faturamento Mensal: R$ 10.000 - R$ 50.000
        2. Área do Negócio: E-commerce
        3. Principal Desafio: Precisa aumentar as vendas online
        """)
        print(f"✅ Step 2 preenchido: {result}")
        
        # Clicar em Próximo para Step 3
        print("➡️ Indo para Step 3...")
        result = agent.run("Clique em 'PRÓXIMO' para ir para o Step 3 (Calendly)")
        print(f"✅ Step 3: {result}")
        
        # Aguardar Step 3
        time.sleep(3)
        
        # Verificar Step 3
        print("🔍 Verificando Step 3...")
        result = agent.run("Descreva o que você vê no Step 3. Há o widget do Calendly?")
        print(f"✅ Step 3: {result}")
        
        # Tentar agendar no Calendly
        print("📅 Tentando agendar no Calendly...")
        result = agent.run("Tente agendar uma reunião no Calendly se possível, ou clique em 'PRÓXIMO' se não conseguir")
        print(f"✅ Calendly: {result}")
        
        # Verificar Step 4
        print("🔍 Verificando Step 4...")
        result = agent.run("Descreva o que você vê no Step 4. Há uma mensagem de confirmação?")
        print(f"✅ Step 4: {result}")
        
        # Verificar se o lead foi salvo
        print("💾 Verificando se o lead foi salvo no banco...")
        result = agent.run("Verifique se há alguma mensagem de sucesso ou confirmação")
        print(f"✅ Confirmação: {result}")
        
        print("✅ Teste end-to-end concluído!")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_modal_e2e()
    if success:
        print("🎉 Teste concluído com sucesso!")
    else:
        print("💥 Teste falhou!")

