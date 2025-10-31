import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.list_filial import LISTA_FILIAIS
from modules.clicar_botao_shadow_dom import clicar_botao_shadow_dom
from modules.clicar_menu_item_direto import clicar_menu_item_direto
from modules.clicar_botao_shadow_por_texto import clicar_botao_shadow_por_texto
from modules.clicar_input_shadow import clicar_input_shadow


def automation_centro_de_custo (competencia, driver):
    """
    Automatiza o download do relatório de centro de custo
    """
    print("=" * 60)
    print("🚀 INICIANDO AUTOMAÇÃO DE CENTRO DE CUSTO")
    print("=" * 60)
    
    # Focar na janela do navegador (assumindo que já está aberta)

    # Clicar no botão "Centro de Custo" usando reconhecimento de imagem
    # Opção 1: Por ID (mais confiável)
    if clicar_menu_item_direto(driver, menu_id="COMP3009"):
        print("✅ Clicado em Cadastros através do botão!")
        time.sleep(2)
    # # Opção 2: Por texto do caption (mais flexível)
    # if clicar_menu_item_direto(driver, caption_texto="Cadastros"):
    #     print("✅ Clicado em Cadastros através do caption!")
    #     time.sleep(2)

    for filial in LISTA_FILIAIS:
        print(f"🏢 Processando filial: {filial}")
    
        # Clicar no botão "Centro de Custo" usando reconhecimento de imagem
        if clicar_menu_item_direto(driver, menu_id="COMP3091"):
                print("✅ Clicado em Centro de Custo através do botão!")
                time.sleep(2)
        # if clicar_menu_item_direto(driver, menu_id="Centro de Custo"):
        #     print("✅ Clicado em Centro de Custo através do caption!")
        #     time.sleep(2)
        
        # da dois tabs para abrir o menu corretamente
        webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(2)

        # apagar o campo selecionado
        webdriver.ActionChains(driver).send_keys(Keys.BACKSPACE).perform()


        # digitar a filial
        webdriver.ActionChains(driver).send_keys(filial).perform()
        time.sleep(2)

        # selecionar o botão confirmar
        # Método 1: Por atributo 'part'
        if clicar_botao_shadow_dom(driver, 'id', 'COMP4522',seletor_interno='button', descricao="Confirmar"):
            print("✅ Clicado em Confirmar através do botão!")
            time.sleep(2)
        # Método 2: Por caption
        else: 
            clicar_botao_shadow_por_texto(driver, 'Confirmar')
            print("✅ Clicado em Confirmar através do texto!")
            time.sleep(2)

        time.sleep(8)
        # selecionar a opção planilha
        if clicar_botao_shadow_dom(driver, 'id', 'COMP4528',seletor_interno='button', descricao="Planilha"):
            print("✅ Clicado em Planilha através do botão!")
            time.sleep(2)
        # Método 2: Por caption
        else: 
            clicar_botao_shadow_por_texto(driver, 'Planilha')
            print("✅ Clicado em Planilha através do texto!")
            time.sleep(2)

        
        # criar a variavel com o nome do arquivo
        nome_arquivo = f"CENTRO_DE_CUSTO_{filial}_{competencia}.xlsx"

        # selecionar o campo nome do arquivo
        if clicar_botao_shadow_dom(driver, 'id', 'COMP4542',seletor_interno='button', descricao="Impressão"):
            print("✅ Clicado em Confirmar através do botão!")
            time.sleep(2)
        # Método 2: Por caption
        else: 
            clicar_botao_shadow_por_texto(driver, 'Impressão')
            print("✅ Clicado em Confirmar através do texto!")
            time.sleep(2)

        # selecionar o campo impressão
        clicar_input_shadow(driver, 'COMP4539')

        # selecionar todo o texto do campo impressão
        webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        time.sleep(1)
        
        # apagar o texto do campo impressão
        webdriver.ActionChains(driver).send_keys(Keys.BACKSPACE).perform()
        
        # preecher o campo impressão com o nome do arquivo

        # clicar no botão imprimir
        
        # caminho fixo
        caminho_fixo = "Y:\CONTROLADORIA\CUSTOS\15_BASES_PROTHEUS\Centro de Custo"

        # join no diretotio com o ano e mes da competencia
        ano = competencia[:4]
        mes = competencia[4:6]
        caminho_fixo_completo = f"{caminho_fixo}\{ano}\{mes}_{ano}"

        # selecioonar o campo servidor

        # limpar o campo de servidor
        webdriver.ActionChains(driver).send_keys(Keys.BACKSPACE).perform()

        # preecher o campo servidor com o caminho fixo
        webdriver.ActionChains(driver).send_keys(caminho_fixo_completo).perform()

        # clicar no botão abrir

        



        

    time.sleep(10)
    print("✓ Download concluído (aguardando validação e organização)")

    print("=" * 60)
    print("✓ AUTOMAÇÃO DE CENTRO DE CUSTO CONCLUÍDA COM SUCESSO!")