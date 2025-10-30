from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

def aguardar_elemento(driver, by, value, timeout=10, descricao="elemento"):
    """Aguarda um elemento ficar disponível"""
    try:
        print(f"⏳ Aguardando {descricao}...")
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        print(f"✓ {descricao} encontrado!")
        return elemento
    except TimeoutException:
        print(f"❌ Timeout: {descricao} não encontrado em {timeout}s")
        return None