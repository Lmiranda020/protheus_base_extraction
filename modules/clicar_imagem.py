import os
import pyautogui
import time
from datetime import datetime

PASTA_PRINTS = os.path.join("log", "prints")


def salvar_print_erro(descricao=""):
    """Salva um print da tela atual em log/prints, para ver o que estava na tela no momento do erro."""
    try:
        os.makedirs(PASTA_PRINTS, exist_ok=True)
        sufixo = "".join(c if c.isalnum() else "_" for c in descricao)[:40]
        nome = f"erro_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{sufixo}.png"
        caminho = os.path.join(PASTA_PRINTS, nome)
        pyautogui.screenshot(caminho)
        print(f"📸 Print da tela salvo em: {caminho}")
    except Exception as e:
        print(f"Não foi possível salvar o print da tela: {e}")


def clicar_imagem(caminho_imagem, confidence=0.8, timeout=10, descricao="", salvar_print=True):
    """
    Procura uma imagem na tela e clica nela

    Args:
        caminho_imagem: caminho para a imagem do botão
        confidence: precisão da busca (0.0 a 1.0)
        timeout: tempo máximo de espera em segundos
        descricao: descrição do botão para logs
        salvar_print: se True, salva um print da tela quando não encontrar a imagem

    Returns:
        True se encontrou e clicou, False caso contrário
    """
    print(f"Procurando por: {descricao if descricao else caminho_imagem}")

    tempo_inicial = time.time()

    while time.time() - tempo_inicial < timeout:
        try:
            # Procurar a imagem na tela
            localizacao = pyautogui.locateOnScreen(caminho_imagem, confidence=confidence)

            if localizacao:
                # Pegar o centro da imagem
                centro = pyautogui.center(localizacao)

                # Clicar no centro
                pyautogui.click(centro)
                print(f"✓ Clicou em: {descricao if descricao else caminho_imagem}")
                return True

        except pyautogui.ImageNotFoundException:
            pass
        except Exception as e:
            print(f"Erro ao procurar imagem: {e}")

        time.sleep(0.5)  # Aguardar meio segundo antes de tentar novamente

    print(f"✗ Não encontrou: {descricao if descricao else caminho_imagem}")
    if salvar_print:
        salvar_print_erro(descricao or os.path.basename(caminho_imagem))
    return False
