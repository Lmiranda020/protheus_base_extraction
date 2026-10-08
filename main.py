import pyautogui
import time
import os
from dotenv import load_dotenv
from modules.clicar_imagem import clicar_imagem, salvar_print_erro
from modules.centro_de_custo import automacao_centro_de_custo
from modules.calcular_competencia import calcular_competencia
from modules.consumo import automacao_consumo
from modules.conectar_vpn import conectar_vpn
from modules.abrir_app_agent import habilitar_app_agent
from modules.logger_excel import LogExecucao, filiais_com_sucesso
from modules.enviar_email import enviar_email_resultado
from config.list_filial import LISTA_FILIAIS


def filiais_pendentes(tipo, competencia, raiz_projeto):
    """Filiais de LISTA_FILIAIS que ainda não têm sucesso no log para esse tipo e competência."""
    ja_processadas = filiais_com_sucesso(raiz_projeto, tipo, competencia)
    pendentes = [f for f in LISTA_FILIAIS if f not in ja_processadas]

    print(f"📊 {tipo} ({competencia}): {len(LISTA_FILIAIS) - len(pendentes)} já processada(s), "
          f"{len(pendentes)} pendente(s)")
    if pendentes:
        print(f"   Pendentes: {', '.join(pendentes)}")
    return pendentes


def executar_relatorio(tipo, automacao, competencia, filiais, raiz_projeto):
    """Roda a automação do relatório só para as filiais informadas, grava o log e envia o e-mail."""
    if not filiais:
        print(f"✅ {tipo}: todas as filiais da competência {competencia} já foram processadas. Pulando.")
        return

    log = LogExecucao(raiz_projeto=raiz_projeto)
    log.iniciar_execucao(
        tipo=tipo,
        competencia=competencia,
        filiais=filiais,
    )

    automacao(competencia, log=log, filiais=filiais)

    resumo = log.finalizar_execucao()
    enviar_email_resultado(resumo)


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

    # ── Filiais pendentes ─────────────────────────────────────────────────────
    # Consulta o log para não processar de novo as filiais que já deram certo
    # nessa competência (útil quando a automação é rodada mais de uma vez no mês)

    pendentes_consumo = filiais_pendentes("Consumo", competencia_anterior, RAIZ_PROJETO)
    pendentes_cc      = filiais_pendentes("Centro de Custo", competencia_anterior, RAIZ_PROJETO)

    if not pendentes_consumo and not pendentes_cc:
        print("✅ Nada pendente para essa competência. Encerrando sem abrir o sistema.")
        exit(0)

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

    # clicar no campo para digitar o usuário, através da imagem do campo de usuário
    if not clicar_imagem("data/campo_usuario.png", confidence=0.8, timeout=15, descricao="Campo usuário"):
        print("Erro ao clicar no campo de usuário.")
        exit(1)


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

    executar_relatorio("Consumo", automacao_consumo, competencia_anterior,
                       pendentes_consumo, RAIZ_PROJETO)

    # ── Automação de CENTRO DE CUSTO ─────────────────────────────────────────

    executar_relatorio("Centro de Custo", automacao_centro_de_custo, competencia_anterior,
                       pendentes_cc, RAIZ_PROJETO)

    # ── Encerramento ──────────────────────────────────────────────────────────

    print("Automação concluída com sucesso!")

    finalizou = False
    for _ in range(3):
        pyautogui.keyDown('ctrl')
        pyautogui.press('q')
        pyautogui.keyUp('ctrl')
        time.sleep(2)

        # se alguma consulta ficou aberta, o Protheus pergunta se pode
        # interromper o processo da sessão atual: confirma com "Sim".
        # confidence 0.9 para não confundir com o botão "Arquivo", que é parecido
        if clicar_imagem("data/botao_sim_fechar_sessao.png", confidence=0.9, timeout=5,
                         descricao="Sim (fechar sessão)", salvar_print=False):
            time.sleep(3)

        if clicar_imagem("data/botao_finalizar.png", confidence=0.8, timeout=15,
                         descricao="Botão Finalizar", salvar_print=False):
            finalizou = True
            break

    if not finalizou:
        print("Erro ao clicar no botão finalizar.")
        salvar_print_erro("Botão Finalizar")

    pyautogui.press('f11')

    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('alt')

    exit(0)