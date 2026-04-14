from modules.clicar_imagem import clicar_imagem
import time
from config.list_filial import LISTA_FILIAIS
import pyautogui
from datetime import datetime
from modules.mover_e_renomear_arquivo_baixado import mover_e_renomear_csv
from modules.aguardar_download_inteligente import aguardar_download_completo, fechar_excel
import os


def automacao_consumo(competencia, log=None):
    """
    Automação de consumo.

    Args:
        competencia: data no formato "DD/MM/YYYY"
        log: instância de LogExecucao (opcional). Se informado, registra cada filial.
    """
    # escolhe a opção do relatório de consumo
    if not clicar_imagem("data/menu_consultas.png", confidence=0.8, timeout=15, descricao="Menu Consumo"):
        print("Erro ao acessar o menu consultas.")
        return

    time.sleep(2)

    for filial in LISTA_FILIAIS:
        inicio_filial = datetime.now()

        print(f"\n{'='*60}")
        print(f"🏢 Processando filial: {filial}")
        print(f"{'='*60}\n")

        time.sleep(5)
        # clica na opção consumo mes a mes
        if not clicar_imagem("data/opcao_genericos.png", confidence=0.8, timeout=15, descricao="Opção genericos"):
            msg = "Erro ao escolher a opção genericos"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(3)

        # selecionar todo o campo focado
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')

        # limpar todo o campo selecionado
        pyautogui.press('backspace')
        time.sleep(2)

        # digitar a competencia do mês anterior
        pyautogui.write(competencia, interval=0.1)
        time.sleep(2)

        # clicar duas vezes o tab
        pyautogui.press('tab', presses=1, interval=0.5)

        # seleciona todo o campo
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')

        # apaga o conteúdo do campo
        pyautogui.press('backspace')

        # digita a filial
        pyautogui.write(filial, interval=0.1)

        # clica no botão "Confirmar"
        time.sleep(5)

        if not clicar_imagem("data/botao_confirmar.png", confidence=0.8, timeout=15, descricao="Botão Confirmar"):
            msg = "Erro ao clicar no botão Confirmar"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(5)

        # clicar no botão reforma tributaria
        if not clicar_imagem("data/botao_reforma_tributaria.png", confidence=0.8, timeout=15, descricao="Botão Reforma Tributária"):
            print("Erro ao clicar no botão Reforma Tributária.")

        time.sleep(10)

        if not clicar_imagem("data/caixa_pesquisa.png", confidence=0.8, timeout=15, descricao="Caixa de pesquisa"):
            msg = "Erro ao clicar na caixa de texto"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(5)

        # selecionar todo o campo focado
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')

        # limpar todo o campo selecionado
        pyautogui.press('backspace')

        # digitar "SD3"
        pyautogui.write("SD3", interval=0.1)
        time.sleep(2)

        # pressionar tab
        pyautogui.press('tab', presses=2, interval=0.5)

        # pressionar enter
        pyautogui.press('enter')

        print("Iniciando a configuração de filtro...")
        time.sleep(6)

        # adicionar dicionario
        if not clicar_imagem("data/dicionario.png", confidence=0.8, timeout=15, descricao="Botão Dicionario"):
            msg = "Erro ao clicar na opção dicionário"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(4)

        # marcar a caixa de seleção dicionário
        if not clicar_imagem("data/marcar_caixa_dicionario.png", confidence=0.8, timeout=15, descricao="Caixa dicionário"):
            msg = "Erro ao flegar a caixa de seleção dicionário"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(3)

        # marcar em ok
        if not clicar_imagem("data/ok_dicionario.png", confidence=0.8, timeout=15, descricao="Opção 'ok' dicionário"):
            msg = "Erro ao clicar 'ok' dicionário"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(4)

        # clica na opção filtro
        if not clicar_imagem("data/filtrar_consumo.png", confidence=0.8, timeout=15, descricao="Botão Filtrar"):
            msg = "Erro ao clicar no filtro"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(3)

        # clica na opção criar filtro
        if not clicar_imagem("data/criar_filtro.png", confidence=0.8, timeout=15, descricao="Botão Criar Filtro"):
            msg = "Erro ao clicar no Criar Filtro"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(3)

        # clicar tres vezes tab e digitar o nome do filtro
        pyautogui.press('tab', presses=3, interval=0.5)
        pyautogui.write('Competecia', interval=0.1)

        # alterar os dois primeiros digitos da data por 01
        competencia_inicial = "01" + competencia[2:]
        print(f"Competência inicial: {competencia_inicial}")
        print(f"Competência final: {competencia}")

        # selecionar o botao de data
        if not clicar_imagem("data/botao_data.png", confidence=0.8, timeout=15, descricao="Botão Data"):
            msg = "Erro ao clicar na opção data"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        pyautogui.write("D", interval=0.1)
        pyautogui.press('down')
        pyautogui.press('enter')
        time.sleep(2)

        # seleciona o campo de operador
        if not clicar_imagem("data/operador_igual_a.png", confidence=0.8, timeout=15, descricao="Operador igual a"):
            msg = "Erro ao clicar na opção operador igual a"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        pyautogui.write("M", interval=0.1)
        pyautogui.press('down', presses=3, interval=0.5)
        pyautogui.press('enter')

        # busca o campo para digitar a competencia inicial
        if not clicar_imagem("data/campo_valor_filtro.png", confidence=0.8, timeout=15, descricao="Campo valor filtro"):
            msg = "Erro ao clicar na opção campo valor filtro"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        pyautogui.write(competencia_inicial, interval=0.1)

        # clica no botão adicionar filtro
        if not clicar_imagem("data/botao_add_filtro.png", confidence=0.8, timeout=15, descricao="Botão Adicionar filtro"):
            msg = "Erro ao clicar na opção para adicionar filtro"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        pyautogui.press('tab', presses=5, interval=0.5)
        pyautogui.press('enter')

        time.sleep(2)

        # clicar na opção maior ou igual a para trocar o operador
        if not clicar_imagem("data/operador_maior_igual_a.png", confidence=0.8, timeout=15, descricao="Operador maior igual a"):
            msg = "Erro ao clicar na opção operador maior igual a"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        pyautogui.press('up', presses=2, interval=0.5)
        pyautogui.press('enter')

        # busca o campo para digitar a competencia final
        if not clicar_imagem("data/campo_valor_filtro.png", confidence=0.8, timeout=15, descricao="Campo valor filtro"):
            msg = "Erro ao clicar na opção campo valor filtro"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        pyautogui.write(competencia, interval=0.1)
        time.sleep(2)

        if not clicar_imagem("data/botao_add_filtro.png", confidence=0.8, timeout=15, descricao="Botão Adicionar filtro"):
            msg = "Erro ao clicar na opção para adicionar filtro (competência final)"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        if not clicar_imagem("data/botao_salvar_filtro.png", confidence=0.8, timeout=15, descricao="Botão salvar filtro"):
            msg = "Erro ao clicar na opção salvar filtro"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        if not clicar_imagem("data/selecionar_filtro_selecionado.png", confidence=0.8, timeout=15, descricao="Caixa de seleção do filtro criado"):
            msg = "Erro ao selecionar a caixa do filtro criado"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        if not clicar_imagem("data/aplicar_filtro_selecionado.png", confidence=0.8, timeout=15, descricao="Aplicar filtro selecionado"):
            msg = "Erro ao aplicar o filtro selecionado"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        if not clicar_imagem("data/export_csv.png", confidence=0.8, timeout=15, descricao="Selecionar o tipo de opção export"):
            msg = "Erro ao selecionar o tipo de exportação"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        if not clicar_imagem("data/ponto_e_virgula.png", confidence=0.8, timeout=15, descricao="Selecionar o tipo ponto e virgula"):
            msg = "Erro ao selecionar o tipo ponto e virgula"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        if not clicar_imagem("data/confirmar_export.png", confidence=0.8, timeout=15, descricao="Confirmar exportação"):
            msg = "Erro ao confirmar exportação"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        diretorio_temp = os.getenv("DIRETORIO_TEMP")

        sucesso_dl, arquivo_baixado, tempo_gasto = aguardar_download_completo(
            diretorio_temp=diretorio_temp,
            timeout=900,
            intervalo_verificacao=2
        )

        if not sucesso_dl:
            msg = f"Download não concluído para a filial {filial}"
            print(f"❌ Erro: {msg}")
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            continue

        print(f"⚡ Economia de tempo: {900 - tempo_gasto:.1f} segundos!")

        fechar_excel()
        time.sleep(4)

        # Define o diretório de destino
        data = datetime.strptime(competencia, "%d/%m/%Y")
        ano  = data.year
        mes  = data.month
        caminho_fixo = os.getenv("CAMINHO_FIXO_CONSUMO")
        diretorio_destino = f"{caminho_fixo}\\{ano}\\{mes}_{ano}"
        print(f"📂 Caminho: {diretorio_destino}")

        print("Processando arquivo baixado...")
        if mover_e_renomear_csv(filial, competencia, diretorio_destino):
            print(f"✅ Filial {filial} processada com sucesso!")
            if log:
                log.registrar_filial(filial, sucesso=True,
                                     mensagem="Arquivo exportado e movido com sucesso",
                                     inicio_filial=inicio_filial)
        else:
            msg = "Erro ao mover/renomear o arquivo CSV"
            print(f"❌ {msg} da filial {filial}")
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)

        time.sleep(5)

        # sair do consumo
        if not clicar_imagem("data/sair_consumo.png", confidence=0.8, timeout=15, descricao="Saindo do consumo"):
            print("Erro ao sair do consumo")
            return

    print("\n" + "="*60)
    print("✅ Automação de consumo concluída para todas as filiais!")
    print("="*60)