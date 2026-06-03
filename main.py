import pyautogui
import time
import os
from dotenv import load_dotenv
from modules.clicar_imagem import clicar_imagem
from modules.centro_de_custo import automacao_centro_de_custo
from modules.calcular_competencia import calcular_competencia
from modules.consumo import automacao_consumo
from modules.conectar_vpn import conectar_vpn
from modules.abrir_app_agent import habilitar_app_agent
from modules.logger_excel import LogExecucao
from modules.enviar_email import enviar_email_resultado
from config.list_filial import LISTA_FILIAIS

if __name__ == "__main__":

    # Carregar variáveis de ambiente
    load_dotenv()

    # Diretório raiz do projeto (onde está o main.py)
    RAIZ_PROJETO = os.path.dirname(os.path.abspath(__file__))

    # Calcula a competencia
    competencia_anterior = calcular_competencia()

    # conectar_vpn() # não será mais necessário conectar VPN, pois o script será executado em um servidor que já tem acesso ao sistema

    # Carregar variáveis de ambiente obrigatórias
    try:
        NOME_APP = os.getenv("NOME_APP")
        USER     = os.getenv("USER")
        SENHA    = os.getenv("SENHA")

        if not NOME_APP or not USER or not SENHA:
            print("Erro: Variáveis de ambiente não configuradas!")
            print(f"NOME_APP: {NOME_APP}")
            print(f"USER: {USER}")
            print(f"SENHA: {'***' if SENHA else None}")
            exit(1)

        print("Variáveis carregadas com sucesso!")

    except Exception as e:
        print("Erro ao carregar variáveis de ambiente:", e)
        exit(1)

    # ── Login no sistema ──────────────────────────────────────────────────────

    pyautogui.press('win')
    pyautogui.write(NOME_APP, interval=0.1)
    pyautogui.press('enter')
    time.sleep(10)

    pyautogui.press('f11')
    pyautogui.press('enter')
    time.sleep(8)

    habilitar_app_agent()
    time.sleep(15)

    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.press('backspace')

    pyautogui.typewrite(USER.upper(), interval=0.2)
    pyautogui.press('tab')
    pyautogui.write(SENHA, interval=0.1)
    pyautogui.press('enter')

    time.sleep(5)
    pyautogui.click(x=100, y=200)
    time.sleep(5)
    pyautogui.press('end')
    time.sleep(2)

    if not clicar_imagem("data/botao_entrar.png", confidence=0.8, timeout=15, descricao="Botão entrar"):
        print("Erro ao clicar no botão entrar.")
        exit(1)

    time.sleep(3)

    # ── Automação de CONSUMO ──────────────────────────────────────────────────

    log_consumo = LogExecucao(raiz_projeto=RAIZ_PROJETO)
    log_consumo.iniciar_execucao(
        tipo="Consumo",
        competencia=competencia_anterior,
        filiais=LISTA_FILIAIS,
    )

    automacao_consumo(competencia_anterior, log=log_consumo)

    resumo_consumo = log_consumo.finalizar_execucao()
    enviar_email_resultado(resumo_consumo)

    # # ── Automação de CENTRO DE CUSTO ─────────────────────────────────────────

    log_cc = LogExecucao(raiz_projeto=RAIZ_PROJETO)
    log_cc.iniciar_execucao(
        tipo="Centro de Custo",
        competencia=competencia_anterior,
        filiais=LISTA_FILIAIS,
    )

    automacao_centro_de_custo(competencia_anterior, log=log_cc)

    resumo_cc = log_cc.finalizar_execucao()
    enviar_email_resultado(resumo_cc)

    # ── Encerramento ──────────────────────────────────────────────────────────

    print("Automação concluída com sucesso!")

    pyautogui.keyDown('ctrl')
    pyautogui.press('q')
    pyautogui.keyUp('ctrl')
    time.sleep(1)

    if not clicar_imagem("data/botao_finalizar.png", confidence=0.8, timeout=15, descricao="Botão Finalizar"):
        print("Erro ao clicar no botão finalizar.")

    pyautogui.press('f11')

    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('alt')

    exit(0)