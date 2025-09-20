#!/usr/bin/env python3
"""
Teste simples da API de leads
"""
import requests
import json

def test_api():
    """Teste da API de leads"""
    
    print("🔍 Testando API de leads...")
    
    # Dados de teste para Step 1
    data_step1 = {
        'step': '1',
        'name': 'João Silva Teste',
        'email': 'joao.teste@empresa.com',
        'phone': '+5511999999999'
    }
    
    try:
        # Testar Step 1
        print("📝 Testando Step 1...")
        response = requests.post(
            'https://www.agenciakaizen.com.br/leads/api/lead/',
            json=data_step1,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                lead_id = result.get('lead_id')
                print(f"✅ Lead criado com sucesso! ID: {lead_id}")
                
                # Testar Step 2
                print("📝 Testando Step 2...")
                data_step2 = {
                    'step': '2',
                    'lead_id': lead_id,
                    'monthly_revenue': '10k_50k',
                    'business_area': 'ecommerce',
                    'main_challenge': 'Precisa aumentar as vendas online',
                    'website_social': 'https://exemplo.com'
                }
                
                response2 = requests.post(
                    'https://www.agenciakaizen.com.br/leads/api/lead/',
                    json=data_step2,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                
                print(f"Step 2 - Status Code: {response2.status_code}")
                print(f"Step 2 - Response: {response2.text}")
                
                if response2.status_code == 200:
                    result2 = response2.json()
                    if result2.get('success'):
                        print("✅ Step 2 salvo com sucesso!")
                        return True
                    else:
                        print(f"❌ Erro no Step 2: {result2.get('error')}")
                        return False
                else:
                    print(f"❌ Erro HTTP no Step 2: {response2.status_code}")
                    return False
            else:
                print(f"❌ Erro no Step 1: {result.get('error')}")
                return False
        else:
            print(f"❌ Erro HTTP no Step 1: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        return False

if __name__ == "__main__":
    success = test_api()
    if success:
        print("🎉 Teste da API concluído com sucesso!")
    else:
        print("💥 Teste da API falhou!")

