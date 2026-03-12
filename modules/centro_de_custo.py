from modules.clicar_imagem import clicar_imagem
import time
from config.list_filial import LISTA_FILIAIS
import pyautogui
from datetime import datetime
import os

def listar_arquivos_diretorio(caminho):
    """
    Lista todos os arquivos em um diretório com seus timestamps de modificação
    """
    try:
        # se o diretorio não exitir, cria o diretório
        if not os.path.exists(caminho):
            print(f"⚠️  Diretório não existe ainda: {caminho}")
            os.makedirs(caminho, exist_ok=True)
        
        arquivos = {}
        for arquivo in os.listdir(caminho):
            caminho_completo = os.path.join(caminho, arquivo)
            if os.path.isfile(caminho_completo):
                # Guarda o timestamp de modificação
                arquivos[arquivo] = os.path.getmtime(caminho_completo)
        
        return arquivos
    except Exception as e:
        print(f"❌ Erro ao listar arquivos: {e}")
        return {}

def aguardar_novo_arquivo(caminho, arquivos_antes, timeout=300, intervalo=2):
    """
    Aguarda até que um novo arquivo apareça no diretório
    
    Args:
        caminho: Caminho do diretório a monitorar
        arquivos_antes: Dicionário com arquivos existentes antes do download
        timeout: Tempo máximo de espera em segundos (padrão: 5 minutos)
        intervalo: Intervalo entre verificações em segundos
    
    Returns:
        Nome do novo arquivo encontrado ou None se timeout
    """
    print(f"⏳ Monitorando diretório por até {timeout} segundos...")
    tempo_inicio = time.time()
    tempo_decorrido = 0
    
    while tempo_decorrido < timeout:
        time.sleep(intervalo)
        tempo_decorrido = time.time() - tempo_inicio
        
        # Lista arquivos atuais
        arquivos_agora = listar_arquivos_diretorio(caminho)
        
        # Verifica se há novos arquivos
        novos_arquivos = set(arquivos_agora.keys()) - set(arquivos_antes.keys())
        
        if novos_arquivos:
            novo_arquivo = list(novos_arquivos)[0]
            print(f"✅ Novo arquivo detectado: {novo_arquivo}")
            print(f"⏱️  Tempo de espera: {tempo_decorrido:.1f} segundos")
            return novo_arquivo
        
        # Verifica se algum arquivo foi modificado (pode estar sendo baixado)
        for arquivo in arquivos_agora:
            if arquivo in arquivos_antes:
                if arquivos_agora[arquivo] != arquivos_antes[arquivo]:
                    print(f"📝 Arquivo em modificação detectado: {arquivo}")
        
        # Mostra progresso a cada 10 segundos
        if int(tempo_decorrido) % 10 == 0 and tempo_decorrido > 0:
            print(f"⏳ Aguardando... {int(tempo_decorrido)}s / {timeout}s")
    
    print(f"⚠️  Timeout atingido ({timeout}s) - nenhum novo arquivo detectado")
    return None

def automacao_centro_de_custo(competencia):
    """
    Automação para download do relatório de centro de custo
    """ 
    print("🚀 Iniciando automação do centro de custo...")
    
    # no menu a opção "Relatórios"
    if not clicar_imagem("data/menu_relatorios.png", confidence=0.8, timeout=15, descricao="Menu Relatórios"):
        print("Erro ao acessar o menu Relatórios.")
        return
    
    for filial in LISTA_FILIAIS:
        print(f"\n{'='*60}")
        print(f"🏢 Processando filial: {filial}")
        print(f"{'='*60}\n")
        
        # Definir o caminho do diretório
        data = datetime.strptime(competencia, "%d/%m/%Y")
        ano = data.year
        mes = data.month
        caminho_fixo = os.getenv("CAMINHO_FIXO_CC")
        if len(mes) == 1:
            mes = f"0{mes}"
        caminho_fixo_completo = f"{caminho_fixo}\\{ano}\\{mes}_{ano}"
        print(f"📂 Caminho: {caminho_fixo_completo}")
        
        # ANTES DE INICIAR O DOWNLOAD: Listar arquivos existentes
        print(f"📋 Listando arquivos existentes no diretório...")
        arquivos_antes = listar_arquivos_diretorio(caminho_fixo_completo)
        print(f"   Arquivos encontrados: {len(arquivos_antes)}")
        if arquivos_antes:
            for arquivo in list(arquivos_antes.keys())[:3]:  # Mostra apenas os 3 primeiros
                print(f"   - {arquivo}")
            if len(arquivos_antes) > 3:
                print(f"   ... e mais {len(arquivos_antes) - 3} arquivo(s)")
        
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
        time.sleep(2)

        # clica no botão "Confirmar"
        
        if not clicar_imagem("data/botao_confirmar.png", confidence=0.8, timeout=15, descricao="Botão Confirmar"):
            print("Erro ao clicar no botão Confirmar.")
            return
        
        time.sleep(5)

        # clicar no botão reforma tributaria
        if not clicar_imagem("data/botao_reforma_tributaria.png", confidence=0.8, timeout=15, descricao="Botão Reforma Tributária"):
            print("Erro ao clicar no botão Reforma Tributária.")

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

        # digita o caminho da pasta de centro de custo  
        pyautogui.write(caminho_fixo_completo, interval=0.1)

        time.sleep(2)

        # clicar no botão "Salvar" da janela de salvar arquivo
        if not clicar_imagem("data/botao_salvar_arquivo_final.png", confidence=0.8, timeout=15, descricao="Botão Salvar Arquivo"):
            print("Erro ao clicar no botão Salvar Arquivo na janela de salvar.")
            return

        print("🔍 Aguardando conclusão do download...")

        # AGUARDAR NOVO ARQUIVO SER BAIXADO
        novo_arquivo = aguardar_novo_arquivo(
            caminho=caminho_fixo_completo,
            arquivos_antes=arquivos_antes,
            timeout=600,  # 5 minutos de timeout
            intervalo=2   # Verifica a cada 2 segundos
        )
        
        if novo_arquivo:
            print(f"✅ Filial {filial} processada com sucesso!")
            print(f"📄 Arquivo baixado: {novo_arquivo}")
        else:
            print(f"⚠️  Filial {filial} - Download não detectado no tempo esperado")
            print(f"   Continuando para próxima filial...")

    # clica no menu a opção "Relatórios", para fechar o menu aberto inicialmente
    if not clicar_imagem("data/menu_relatorios.png", confidence=0.8, timeout=15, descricao="Menu Relatórios"):
        print("Erro ao acessar o menu Relatórios.")
        return
    
    print("\n" + "="*60)
    print("✅ Automação do centro de custo concluída para todas as filiais!")
    print("="*60)