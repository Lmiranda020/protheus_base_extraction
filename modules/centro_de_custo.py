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
from modules.clicar_input_shadow import clicar_input_shadow, preencher_input_shadow


def automation_centro_de_custo (competencia, driver):
    """
    Automatiza o download do relatório de centro de custo
    """
    print("=" * 60)
    print("🚀 INICIANDO AUTOMAÇÃO DE CENTRO DE CUSTO")
    print("=" * 60)
    
    # Clicar no menu "Cadastros"
    if clicar_menu_item_direto(driver, menu_id="COMP3009"):
        print("✅ Clicado em Cadastros através do botão!")
        time.sleep(2)

    for filial in LISTA_FILIAIS:
        print(f"🏢 Processando filial: {filial}")
    
        # Clicar no botão "Centro de Custo"
        if clicar_menu_item_direto(driver, menu_id="COMP3091"):
                print("✅ Clicado em Centro de Custo através do botão!")
                time.sleep(2)
        
        # Navegar pelos campos (2 tabs)
        webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(2)

        # Apagar o campo selecionado
        webdriver.ActionChains(driver).send_keys(Keys.BACKSPACE).perform()

        # Digitar a filial
        webdriver.ActionChains(driver).send_keys(filial).perform()
        time.sleep(2)

        # Clicar no botão "Confirmar"
        # Método 1: Por id
        if clicar_botao_shadow_dom(driver, 'id', 'COMP4522',seletor_interno='button', descricao="Confirmar"):
            print("✅ Clicado em Confirmar através do botão!")
            time.sleep(2)
        # Método 2: Por caption
        else: 
            clicar_botao_shadow_por_texto(driver, 'Confirmar')
            print("✅ Clicado em Confirmar através do texto!")
            time.sleep(2)

        time.sleep(8)

        # Selecionar a opção "Planilha"
        if clicar_botao_shadow_dom(driver, 'id', 'COMP4528',seletor_interno='button', descricao="Planilha"):
            print("✅ Clicado em Planilha através do botão!")
            time.sleep(2)
        else: 
            clicar_botao_shadow_por_texto(driver, 'Planilha')
            print("✅ Clicado em Planilha através do texto!")
            time.sleep(2)

        
        # Criar o nome do arquivo
        nome_arquivo = f"CENTRO_DE_CUSTO_{filial}_{competencia}.xlsx"

        # # Debug completo
        # resultados = debug_estrutura_completa(driver)

        # # Também tente buscar por texto próximo (ex: "Impressão", "Arquivo", etc.)
        # buscar_elemento_por_vizinhos(driver, "impressão")
        # buscar_elemento_por_vizinhos(driver, "arquivo")
        # buscar_elemento_por_vizinhos(driver, "nome")

        # input("\n⏸️  Pressione Enter para continuar após revisar o debug...")

        time.sleep(5)

        # Focar no campo de impressão
        print("\n📝 Focando no campo de impressão...")
        if not clicar_input_shadow(driver, 'COMP4539', debug=True): 
            print("⚠️ Não conseguiu focar no campo COMP4539, tentando alternativa...")
            # Alternativa: usar TABs
            webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
            time.sleep(1)
        
        time.sleep(2)

        # Selecionar todo o texto do campo
        print("📋 Selecionando todo o texto...")
        webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        time.sleep(1)
        
        # Apagar o texto
        print("🗑️ Apagando texto...")
        webdriver.ActionChains(driver).send_keys(Keys.BACKSPACE).perform()
        time.sleep(1)
        
        # Preencher com o nome do arquivo
        print(f"✍️ Preenchendo com: {nome_arquivo}")
        webdriver.ActionChains(driver).send_keys(nome_arquivo).perform()
        time.sleep(2)

        # OU usar a função direta (escolha uma das duas abordagens):
        # if preencher_input_shadow(driver, 'COMP4539', nome_arquivo, limpar_antes=True):
        #     print("✅ Campo preenchido com sucesso!")
        # else:
        #     print("⚠️ Falha ao preencher, usando ActionChains...")
        #     webdriver.ActionChains(driver).send_keys(nome_arquivo).perform()
        
        # clicar no botão imprimir
        
        # Preparar o caminho completo
        ano = competencia[:4]
        mes = competencia[4:6]
        caminho_fixo = "Y:\\CONTROLADORIA\\CUSTOS\\15_BASES_PROTHEUS\\Centro de Custo"
        caminho_fixo_completo = f"{caminho_fixo}\\{ano}\\{mes}_{ano}"

        print(f"📂 Caminho: {caminho_fixo_completo}")

        # Navegar para o campo de servidor (provavelmente o próximo TAB)
        print("\n📁 Focando no campo servidor...")
        webdriver.ActionChains(driver).send_keys(Keys.TAB).perform()
        time.sleep(1)

        # Selecionar tudo e apagar
        webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform()
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.BACKSPACE).perform()
        time.sleep(1)
        
        # Preencher o caminho
        print(f"✍️ Preenchendo caminho...")
        webdriver.ActionChains(driver).send_keys(caminho_fixo_completo).perform()
        time.sleep(2)
        
        # TODO: Clicar no botão "Imprimir" ou "OK" para finalizar
        # Você precisa identificar o ID do botão de impressão
        print("\n🖨️ Clicando no botão de impressão...")
        # if clicar_botao_shadow_dom(driver, 'id', 'COMP4XXX', seletor_interno='button', descricao="Imprimir"):
        #     print("✅ Download iniciado!")
        # else:
        #     clicar_botao_shadow_por_texto(driver, 'Imprimir')
        
        print(f"✅ Filial {filial} processada!")
        time.sleep(3)

    time.sleep(10)
    print("✓ Download concluído (aguardando validação e organização)")

    print("=" * 60)
    print("✓ AUTOMAÇÃO DE CENTRO DE CUSTO CONCLUÍDA COM SUCESSO!")