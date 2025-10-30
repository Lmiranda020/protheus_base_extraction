from modules.aguardar_elemento import aguardar_elemento
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def aguardar_clicavel(driver, by, value, timeout=10, descricao="elemento"):
    """Aguarda um elemento ficar clicável"""
    try:
        print(f"⏳ Aguardando {descricao} ficar clicável...")
        elemento = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        print(f"✓ {descricao} clicável!")
        return elemento
    except TimeoutException:
        print(f"❌ Timeout: {descricao} não ficou clicável em {timeout}s")
        return None

def scroll_para_elemento(driver, elemento):
    """Rola a página até o elemento"""
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", elemento)
    time.sleep(0.5)

def clicar_botao_por_texto(driver, texto, timeout=10):
    """Tenta encontrar e clicar em um botão pelo texto (para botões normais, não shadow)"""
    try:
        botao = aguardar_clicavel(driver, By.XPATH, f"//button[contains(text(), '{texto}')]", timeout, f"botão '{texto}'")
        if botao:
            scroll_para_elemento(driver, botao)
            botao.click()
            return True
        return False
    except Exception as e:
        print(f"⚠️ Erro ao clicar em '{texto}': {e}")
        return False

def fazer_login_selenium(driver, email, senha, url_login=None, navegar=False, modo_simples=True):
    """
    Realiza login no sistema
    
    Args:
        driver: Instância do WebDriver
        email: Email para login
        senha: Senha para login
        url_login: URL da página de login (opcional)
        navegar: Se True, navega para a URL antes de fazer login (padrão: False)
        modo_simples: Se True, usa digitação direta (campo já focado) + TAB + ENTER
                     Se False, busca os campos manualmente
    """
    print("🔐 Fazendo login...")
    
    try:
        # Só navega se explicitamente solicitado
        if navegar and url_login:
            print(f"📍 Navegando para: {url_login}")
            driver.get(url_login)
            time.sleep(2)
        else:
            print("📍 Usando página atual (sem navegação)")
            time.sleep(1)
        
        if modo_simples:
            # ========== MODO SIMPLES: CAMPO JÁ FOCADO ==========
            print("⌨️ Modo simples: digitação direta (campo já focado)")
            
            # Obter o elemento ativo (que já está focado)
            elemento_ativo = driver.switch_to.active_element
            
            # 1. Digitar email no campo já focado
            print(f"📧 Digitando email...")
            elemento_ativo.send_keys(email)
            time.sleep(0.5)
            
            # 2. Pressionar TAB para ir para o campo de senha
            print("⇥ Pressionando TAB...")
            elemento_ativo.send_keys(Keys.TAB)
            time.sleep(0.5)
            
            # 3. Digitar senha
            print("🔑 Digitando senha...")
            elemento_ativo = driver.switch_to.active_element
            elemento_ativo.send_keys(senha)
            time.sleep(0.5)
            
            # 4. Pressionar ENTER para fazer login
            print("↵ Pressionando ENTER...")
            elemento_ativo.send_keys(Keys.RETURN)
            time.sleep(3)
            
        else:
            # ========== MODO TRADICIONAL: BUSCAR CAMPOS ==========
            print("🔍 Modo tradicional: buscando campos manualmente")
            
            # Aguardar e preencher email
            campo_email = aguardar_elemento(driver, By.CSS_SELECTOR, 
                "input[type='email'], input[name='email'], input#email", 
                descricao="campo de email")
            if campo_email:
                campo_email.clear()
                campo_email.send_keys(email)
            
            # Aguardar e preencher senha
            campo_senha = aguardar_elemento(driver, By.CSS_SELECTOR, 
                "input[type='password'], input[name='password'], input#password", 
                descricao="campo de senha")
            if campo_senha:
                campo_senha.clear()
                campo_senha.send_keys(senha)
            
            # Tentar clicar no botão de login
            if not clicar_botao_por_texto(driver, "Entrar", timeout=5):
                if not clicar_botao_por_texto(driver, "Login", timeout=5):
                    # Fallback: pressionar Enter
                    campo_senha.send_keys(Keys.RETURN)
            
            time.sleep(3)
        
        print("✓ Login realizado!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        import traceback
        traceback.print_exc()
        return False