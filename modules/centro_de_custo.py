from modules.clicar_imagem import clicar_imagem
import time
from config.list_filial import LISTA_FILIAIS
import pyautogui
from datetime import datetime
import os


def listar_arquivos_diretorio(caminho):
    """Lista todos os arquivos em um diretório com seus timestamps de modificação."""
    try:
        if not os.path.exists(caminho):
            print(f"⚠️  Diretório não existe ainda: {caminho}")
            os.makedirs(caminho, exist_ok=True)

        arquivos = {}
        for arquivo in os.listdir(caminho):
            caminho_completo = os.path.join(caminho, arquivo)
            if os.path.isfile(caminho_completo):
                arquivos[arquivo] = os.path.getmtime(caminho_completo)

        return arquivos
    except Exception as e:
        print(f"❌ Erro ao listar arquivos: {e}")
        return {}


def aguardar_novo_arquivo(caminho, arquivos_antes, timeout=300, intervalo=2):
    """
    Aguarda até que um novo arquivo apareça no diretório.

    Returns:
        Nome do novo arquivo encontrado ou None se timeout.
    """
    print(f"⏳ Monitorando diretório por até {timeout} segundos...")
    tempo_inicio   = time.time()
    tempo_decorrido = 0

    while tempo_decorrido < timeout:
        time.sleep(intervalo)
        tempo_decorrido = time.time() - tempo_inicio

        arquivos_agora = listar_arquivos_diretorio(caminho)
        novos_arquivos = set(arquivos_agora.keys()) - set(arquivos_antes.keys())

        if novos_arquivos:
            novo_arquivo = list(novos_arquivos)[0]
            print(f"✅ Novo arquivo detectado: {novo_arquivo}")
            print(f"⏱️  Tempo de espera: {tempo_decorrido:.1f} segundos")
            return novo_arquivo

        for arquivo in arquivos_agora:
            if arquivo in arquivos_antes:
                if arquivos_agora[arquivo] != arquivos_antes[arquivo]:
                    print(f"📝 Arquivo em modificação detectado: {arquivo}")

        if int(tempo_decorrido) % 10 == 0 and tempo_decorrido > 0:
            print(f"⏳ Aguardando... {int(tempo_decorrido)}s / {timeout}s")

    print(f"⚠️  Timeout atingido ({timeout}s) — nenhum novo arquivo detectado")
    return None


def automacao_centro_de_custo(competencia, log=None):
    """
    Automação para download do relatório de centro de custo.

    Args:
        competencia: data no formato "DD/MM/YYYY"
        log: instância de LogExecucao (opcional). Se informado, registra cada filial.
    """
    print("🚀 Iniciando automação do centro de custo...")

    if not clicar_imagem("data/menu_relatorios.png", confidence=0.8, timeout=15, descricao="Menu Relatórios"):
        print("Erro ao acessar o menu Relatórios.")
        return

    for filial in LISTA_FILIAIS:
        inicio_filial = datetime.now()

        print(f"\n{'='*60}")
        print(f"🏢 Processando filial: {filial}")
        print(f"{'='*60}\n")

        # Definir o caminho do diretório
        data = datetime.strptime(competencia, "%d/%m/%Y")
        ano  = data.year
        mes  = str(data.month).zfill(2)   # corrigido: zfill em vez de len check
        caminho_fixo = os.getenv("CAMINHO_FIXO_CC")
        caminho_fixo_completo = f"{caminho_fixo}\\{ano}\\{mes}_{ano}"
        print(f"📂 Caminho: {caminho_fixo_completo}")

        # ANTES DO DOWNLOAD: listar arquivos existentes
        print("📋 Listando arquivos existentes no diretório...")
        arquivos_antes = listar_arquivos_diretorio(caminho_fixo_completo)
        print(f"   Arquivos encontrados: {len(arquivos_antes)}")
        for arquivo in list(arquivos_antes.keys())[:3]:
            print(f"   - {arquivo}")
        if len(arquivos_antes) > 3:
            print(f"   ... e mais {len(arquivos_antes) - 3} arquivo(s)")

        time.sleep(2)

        # clicar na opção "Centro de Custo"
        if not clicar_imagem("data/opcao_centro_de_custo.png", confidence=0.8, timeout=15, descricao="Opção Centro de Custo"):
            msg = "Erro ao acessar a opção Centro de Custo"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        # navegar até o campo de filial
        pyautogui.press('tab', presses=2, interval=0.5)

        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')
        pyautogui.press('backspace')

        pyautogui.write(filial, interval=0.1)
        time.sleep(2)

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

        time.sleep(8)

        # clicar no menu "planilha"
        if not clicar_imagem("data/menu_planilha.png", confidence=0.8, timeout=15, descricao="Menu Planilha"):
            msg = "Erro ao clicar no menu Planilha"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(5)

        # clicar no campo input para renomear o arquivo
        if not clicar_imagem("data/input_nome_arquivo.png", confidence=0.8, timeout=15, descricao="Input Nome do Arquivo"):
            msg = "Erro ao clicar no input de nome do arquivo"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')
        pyautogui.press('backspace')

        nome_arquivo = f"CC_{filial}_{competencia.replace('/', '-')}"
        pyautogui.write(nome_arquivo, interval=0.1)

        # escolhe o tipo de exportação para xlsx
        if not clicar_imagem("data/opcao_tipo_xlsx.png", confidence=0.8, timeout=15, descricao="Opção Tipo XLSX"):
            msg = "Erro ao selecionar o tipo XLSX"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        pyautogui.press('down', presses=3, interval=0.5)
        pyautogui.press('enter')
        time.sleep(2)

        # desflega a opção review
        if not clicar_imagem("data/opcao_desflega_review.png", confidence=0.8, timeout=15, descricao="Opção Desflega Review"):
            msg = "Erro ao desflegar a opção Review"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        # clicar no botão "Salvar"
        if not clicar_imagem("data/botao_salvar_arquivo.png", confidence=0.8, timeout=15, descricao="Botão Salvar Arquivo"):
            msg = "Erro ao clicar no botão Salvar Arquivo"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        # escolhe o input para definir o diretório
        if not clicar_imagem("data/input_diretorio_arquivo.png", confidence=0.8, timeout=15, descricao="Input Diretório Arquivo"):
            msg = "Erro ao clicar no input de diretório do arquivo"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        pyautogui.keyDown('ctrl')
        pyautogui.press('a')
        pyautogui.keyUp('ctrl')
        pyautogui.press('backspace')

        pyautogui.write(caminho_fixo_completo, interval=0.1)
        time.sleep(2)

        # clicar no botão "Salvar" da janela de salvar arquivo
        if not clicar_imagem("data/botao_salvar_arquivo_final.png", confidence=0.8, timeout=15, descricao="Botão Salvar Arquivo"):
            msg = "Erro ao clicar no botão Salvar Arquivo na janela de salvar"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        print("🔍 Aguardando conclusão do download...")

        novo_arquivo = aguardar_novo_arquivo(
            caminho=caminho_fixo_completo,
            arquivos_antes=arquivos_antes,
            timeout=600,
            intervalo=2
        )

        if novo_arquivo:
            print(f"✅ Filial {filial} processada com sucesso!")
            print(f"📄 Arquivo baixado: {novo_arquivo}")
            if log:
                log.registrar_filial(filial, sucesso=True,
                                     mensagem=f"Arquivo gerado: {novo_arquivo}",
                                     inicio_filial=inicio_filial)
        else:
            msg = "Download não detectado no tempo esperado (timeout 600s)"
            print(f"⚠️  Filial {filial} — {msg}")
            print("   Continuando para próxima filial...")
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)

    # fecha o menu Relatórios aberto no início
    if not clicar_imagem("data/menu_relatorios.png", confidence=0.8, timeout=15, descricao="Menu Relatórios"):
        print("Erro ao fechar o menu Relatórios.")

    print("\n" + "="*60)
    print("✅ Automação do centro de custo concluída para todas as filiais!")
    print("="*60)