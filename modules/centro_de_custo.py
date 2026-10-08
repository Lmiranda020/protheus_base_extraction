from modules.clicar_imagem import clicar_imagem
from modules.localizar_imagem import localizar_imagem
from modules.etapa import EtapaFalhou, etapa, processar_filiais, registrar_filiais_com_erro
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


def voltar_tela_inicial_cc(tentativas=6):
    """
    Fecha o que estiver aberto até a opção "Centro de Custo" aparecer na tela
    do Smart View (ponto de partida de cada filial).

    Returns:
        True se a tela inicial está visível, False caso contrário.
    """
    for _ in range(tentativas):
        if localizar_imagem("data/opcao_centro_de_custo.png", confidence=0.9, timeout=5,
                            descricao="Tela inicial (opção Centro de Custo)"):
            return True

        # se a exportação terminou, o botão OK leva de volta à lista de relatórios
        if clicar_imagem("data/botao_ok.png", confidence=0.8, timeout=3,
                         descricao="Botão OK", salvar_print=False):
            time.sleep(3)
            continue

        # caso contrário, fecha o diálogo/janela que estiver na frente
        pyautogui.press('esc')
        time.sleep(3)

    return False


def processar_filial_cc(filial, competencia):
    """
    Exporta o relatório de centro de custo de UMA filial.

    Returns:
        Mensagem de sucesso para o log.

    Raises:
        EtapaFalhou: se alguma etapa não puder ser concluída.
    """
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
    etapa("data/opcao_centro_de_custo.png", "Opção Centro de Custo",
          "Erro ao acessar a opção Centro de Custo", confidence=0.9)

    time.sleep(2)

    # navegar até o campo de filial
    pyautogui.press('tab', presses=2, interval=0.5)

    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.press('backspace')

    pyautogui.write(filial, interval=0.1)
    time.sleep(2)

    etapa("data/botao_confirmar.png", "Botão Confirmar",
          "Erro ao clicar no botão Confirmar")

    time.sleep(5)

    # clicar no botão reforma tributaria (nem sempre aparece, então não é erro)
    if not clicar_imagem("data/botao_reforma_tributaria.png", confidence=0.8, timeout=15,
                         descricao="Botão Reforma Tributária", salvar_print=False):
        print("Botão Reforma Tributária não apareceu, seguindo.")

    time.sleep(8)

    # clicar no menu "planilha"
    etapa("data/opcao_exportar.png", "Menu Planilha",
          "Erro ao clicar na opção selecionada para exportar planilha")

    time.sleep(2)

    # clica em confirmar o tipo de exportação escolhido
    etapa("data/botao_confirmar_exportacao.png", "Botão Confirmar Exportação",
          "Erro ao clicar no botão Confirmar Exportação")

    time.sleep(8)

    # selecionar o tipo de extensão do arquivo csv
    etapa("data/opcao_tipo_csv.png", "Opção Tipo CSV",
          "Erro ao selecionar o tipo CSV", timeout=1800)

    time.sleep(3)

    # clica na opção diretorio
    etapa("data/opcao_diretorio.png", "Opção Diretório",
          "Erro ao clicar na opção diretório")

    time.sleep(2)

    # clicar no campo input para renomear o arquivo
    etapa("data/input_nome_arquivo.png", "Input Nome do Arquivo",
          "Erro ao clicar no input de nome do arquivo")

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
    etapa("data/botao_salvar_arquivo_final.png", "Botão Salvar Arquivo",
          "Erro ao clicar no botão Salvar Arquivo na janela de salvar", confidence=0.9)

    print("🔍 Aguardando conclusão do download...")

    time.sleep(2)

    # clica no botao de download
    etapa("data/botao_download.png", "Botão Download",
          "Erro ao clicar no botão Download")

    novo_arquivo = aguardar_novo_arquivo(
        caminho=caminho_fixo_completo,
        arquivos_antes=arquivos_antes,
        momento_download=momento_download,
        timeout=600,
        intervalo=2,
        margem_seguranca_segundos=30
    )

    if not novo_arquivo:
        raise EtapaFalhou("Download não detectado no tempo esperado (timeout 600s)")

    print(f"📄 Arquivo baixado: {novo_arquivo}")

    # Renomeia o arquivo pro padrão CC_{filial}_{competencia}
    arquivo_final = renomear_arquivo_baixado(
        caminho=caminho_fixo_completo,
        nome_atual=novo_arquivo,
        nome_novo_sem_extensao=nome_arquivo
    )

    if not arquivo_final:
        # Download ocorreu, mas o rename falhou — registra como falha pra ficar
        # visível no log. Não tenta de novo para não gerar arquivo duplicado.
        raise EtapaFalhou(f"Download concluído como '{novo_arquivo}', "
                          f"mas falhou ao renomear para '{nome_arquivo}'",
                          tentar_novamente=False)

    # clica no botão ok para ir para a proxima filial. O arquivo já foi salvo,
    # então uma falha aqui não refaz a filial: a próxima volta para a tela inicial.
    if not clicar_imagem("data/botao_ok.png", confidence=0.8, timeout=60, descricao="Botão OK"):
        print("⚠️  Erro ao clicar no botão OK (o arquivo já foi salvo).")

    return f"Arquivo gerado e renomeado: {arquivo_final}"


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
    if not clicar_imagem("data/menu_consultas.png", confidence=0.8, timeout=60, descricao="Menu Relatórios"):
        msg = "Erro ao acessar o menu Relatórios"
        print(msg)
        registrar_filiais_com_erro(log, LISTA_FILIAIS, msg)
        return

    time.sleep(2)

    # clicar na opção smart view. A falha acontece antes de qualquer filial,
    # então todas ficam registradas como não processadas.
    if not clicar_imagem("data/opcao_smart_view.png", confidence=0.8, timeout=60, descricao="Opção Smart View"):
        msg = "Erro ao acessar a opção Smart View"
        print(msg)
        registrar_filiais_com_erro(log, LISTA_FILIAIS, msg)
        return

    time.sleep(2)

    processar_filiais(
        filiais=LISTA_FILIAIS,
        processar_filial=lambda filial: processar_filial_cc(filial, competencia),
        voltar_tela_inicial=voltar_tela_inicial_cc,
        log=log,
    )

    # fecha o menu Relatórios aberto no início
    if not clicar_imagem("data/menu_relatorios.png", confidence=0.8, timeout=15, descricao="Menu Relatórios"):
        print("Erro ao fechar o menu Relatórios.")

    print("\n" + "="*60)
    print("✅ Automação do centro de custo concluída!")
    print("="*60)
