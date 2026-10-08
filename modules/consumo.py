from modules.clicar_imagem import clicar_imagem
from modules.localizar_imagem import localizar_imagem
from modules.etapa import (EtapaFalhou, etapa, aguardar_imagem_sumir, processar_filiais,
                           registrar_filiais_com_erro)
import time
from config.list_filial import LISTA_FILIAIS
import pyautogui
from datetime import datetime
from modules.mover_e_renomear_arquivo_baixado import mover_e_renomear_csv
from modules.aguardar_download_inteligente import aguardar_download_completo, fechar_excel
import os


def voltar_tela_inicial_consumo(tentativas=6):
    """
    Fecha o que estiver aberto até a opção "genéricos" aparecer na tela
    (ponto de partida de cada filial).

    Returns:
        True se a tela inicial está visível, False caso contrário.
    """
    for _ in range(tentativas):
        if localizar_imagem("data/opcao_genericos.png", confidence=0.8, timeout=5,
                            descricao="Tela inicial (opção genéricos)"):
            return True

        # primeiro fecha janelas que estejam na frente (ex.: Gerenciador de Filtros).
        # Enquanto uma delas estiver aberta, o botão "Sair" aparece atrás dela,
        # mas o clique nele não funciona.
        if clicar_imagem("data/botao_cancelar.png", confidence=0.8, timeout=2,
                         descricao="Botão Cancelar", salvar_print=False):
            time.sleep(2)
            continue

        # se ainda estiver dentro da consulta, sai pelo botão do próprio sistema
        if clicar_imagem("data/sair_consumo.png", confidence=0.8, timeout=3,
                         descricao="Saindo do consumo", salvar_print=False):
            time.sleep(3)
            if localizar_imagem("data/opcao_genericos.png", confidence=0.8, timeout=5,
                                descricao="Tela inicial (opção genéricos)"):
                return True

        # se o "Sair" não resolveu, alguma outra janela está na frente: tenta o Esc
        pyautogui.press('esc')
        time.sleep(3)

    # última tentativa: o menu consultas pode ter sido recolhido
    if clicar_imagem("data/menu_consultas.png", confidence=0.8, timeout=5,
                     descricao="Menu Consultas", salvar_print=False):
        time.sleep(2)
        if localizar_imagem("data/opcao_genericos.png", confidence=0.8, timeout=10,
                            descricao="Tela inicial (opção genéricos)"):
            return True

    return False


def processar_filial_consumo(filial, competencia):
    """
    Exporta o relatório de consumo de UMA filial.

    Returns:
        Mensagem de sucesso para o log.

    Raises:
        EtapaFalhou: se alguma etapa não puder ser concluída.
    """
    time.sleep(5)
    # clica na opção consumo mes a mes
    etapa("data/opcao_genericos.png", "Opção genericos",
          "Erro ao escolher a opção genericos")

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

    etapa("data/botao_confirmar.png", "Botão Confirmar",
          "Erro ao clicar no botão Confirmar")

    time.sleep(5)

    # clicar no botão reforma tributaria (nem sempre aparece, então não é erro)
    if not clicar_imagem("data/botao_reforma_tributaria.png", confidence=0.8, timeout=15,
                         descricao="Botão Reforma Tributária", salvar_print=False):
        print("Botão Reforma Tributária não apareceu, seguindo.")

    time.sleep(10)

    etapa("data/caixa_pesquisa.png", "Caixa de pesquisa",
          "Erro ao clicar na caixa de texto")

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
    etapa("data/dicionario.png", "Botão Dicionario",
          "Erro ao clicar na opção dicionário")

    time.sleep(4)

    # marcar a caixa de seleção dicionário
    etapa("data/marcar_caixa_dicionario.png", "Caixa dicionário",
          "Erro ao flegar a caixa de seleção dicionário")

    time.sleep(3)

    # marcar em ok
    etapa("data/ok_dicionario.png", "Opção 'ok' dicionário",
          "Erro ao clicar 'ok' dicionário")

    time.sleep(4)

    # clica na opção filtro
    etapa("data/filtrar_consumo.png", "Botão Filtrar",
          "Erro ao clicar no filtro")

    time.sleep(3)

    # clica na opção criar filtro
    etapa("data/criar_filtro.png", "Botão Criar Filtro",
          "Erro ao clicar no Criar Filtro")

    time.sleep(3)

    # clicar tres vezes tab e digitar o nome do filtro
    pyautogui.press('tab', presses=3, interval=0.5)
    pyautogui.write('Competecia', interval=0.1)

    # alterar os dois primeiros digitos da data por 01
    competencia_inicial = "01" + competencia[2:]
    print(f"Competência inicial: {competencia_inicial}")
    print(f"Competência final: {competencia}")

    # selecionar o botao de data
    etapa("data/botao_data.png", "Botão Data",
          "Erro ao clicar na opção data")

    pyautogui.write("D", interval=0.1)
    pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(2)

    # seleciona o campo de operador
    etapa("data/operador_igual_a.png", "Operador igual a",
          "Erro ao clicar na opção operador igual a")

    pyautogui.write("M", interval=0.1)
    pyautogui.press('down', presses=3, interval=0.5)
    pyautogui.press('enter')

    # busca o campo para digitar a competencia inicial
    etapa("data/campo_valor_filtro.png", "Campo valor filtro",
          "Erro ao clicar na opção campo valor filtro")

    time.sleep(0.5)
    pyautogui.write(competencia_inicial, interval=0.2)

    # clica no botão adicionar filtro
    etapa("data/botao_add_filtro.png", "Botão Adicionar filtro",
          "Erro ao clicar na opção para adicionar filtro")

    time.sleep(2)

    pyautogui.press('tab', presses=5, interval=0.5)
    pyautogui.press('enter')

    time.sleep(2)

    # clicar na opção maior ou igual a para trocar o operador
    etapa("data/operador_maior_igual_a.png", "Operador maior igual a",
          "Erro ao clicar na opção operador maior igual a")

    pyautogui.press('up', presses=2, interval=0.5)
    pyautogui.press('enter')

    # busca o campo para digitar a competencia final
    etapa("data/campo_valor_filtro.png", "Campo valor filtro",
          "Erro ao clicar na opção campo valor filtro")

    pyautogui.write(competencia, interval=0.2)
    time.sleep(2)

    etapa("data/botao_add_filtro.png", "Botão Adicionar filtro",
          "Erro ao clicar na opção para adicionar filtro (competência final)")

    time.sleep(2)

    etapa("data/botao_salvar_filtro.png", "Botão salvar filtro",
          "Erro ao clicar na opção salvar filtro")

    time.sleep(2)

    etapa("data/selecionar_filtro_selecionado.png", "Caixa de seleção do filtro criado",
          "Erro ao selecionar a caixa do filtro criado")

    time.sleep(2)

    etapa("data/aplicar_filtro_selecionado.png", "Aplicar filtro selecionado",
          "Erro ao aplicar o filtro selecionado")

    # Às vezes o clique em "Aplicar" não é registrado e o Gerenciador de Filtros
    # continua aberto. Aí o "Exp. CSV" é clicado atrás da janela e nada acontece.
    # Por isso confere se a janela fechou e, se não fechou, clica de novo.
    if not aguardar_imagem_sumir("data/aplicar_filtro_selecionado.png", timeout=15):
        print("⚠️  Gerenciador de Filtros ainda aberto, clicando em aplicar novamente...")
        clicar_imagem("data/aplicar_filtro_selecionado.png", confidence=0.8, timeout=5,
                      descricao="Aplicar filtro selecionado", salvar_print=False)
        if not aguardar_imagem_sumir("data/aplicar_filtro_selecionado.png", timeout=30):
            raise EtapaFalhou("O Gerenciador de Filtros não fechou após aplicar o filtro")

    time.sleep(2)

    etapa("data/export_csv.png", "Selecionar o tipo de opção export",
          "Erro ao selecionar o tipo de exportação")

    time.sleep(2)

    etapa("data/ponto_e_virgula.png", "Selecionar o tipo ponto e virgula",
          "Erro ao selecionar o tipo ponto e virgula")

    time.sleep(2)

    etapa("data/confirmar_export.png", "Confirmar exportação",
          "Erro ao confirmar exportação")

    diretorio_temp = os.getenv("DIRETORIO_TEMP")

    sucesso_dl, arquivo_baixado, tempo_gasto = aguardar_download_completo(
        diretorio_temp=diretorio_temp,
        timeout=900,
        intervalo_verificacao=2
    )

    if not sucesso_dl:
        fechar_excel()
        raise EtapaFalhou(f"Download não concluído para a filial {filial}")

    print(f"⚡ Economia de tempo: {900 - tempo_gasto:.1f} segundos!")

    fechar_excel()
    time.sleep(4)

    # Define o diretório de destino
    data = datetime.strptime(competencia, "%d/%m/%Y")
    ano  = data.year
    mes  = str(data.month).zfill(2)  # inserir zero à esquerda do mês, se necessário
    caminho_fixo = os.getenv("CAMINHO_FIXO_CONSUMO")

    diretorio_destino = f"{caminho_fixo}\\{ano}\\{mes}_{ano}"
    print(f"📂 Caminho: {diretorio_destino}")

    print("Processando arquivo baixado...")
    if not mover_e_renomear_csv(filial, competencia, diretorio_destino,
                                arquivo_origem=arquivo_baixado):
        raise EtapaFalhou("Erro ao mover/renomear o arquivo CSV")

    time.sleep(5)

    # sair do consumo. O arquivo já foi salvo, então uma falha aqui não refaz
    # a filial: a próxima filial volta para a tela inicial se precisar.
    if not clicar_imagem("data/sair_consumo.png", confidence=0.8, timeout=60,
                         descricao="Saindo do consumo"):
        print("⚠️  Erro ao sair do consumo (o arquivo já foi salvo).")

    return "Arquivo exportado e movido com sucesso"


def automacao_consumo(competencia, log=None, filiais=None):
    """
    Automação de consumo.

    Args:
        competencia: data no formato "DD/MM/YYYY"
        log: instância de LogExecucao (opcional). Se informado, registra cada filial.
        filiais: filiais a processar. Se não informado, usa todas de LISTA_FILIAIS.
    """
    if filiais is None:
        filiais = LISTA_FILIAIS

    # escolhe a opção do relatório de consumo
    if not clicar_imagem("data/menu_consultas.png", confidence=0.8, timeout=60, descricao="Menu Consumo"):
        msg = "Erro ao acessar o menu consultas"
        print(msg)
        registrar_filiais_com_erro(log, filiais, msg)
        return

    time.sleep(2)

    processar_filiais(
        filiais=filiais,
        processar_filial=lambda filial: processar_filial_consumo(filial, competencia),
        voltar_tela_inicial=voltar_tela_inicial_consumo,
        log=log,
    )

    print("\n" + "="*60)
    print("✅ Automação de consumo concluída!")
    print("="*60)
