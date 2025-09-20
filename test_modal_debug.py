#!/usr/bin/env python3
"""
Teste de debug da modal de leads
"""
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_modal_debug():
    """Teste de debug da modal"""
    
    print("🔍 Iniciando teste de debug da modal...")
    
    # Configurar Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navegar para a página
        print("📱 Navegando para https://www.agenciakaizen.com.br/solucoes/")
        driver.get("https://www.agenciakaizen.com.br/solucoes/")
        
        # Aguardar carregamento
        time.sleep(3)
        
        # Procurar botão da modal
        print("🔍 Procurando botão da modal...")
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-bs-toggle='modal'][data-bs-target='#smartModal']"))
            )
            print("✅ Botão encontrado:", button.text)
            
            # Clicar no botão
            print("🖱️ Clicando no botão...")
            button.click()
            
            # Aguardar modal abrir
            time.sleep(2)
            
            # Verificar se modal está visível
            print("🔍 Verificando se modal está visível...")
            modal = driver.find_element(By.ID, "smartModal")
            if modal.is_displayed():
                print("✅ Modal está visível")
            else:
                print("❌ Modal não está visível")
                return False
            
            # Verificar steps
            print("🔍 Verificando steps...")
            steps = driver.find_elements(By.CSS_SELECTOR, ".step-content")
            print(f"Steps encontrados: {len(steps)}")
            
            for i, step in enumerate(steps):
                step_id = step.get_attribute('id')
                is_visible = step.is_displayed()
                classes = step.get_attribute('class')
                print(f"  Step {i+1}: {step_id} - Visível: {is_visible} - Classes: {classes}")
            
            # Verificar Step 2 especificamente
            print("🔍 Verificando Step 2...")
            step2 = driver.find_element(By.ID, "step2")
            print(f"Step 2 - Visível: {step2.is_displayed()}")
            print(f"Step 2 - Classes: {step2.get_attribute('class')}")
            
            # Verificar se há campos no Step 2
            campos_step2 = step2.find_elements(By.CSS_SELECTOR, "input, select, textarea")
            print(f"Campos no Step 2: {len(campos_step2)}")
            
            for campo in campos_step2:
                campo_id = campo.get_attribute('id')
                campo_type = campo.get_attribute('type') or campo.tag_name
                print(f"  Campo: {campo_id} ({campo_type})")
            
            # Preencher Step 1
            print("📝 Preenchendo Step 1...")
            driver.find_element(By.ID, "name").send_keys("João Silva Teste")
            driver.find_element(By.ID, "email").send_keys("joao.teste@empresa.com")
            driver.find_element(By.ID, "phone").send_keys("(11) 99999-9999")
            
            # Clicar em Próximo
            print("➡️ Clicando em Próximo...")
            next_btn = driver.find_element(By.ID, "nextBtn")
            next_btn.click()
            
            # Aguardar transição
            time.sleep(3)
            
            # Verificar Step 2 após transição
            print("🔍 Verificando Step 2 após transição...")
            step2_after = driver.find_element(By.ID, "step2")
            print(f"Step 2 após transição - Visível: {step2_after.is_displayed()}")
            print(f"Step 2 após transição - Classes: {step2_after.get_attribute('class')}")
            
            # Verificar indicadores
            print("🔍 Verificando indicadores...")
            indicators = driver.find_elements(By.CSS_SELECTOR, ".step-indicator")
            for i, indicator in enumerate(indicators):
                is_active = "active" in indicator.get_attribute('class')
                print(f"  Indicador {i+1}: Ativo: {is_active}")
            
            # Verificar console logs
            print("🔍 Verificando console logs...")
            logs = driver.get_log('browser')
            for log in logs[-10:]:  # Últimos 10 logs
                print(f"  Console: {log['message']}")
            
        except Exception as e:
            print(f"❌ Erro durante o teste: {e}")
            return False
        
        finally:
            driver.quit()
        
        print("✅ Teste concluído!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar driver: {e}")
        return False

if __name__ == "__main__":
    success = test_modal_debug()
    if success:
        print("🎉 Teste de debug concluído!")
    else:
        print("💥 Teste de debug falhou!")

