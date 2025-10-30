from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
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