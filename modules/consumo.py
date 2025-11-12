from modules.clicar_imagem import clicar_imagem
import time
from config.list_filial import LISTA_FILIAIS
import pyautogui
from datetime import datetime
from modules.mover_e_renomear_arquivo_baixado import mover_e_renomear_csv
from modules.aguardar_download_inteligente import aguardar_download_completo, fechar_excel
import os

def automacao_consumo(competencia):
    # escolhe a opção do relatório de consumo
    if not clicar_imagem("data/menu_consultas.png", confidence=0.8, timeout=15, descricao="Menu Consumo"):
        print("Erro ao acessar o menu consultas.")
        return
    time.sleep(2)

    for filial in LISTA_FILIAIS:
        print(f"\n{'='*60}")
        print(f"🏢 Processando filial: {filial}")
        print(f"{'='*60}\n")
        
        time.sleep(5)
        # clica na opção consumo mes a mes
        if not clicar_imagem("data/opcao_genericos.png", confidence=0.8, timeout=15, descricao="Opção genericos"):
            print("Erro ao escolher a opção genericos")
            return
        time.sleep(3)
        
        # selecionar todo o campo focado
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')

        # limpar todo o campo selecionado
        pyautogui.press('backspace')
        time.sleep(2)

        # digitar a competencia que do mês anterior
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
        time.sleep(2)
        if not clicar_imagem("data/botao_confirmar.png", confidence=0.8, timeout=15, descricao="Botão Confirmar"):
            print("Erro ao clicar no botão Confirmar.")
            return
        time.sleep(5)

        # clicar no botão reforma tributaria
        if not clicar_imagem("data/botao_reforma_tributaria.png", confidence=0.8, timeout=15, descricao="Botão Reforma Tributária"):
            print("Erro ao clicar no botão Reforma Tributária.")

        time.sleep(10)
        if not clicar_imagem("data/caixa_pesquisa.png", confidence=0.8, timeout=15, descricao="Caixa de pesquisa"):
            print("Erro ao clicar na caixa de texto.")
            return
        time.sleep(5)

        # selecionar todo o campo focado
        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')

        # limpar todo o campo selecionado
        pyautogui.press('backspace')

        # digitar "sd3"
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
            print("Erro ao clicar na opção dicionário.")
            return
        
        time.sleep(4)
        # marcar a caixa de seleção dicionário
        if not clicar_imagem("data/marcar_caixa_dicionario.png", confidence=0.8, timeout=15, descricao="Caixa dicionário"):
            print("Erro ao flegar a caixa de seleção dicionário.")
            return

        time.sleep(3)
        # marcar em ok
        if not clicar_imagem("data/ok_dicionario.png", confidence=0.8, timeout=15, descricao="Opção 'ok' dicionário"):
            print("Erro ao clicar 'ok' dicionário")
            return

        time.sleep(4)
        # clica na opção filtro
        if not clicar_imagem("data/filtrar_consumo.png", confidence=0.8, timeout=15, descricao="Botão Filtrar"):
            print("Erro ao clicar no filtro.")
            return

        time.sleep(3)        
        # clica na opção criar filtro
        if not clicar_imagem("data/criar_filtro.png", confidence=0.8, timeout=15, descricao="Botão Criar Filtro"):
            print("Erro ao clicar no Criar Filtro.")
            return
        
        time.sleep(3)
        # clicar tres vezes tab
        pyautogui.press('tab', presses=3, interval=0.5)

        # digitar o nome do filtro
        pyautogui.write('Competecia', interval=0.1)

        # selecionar a opção expresssão
        if not clicar_imagem("data/botao_expressao.png", confidence=0.8, timeout=15, descricao="Botão Expressão"):
            print("Erro ao clicar na opção expressão.")
            return
        
        time.sleep(2)
        
        pyautogui.press('tab', presses=2, interval=0.5)

        pyautogui.press('backspace')

        # alterar os dois primeiros digitos da data por 01
        competencia_inicial = "01" + competencia[2:]
        print(competencia_inicial)

        expressao_filtro = f'D3_EMISSAO >= CTOD("{competencia_inicial}") .AND. D3_EMISSAO <= CTOD("{competencia}")'

        # digitar a expressão
        pyautogui.write(expressao_filtro, interval=0.1)
        
        time.sleep(5)

        time.sleep(2)
        # clica no campo para preecher a competencia
        if not clicar_imagem("data/botao_add_filtro.png", confidence=0.8, timeout=15, descricao="Botão Adicionar filtro"):
            print("Erro ao clicar na opção para adicionar filtro")
            return
        
        time.sleep(2)        
        # clicar no botao para salvar o filtro
        if not clicar_imagem("data/botao_salvar_filtro.png", confidence=0.8, timeout=15, descricao="Botão salvar filtro"):
            print("Erro ao clicar na opção salvar filtro")
            return
        
        time.sleep(2)        
        # clicar na caixa de seleção do filtro criado
        if not clicar_imagem("data/selecionar_filtro_selecionado.png", confidence=0.8, timeout=15, descricao="Caixa de seleção do filtro criado"):
            print("Erro ao selecionar a caixa do filtro criado")
            return
        
        time.sleep(2)        
        # clicar no botao para aplicar o filtro
        if not clicar_imagem("data/aplicar_filtro_selecionado.png", confidence=0.8, timeout=15, descricao="Aplicar filtro selecionado"):
            print("Erro ao aplicar o filtro selecionado")
            return

        time.sleep(2)
        # selecionar oo tipo de exportação
        if not clicar_imagem("data/export_csv.png", confidence=0.8, timeout=15, descricao="Selecionar o tipo de opção export"):
            print("Erro ao selecionar o tipo de exportação")
            return

        time.sleep(2)
        # selecionar oo tipo de exportação
        if not clicar_imagem("data/ponto_e_virgula.png", confidence=0.8, timeout=15, descricao="Selecionar o tipo ponto e virgula"):
            print("Erro ao selecionar o tipo ponto e virgula")
            return
        
        time.sleep(2)
        # selecionar a opção "confirmar"
        if not clicar_imagem("data/confirmar_export.png", confidence=0.8, timeout=15, descricao="Confirmar exportação"):
            print("Erro ao confirmar exportação")
            return


        diretorio_temp = os.getenv("DIRETORIO_TEMP")
        
        sucesso, arquivo_baixado, tempo_gasto = aguardar_download_completo(
            diretorio_temp=diretorio_temp,
            timeout=900, 
            intervalo_verificacao=2  # Verifica a cada 2 segundos
        )
        
        if not sucesso:
            print(f"❌ Erro: Download não concluído para a filial {filial}")
            continue
        
        print(f"⚡ Economia de tempo: {900 - tempo_gasto:.1f} segundos!")
        
        # Fecha o Excel antes de mover o arquivo
        fechar_excel()
        
        time.sleep(4)
        
        # Define o diretório de destino
        data = datetime.strptime(competencia, "%d/%m/%Y")
        ano = data.year
        mes = data.month
        caminho_fixo = os.getenv("CAMINHO_FIXO_CONSUMO")
        diretorio_destino = f"{caminho_fixo}\\{ano}\\{mes}_{ano}"
        print(f"📂 Caminho: {diretorio_destino}")
        
        # Move e renomeia o arquivo
        print("Processando arquivo baixado...")
        if mover_e_renomear_csv(filial, competencia, diretorio_destino):
            print(f"✅ Filial {filial} processada com sucesso!")
        else:
            print(f"❌ Erro ao processar o arquivo da filial {filial}")

        time.sleep(5)
        # sair do consumo
        if not clicar_imagem("data/sair_consumo.png", confidence=0.8, timeout=15, descricao="Saindo do consumo"):
            print("Erro ao sair do consumo")
            return

    print("\n" + "="*60)
    print("✅ Automação de consumo concluída para todas as filiais!")
    print("="*60)