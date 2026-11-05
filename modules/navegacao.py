import os
import time
from modules.clicar_imagem import clicar_imagem
from modules.localizar_imagem import localizar_imagem
from modules.etapa import fechar_aba_atual

# Tela inicial do Protheus (com o logo), mostrada quando nenhuma rotina está aberta.
# Enquanto o recorte não existir em data/, essa conferência é pulada.
IMAGEM_TELA_INICIAL = "data/tela_inicial_logo.png"


def preparar_tela_inicial(max_abas=3):
    """
    Deixa o Protheus na tela inicial antes de começar um relatório: fecha as
    abas de rotina que tenham ficado abertas (ex.: "Genéricos - 01/...") e,
    se o recorte do logo existir, confere se a tela inicial apareceu.

    Returns:
        True se está na tela inicial (ou se não há recorte do logo para conferir).
    """
    for _ in range(max_abas):
        if not fechar_aba_atual():
            break
        print("🗂️  Aba de rotina fechada.")

    if not os.path.exists(IMAGEM_TELA_INICIAL):
        return True

    return bool(localizar_imagem(IMAGEM_TELA_INICIAL, confidence=0.8, timeout=15,
                                 descricao="Tela inicial (logo)"))


def abrir_menu(caminho, destino, confidence_destino=0.8):
    """
    Abre o menu até o item `destino` ficar visível, clicando SÓ nos níveis que
    ainda estão fechados. Assim um menu que já está aberto (ex.: "Consultas",
    deixado aberto pelo relatório anterior) não é clicado de novo, o que o fecharia.

    Args:
        caminho: imagens dos níveis do menu, do mais externo ao mais interno
                 (ex.: ["data/menu_consultas.png", "data/opcao_smart_view.png"])
        destino: imagem do item que precisa ficar visível
                 (ex.: "data/opcao_centro_de_custo.png")

    Returns:
        True se o destino ficou visível, False caso contrário.
    """
    def visivel(imagem, confidence=0.8, timeout=3):
        return localizar_imagem(imagem, confidence=confidence, timeout=timeout,
                                descricao=os.path.basename(imagem))

    if visivel(destino, confidence_destino):
        return True

    # começa pelo nível mais interno que já está visível (é o que está fechado)
    inicio = None
    for i in range(len(caminho) - 1, -1, -1):
        if visivel(caminho[i]):
            inicio = i
            break

    if inicio is None:
        print("⚠️  Nenhum item do menu encontrado na tela.")
        return False

    for imagem in caminho[inicio:]:
        if not clicar_imagem(imagem, confidence=0.8, timeout=30,
                             descricao=os.path.basename(imagem)):
            return False
        time.sleep(2)

    return bool(visivel(destino, confidence_destino, timeout=15))
