import selenium
import time
from modules.clicar_imagem import clicar_imagem

def habilitar_app_agent():

    if not clicar_imagem("data/botao_confirmar_agent.png", confidence=0.8, timeout=15, descricao="Botão app web agent"):
        print("Erro ao clicar no botão WebAgent.")
        time.sleep(8)    