from modules.clicar_imagem import clicar_imagem
import time
from config.list_filial import LISTA_FILIAIS
import pyautogui
from datetime import datetime, timedelta
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


def arquivo_esta_estavel(caminho_completo, tentativas=3, intervalo=2):
    """
    Verifica se o arquivo parou de ser escrito (tamanho estável entre leituras).
    Em pastas de rede o download pode "aparecer" antes de terminar de gravar,
    então confirmamos que o tamanho não muda por algumas verificações seguidas.

    Returns:
        True se o arquivo ficou estável, False se não foi possível confirmar.
    """
    try:
        tamanho_anterior = -1
        estavel_count = 0

        for _ in range(tentativas + 5):  # margem extra de tentativas
            if not os.path.exists(caminho_completo):
                return False

            tamanho_atual = os.path.getsize(caminho_completo)

            if tamanho_atual == tamanho_anterior and tamanho_atual > 0:
                estavel_count += 1
                if estavel_count >= tentativas:
                    return True
            else:
                estavel_count = 0

            tamanho_anterior = tamanho_atual
            time.sleep(intervalo)

        return False
    except Exception as e:
        print(f"❌ Erro ao verificar estabilidade do arquivo: {e}")
        return False


def aguardar_novo_arquivo(caminho, arquivos_antes, momento_download=None, timeout=300,
                           intervalo=2, margem_seguranca_segundos=30):
    """
    Aguarda até que um novo arquivo apareça no diretório, confirma que ele foi
    salvo depois do momento em que a exportação foi acionada (evita pegar um
    arquivo antigo por engano) e espera ele ficar estável (gravação concluída).

    Args:
        caminho: diretório monitorado
        arquivos_antes: snapshot {nome: mtime} de antes do download
        momento_download: datetime de referência — o arquivo novo precisa ter
                           mtime posterior a esse horário (com margem) para ser
                           considerado válido
        timeout: tempo máximo de espera em segundos
        intervalo: intervalo entre verificações
        margem_seguranca_segundos: tolerância aplicada antes de momento_download,
                           pra absorver diferença de relógio entre a máquina local
                           e o servidor de rede, e pequenos delays entre o clique
                           e o início real da gravação do arquivo

    Returns:
        Nome do novo arquivo encontrado e confirmado, ou None se timeout/inválido.
    """
    print(f"⏳ Monitorando diretório por até {timeout} segundos...")
    tempo_inicio = time.time()
    tempo_decorrido = 0

    while tempo_decorrido < timeout:
        time.sleep(intervalo)
        tempo_decorrido = time.time() - tempo_inicio

        arquivos_agora = listar_arquivos_diretorio(caminho)
        novos_arquivos = set(arquivos_agora.keys()) - set(arquivos_antes.keys())

        if novos_arquivos:
            novo_arquivo = list(novos_arquivos)[0]
            caminho_completo = os.path.join(caminho, novo_arquivo)

            # Verifica se o horário de modificação é posterior ao início da exportação
            # (com margem de segurança pra absorver delay/diferença de relógio)
            if momento_download:
                mtime_arquivo = datetime.fromtimestamp(os.path.getmtime(caminho_completo))
                limite_aceitavel = momento_download - timedelta(seconds=margem_seguranca_segundos)
                if mtime_arquivo < limite_aceitavel:
                    print(f"⚠️  Arquivo '{novo_arquivo}' encontrado, mas o horário "
                          f"({mtime_arquivo.strftime('%H:%M:%S')}) é anterior ao limite aceitável "
                          f"({limite_aceitavel.strftime('%H:%M:%S')}, margem de "
                          f"{margem_seguranca_segundos}s antes de "
                          f"{momento_download.strftime('%H:%M:%S')}). Ignorando.")
                    continue

            print(f"✅ Novo arquivo detectado: {novo_arquivo}")
            print(f"⏱️  Tempo de espera: {tempo_decorrido:.1f} segundos")

            # Confirma que o arquivo terminou de ser gravado na rede
            print("🔍 Confirmando que o arquivo terminou de ser salvo...")
            if arquivo_esta_estavel(caminho_completo):
                print(f"✅ Arquivo '{novo_arquivo}' confirmado como salvo (tamanho estável).")
                return novo_arquivo
            else:
                print(f"⚠️  Não foi possível confirmar estabilidade de '{novo_arquivo}'. "
                      f"Seguindo mesmo assim, mas vale checar manualmente.")
                return novo_arquivo

        for arquivo in arquivos_agora:
            if arquivo in arquivos_antes:
                if arquivos_agora[arquivo] != arquivos_antes[arquivo]:
                    print(f"📝 Arquivo em modificação detectado: {arquivo}")

        if int(tempo_decorrido) % 10 == 0 and tempo_decorrido > 0:
            print(f"⏳ Aguardando... {int(tempo_decorrido)}s / {timeout}s")

    print(f"⚠️  Timeout atingido ({timeout}s) — nenhum novo arquivo detectado")
    return None


def renomear_arquivo_baixado(caminho, nome_atual, nome_novo_sem_extensao):
    """
    Renomeia o arquivo recém-baixado para o padrão desejado (ex: CC_FILIAL_DD-MM-YYYY),
    preservando a extensão original. Se já existir um arquivo com o nome de destino,
    adiciona um sufixo numérico para não sobrescrever nada.

    Returns:
        Nome final do arquivo (já renomeado) ou None se falhou.
    """
    try:
        caminho_atual = os.path.join(caminho, nome_atual)
        extensao = os.path.splitext(nome_atual)[1]  # inclui o ponto, ex: ".csv"

        nome_destino = f"{nome_novo_sem_extensao}{extensao}"
        caminho_destino = os.path.join(caminho, nome_destino)

        # Evita sobrescrever caso já exista um arquivo com esse nome
        contador = 1
        while os.path.exists(caminho_destino):
            nome_destino = f"{nome_novo_sem_extensao}_{contador}{extensao}"
            caminho_destino = os.path.join(caminho, nome_destino)
            contador += 1

        os.rename(caminho_atual, caminho_destino)
        print(f"✏️  Arquivo renomeado: '{nome_atual}' → '{nome_destino}'")
        return nome_destino
    except Exception as e:
        print(f"❌ Erro ao renomear arquivo '{nome_atual}': {e}")
        return None


def automacao_centro_de_custo(competencia, log=None):
    """
    Automação para download do relatório de centro de custo.

    Args:
        competencia: data no formato "DD/MM/YYYY"
        log: instância de LogExecucao (opcional). Se informado, registra cada filial.
    """
    print("🚀 Iniciando automação do centro de custo...")

    time.sleep(2)

    # clicar em consultas 
    if not clicar_imagem("data/menu_consultas.png", confidence=0.8, timeout=15, descricao="Menu Relatórios"):
        print("Erro ao acessar o menu Relatórios.")
        return
    
    time.sleep(2)

    # clicar na opção smart view
    if not clicar_imagem("data/opcao_smart_view.png", confidence=0.8, timeout=15, descricao="Opção Smart View"):
        msg = "Erro ao acessar a opção Smart View"
        print(msg)
        if log:
            log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                    inicio_filial=inicio_filial)
        return

    time.sleep(2)

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

        # ANTES DO DOWNLOAD: listar arquivos existentes na rede
        # (isso é o que garante que, ao comparar depois, a gente saiba
        # exatamente qual arquivo é novo e precisa ser renomeado)
        print("📋 Listando arquivos existentes no diretório...")
        arquivos_antes = listar_arquivos_diretorio(caminho_fixo_completo)
        print(f"   Arquivos encontrados: {len(arquivos_antes)}")
        for arquivo in list(arquivos_antes.keys())[:3]:
            print(f"   - {arquivo}")
        if len(arquivos_antes) > 3:
            print(f"   ... e mais {len(arquivos_antes) - 3} arquivo(s)")

        time.sleep(2)

        # clicar na opção "Centro de Custo"
        if not clicar_imagem("data/opcao_centro_de_custo.png", confidence=0.9, timeout=15, descricao="Opção Centro de Custo"):
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
        if not clicar_imagem("data/opcao_exportar.png", confidence=0.8, timeout=15, descricao="Menu Planilha"):
            msg = "Erro ao clicar na opção selecionada para exportar planilha"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

        # clica em confirmar o tipo de exportação escolhido
        if not clicar_imagem("data/botao_confirmar_exportacao.png", confidence=0.8, timeout=15, descricao="Botão Confirmar Exportação"):
            msg = "Erro ao clicar no botão Confirmar Exportação"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(8)

        # selecionar o tipo de extensão do arquivo csv
        if not clicar_imagem("data/opcao_tipo_csv.png", confidence=0.8, timeout=1800, descricao="Opção Tipo CSV"):
            msg = "Erro ao selecionar o tipo CSV"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(3)

        # clica na opção diretorio
        if not clicar_imagem("data/opcao_diretorio.png", confidence=0.8, timeout=15, descricao="Opção Diretório"):
            msg = "Erro ao clicar na opção diretório"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        time.sleep(2)

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

        # Nome final desejado para o arquivo (sem extensão — a extensão é
        # preservada automaticamente na hora de renomear, depois do download)
        nome_arquivo = f"CC_{filial}_{competencia.replace('/', '-')}"

        # junta o nome do diretorio com o nome do arquivo
        caminho_fixo_completo_p_digitar = caminho_fixo_completo
        pyautogui.write(caminho_fixo_completo_p_digitar, interval=0.1)
        pyautogui.press('enter')
        time.sleep(2)

        # marca o horário ANTES do clique em "Salvar Arquivo Final" — é esse
        # clique que efetivamente dispara a exportação/gravação do arquivo na
        # rede (o botão "Download" logo depois é só confirmação/acompanhamento
        # da UI), então a referência de horário precisa vir de antes dele,
        # não depois. Uma margem de segurança extra é aplicada na comparação
        # dentro de aguardar_novo_arquivo pra absorver qualquer delay residual.
        momento_download = datetime.now()

        # clicar no botão "Salvar" da janela de salvar arquivo
        if not clicar_imagem("data/botao_salvar_arquivo_final.png", confidence=0.9, timeout=15, descricao="Botão Salvar Arquivo"):
            msg = "Erro ao clicar no botão Salvar Arquivo na janela de salvar"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        print("🔍 Aguardando conclusão do download...")

        time.sleep(2)

        # clica no botao de download
        if not clicar_imagem("data/botao_download.png", confidence=0.8, timeout=15, descricao="Botão Download"):
            msg = "Erro ao clicar no botão Download"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

        novo_arquivo = aguardar_novo_arquivo(
            caminho=caminho_fixo_completo,
            arquivos_antes=arquivos_antes,
            momento_download=momento_download,
            timeout=600,
            intervalo=2,
            margem_seguranca_segundos=30
        )

        if novo_arquivo:
            print(f"✅ Filial {filial} processada com sucesso!")
            print(f"📄 Arquivo baixado: {novo_arquivo}")

            # Renomeia o arquivo pro padrão CC_{filial}_{competencia}
            arquivo_final = renomear_arquivo_baixado(
                caminho=caminho_fixo_completo,
                nome_atual=novo_arquivo,
                nome_novo_sem_extensao=nome_arquivo
            )

            if arquivo_final:
                if log:
                    log.registrar_filial(filial, sucesso=True,
                                         mensagem=f"Arquivo gerado e renomeado: {arquivo_final}",
                                         inicio_filial=inicio_filial)
            else:
                # Download ocorreu, mas o rename falhou — registra como falha
                # pra ficar visível no log que essa filial precisa de atenção
                msg = (f"Download concluído como '{novo_arquivo}', "
                       f"mas falhou ao renomear para '{nome_arquivo}'")
                print(f"⚠️  {msg}")
                if log:
                    log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                         inicio_filial=inicio_filial)
        else:
            msg = "Download não detectado no tempo esperado (timeout 600s)"
            print(f"⚠️  Filial {filial} — {msg}")
            print("   Continuando para próxima filial...")
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)

        # clica no botão ok para ir para a proxima filial
        if not clicar_imagem("data/botao_ok.png", confidence=0.8, timeout=15, descricao="Botão OK"):
            msg = "Erro ao clicar no botão OK para ir para a próxima filial"
            print(msg)
            if log:
                log.registrar_filial(filial, sucesso=False, mensagem=msg,
                                     inicio_filial=inicio_filial)
            return

    # fecha o menu Relatórios aberto no início
    if not clicar_imagem("data/menu_relatorios.png", confidence=0.8, timeout=15, descricao="Menu Relatórios"):
        print("Erro ao fechar o menu Relatórios.")

    print("\n" + "="*60)
    print("✅ Automação do centro de custo concluída para todas as filiais!")
    print("="*60)