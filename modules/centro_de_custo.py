from modules.clicar_imagem import clicar_imagem
import time
from config.list_filial import LISTA_FILIAIS
import pyautogui
from datetime import datetime
from modules.aguardar_download_inteligente import aguardar_download_completo, fechar_excel
import os

def automacao_centro_de_custo(competencia):
    """
    Automação para download do relatório de centro de custo
    """ 
    print("🚀Iniciando automação do centro de custo...")
    # no menu a oção "Relatórios"
    if not clicar_imagem("data/menu_relatorios.png", confidence=0.8, timeout=15, descricao="Menu Relatórios"):
        print("Erro ao acessar o menu Relatórios.")
        return
    
    for filial in LISTA_FILIAIS:
        print(f"\n{'='*60}")
        print(f"🏢 Processando filial: {filial}")
        print(f"{'='*60}\n")
        
        time.sleep(2)
        # clicar na opção "Centro de Custo"
        if not clicar_imagem("data/opcao_centro_de_custo.png", confidence=0.8, timeout=15, descricao="Opção Centro de Custo"):
            print("Erro ao acessar a opção Centro de Custo.")
            return
        
        time.sleep(2)
        
        # clicar duas vezes o tab
        pyautogui.press('tab', presses=2, interval=0.5)

        # seleciona todo o campo 
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')

        # apaga o conteúdo do campo
        pyautogui.press('backspace')

        # digita a filial
        pyautogui.write(filial, interval=0.1)

        # clica no botão "Confirmar"
        time.sleep(2)
        if not clicar_imagem("data/botao_confirmar.png", confidence=0.8, timeout=15, descricao="Botão Confirmar"):
            print("Erro ao clicar no botão Confirmar.")
            return
        
        time.sleep(8)

        # clicar no menu "planilha"
        if not clicar_imagem("data/menu_planilha.png", confidence=0.8, timeout=15, descricao="Menu Planilha"):
            print("Erro ao clicar no menu Planilha.")
            return
        
        time.sleep(5)

        # clicar no campo input para renomear o arquivo
        if not clicar_imagem("data/input_nome_arquivo.png", confidence=0.8, timeout=15, descricao="Input Nome do Arquivo"):
            print("Erro ao clicar no input de nome do arquivo.")
            return

        # selecionar o conteúdo do campo
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')

        # apagar o conteúdo do campo
        pyautogui.press('backspace')

        # digitar o nome do arquivo com a filial
        nome_arquivo = f"CC_{filial}_{competencia.replace('/', '-')}"
        pyautogui.write(nome_arquivo, interval=0.1)

        # escolhe o tipo de exportação para xlsx
        if not clicar_imagem("data/opcao_tipo_xlsx.png", confidence=0.8, timeout=15, descricao="Opção Tipo XLSX"):
            print("Erro ao selecionar o tipo XLSX.")
            return
        
        time.sleep(2)

        # clicar tres vezes a seta para baixo
        pyautogui.press('down', presses=3, interval=0.5)
        pyautogui.press('enter')
        time.sleep(2)

        # desflega a opção review
        if not clicar_imagem("data/opcao_desflega_review.png", confidence=0.8, timeout=15, descricao="Opção Desflega Review"):
            print("Erro ao desflegar a opção Review.")
            return
        time.sleep(2)

        # clicar no botão "Salvar"
        if not clicar_imagem("data/botao_salvar_arquivo.png", confidence=0.8, timeout=15, descricao="Botão Salvar Arquivo"):
            print("Erro ao clicar no botão Salvar Arquivo.")
            return  
        time.sleep(2)

        # escolhe o input para definir o diretorio
        if not clicar_imagem("data/input_diretorio_arquivo.png", confidence=0.8, timeout=15, descricao="Input Diretório Arquivo"):
            print("Erro ao clicar no input de diretório do arquivo.")
            return
        time.sleep(2)

        # seleciona o conteúdo do campo
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')

        # apaga o conteúdo do campo
        pyautogui.press('backspace')

        # definir o nome do diretório de centro de custo
        data = datetime.strptime(competencia, "%d/%m/%Y")
        ano = data.year
        mes = data.month
        caminho_fixo = os.getenv("CAMINHO_FIXO_CC")
        caminho_fixo_completo = f"{caminho_fixo}\\{ano}\\{mes}_{ano}"
        print(f"📂 Caminho: {caminho_fixo_completo}")

        # digita o caminho da pasta de centro de custo  
        pyautogui.write(caminho_fixo_completo, interval=0.1)

        # clicar no botão "Salvar" da janela de salvar arquivo
        if not clicar_imagem("data/botao_salvar_arquivo_final.png", confidence=0.8, timeout=15, descricao="Botão Salvar Arquivo"):
            print("Erro ao clicar no botão Salvar Arquivo na janela de salvar.")
            return

        print("🔍 Aguardando conclusão do download...")
        
        sucesso, arquivo_baixado, tempo_gasto = aguardar_download_completo(
            diretorio_temp=caminho_fixo_completo,
            timeout=100,  
            intervalo_verificacao=2  # Verifica a cada 2 segundos
        )
        
        if not sucesso:
            print(f"❌ Erro: Download não concluído para a filial {filial}")
            continue
        
        print(f"⚡ Tempo de download: {tempo_gasto:.1f} segundos")
        print(f"💡 Economia: {200 - tempo_gasto:.1f} segundos comparado ao timeout!")
        
        # Fecha o Excel antes de continuar
        fechar_excel()
        
        print(f"✅ Filial {filial} processada com sucesso!")

    # clica no menu a opção "Relatórios", para fechar o menu aberto inicialmente
    if not clicar_imagem("data/menu_relatorios.png", confidence=0.8, timeout=15, descricao="Menu Relatórios"):
        print("Erro ao acessar o menu Relatórios.")
        exit(1)
    
    print("\n" + "="*60)
    print("✅ Automação do centro de custo concluída para todas as filiais!")
    print("="*60)