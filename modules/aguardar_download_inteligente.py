import os
import time
import psutil
import tempfile
from pathlib import Path

def verificar_excel_aberto():
    """Verifica se há alguma instância do Excel aberta"""
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and 'EXCEL.EXE' in proc.info['name'].upper():
                return True
        return False
    except Exception as e:
        print(f"Erro ao verificar Excel: {e}")
        return False

def obter_arquivo_mais_recente(diretorio, extensao='.csv'):
    """Retorna o arquivo mais recente com a extensão especificada e seu timestamp"""
    try:
        arquivos = [os.path.join(diretorio, f) for f in os.listdir(diretorio) 
                   if f.lower().endswith(extensao.lower())]
        if not arquivos:
            return None, None
        arquivo_mais_recente = max(arquivos, key=os.path.getctime)
        timestamp = os.path.getctime(arquivo_mais_recente)
        return arquivo_mais_recente, timestamp
    except Exception as e:
        print(f"Erro ao buscar arquivo: {e}")
        return None, None


def _diretorios_monitorados(diretorio_temp):
    """
    Pastas onde o Protheus pode salvar o CSV exportado: a configurada no .env
    (DIRETORIO_TEMP) e a pasta temporária do Windows (%TEMP%), que o sistema
    passou a usar em nov/2026.
    """
    diretorios = []
    for d in (diretorio_temp, tempfile.gettempdir()):
        if d and os.path.isdir(d) and os.path.normcase(os.path.abspath(d)) not in                 [os.path.normcase(os.path.abspath(x)) for x in diretorios]:
            diretorios.append(d)
    return diretorios


def _listar_csvs(diretorios):
    """Retorna {caminho: mtime} de todos os CSV (.csv ou .CSV) das pastas."""
    arquivos = {}
    for d in diretorios:
        try:
            for f in os.listdir(d):
                if f.lower().endswith('.csv'):
                    caminho = os.path.join(d, f)
                    if os.path.isfile(caminho):
                        arquivos[caminho] = os.path.getmtime(caminho)
        except Exception as e:
            print(f"Erro ao listar {d}: {e}")
    return arquivos


def _csv_novo(diretorios, csvs_antes):
    """CSV mais recente que apareceu (ou foi alterado) depois do snapshot, ou None."""
    novos = {c: m for c, m in _listar_csvs(diretorios).items()
             if c not in csvs_antes or m > csvs_antes[c]}
    return max(novos, key=novos.get) if novos else None


def arquivo_aberto_no_excel(desde=None):
    """
    Retorna o CSV que o Excel abriu (lido da linha de comando do processo).
    Assim o arquivo é encontrado mesmo que o Protheus salve em outra pasta.

    Args:
        desde: timestamp; só aceita arquivos modificados depois dele
    """
    try:
        for proc in psutil.process_iter(['name', 'cmdline']):
            if not (proc.info['name'] and 'EXCEL.EXE' in proc.info['name'].upper()):
                continue
            for arg in reversed(proc.info['cmdline'] or []):
                if arg.lower().endswith('.csv') and os.path.isfile(arg):
                    if desde is None or os.path.getmtime(arg) >= desde:
                        return arg
    except Exception as e:
        print(f"Erro ao verificar arquivo aberto no Excel: {e}")
    return None


def aguardar_download_completo(diretorio_temp, timeout=200, intervalo_verificacao=2):
    """
    Aguarda o download ser concluído monitorando:
    1. Abertura automática do Excel
    2. O CSV gerado: o que o Excel abriu ou um CSV novo em DIRETORIO_TEMP / %TEMP%
    
    Args:
        diretorio_temp: diretório onde os arquivos são baixados
        timeout: tempo máximo de espera em segundos (padrão: 200s)
        intervalo_verificacao: intervalo entre verificações em segundos (padrão: 2s)
    
    Returns:
        tuple: (sucesso, arquivo_path, tempo_decorrido)
    """
    print("🔍 Monitorando download...")

    diretorios = _diretorios_monitorados(diretorio_temp)
    print(f"   Pastas monitoradas: {', '.join(diretorios)}")

    # Registra os CSV que já existem ANTES do download
    csvs_antes = _listar_csvs(diretorios)
    
    tempo_inicio = time.time()
    tempo_decorrido = 0
    excel_detectado = False
    
    while tempo_decorrido < timeout:
        # Condição 1: Excel foi aberto automaticamente
        if not excel_detectado and verificar_excel_aberto():
            excel_detectado = True
            print("✅ Excel detectado aberto (download em progresso/concluído)")

        # Condição 2: arquivo gerado (prioridade para o que o Excel abriu)
        arquivo = None
        if excel_detectado:
            arquivo = arquivo_aberto_no_excel(desde=tempo_inicio - 5) or _csv_novo(diretorios, csvs_antes)

        # Se ambas condições forem atendidas, considera download completo
        if arquivo:
            print(f"✅ Arquivo gerado: {arquivo}")
            # Aguarda mais um pouco para garantir que o arquivo está completo
            print("⏳ Aguardando estabilização do arquivo...")
            time.sleep(5)
            
            tempo_decorrido = time.time() - tempo_inicio
            print(f"✅ Download concluído em {tempo_decorrido:.1f} segundos!")
            return True, arquivo, tempo_decorrido
        
        # Aguarda antes da próxima verificação
        time.sleep(intervalo_verificacao)
        tempo_decorrido = time.time() - tempo_inicio
        
        # Mostra progresso a cada 10 segundos
        if int(tempo_decorrido) % 10 == 0 and tempo_decorrido > 0:
            print(f"⏱️  Aguardando... {int(tempo_decorrido)}s / {timeout}s")
    
    # Timeout atingido
    print(f"⚠️  Timeout atingido ({timeout}s). Verificando se há arquivo disponível...")

    # Só aceita se o arquivo for NOVO (gerado depois do início da espera).
    # Antes, qualquer CSV antigo da pasta era aceito e podia ser renomeado
    # com a filial errada.
    arquivo_final = _csv_novo(diretorios, csvs_antes)

    if arquivo_final:
        print(f"📄 Arquivo novo encontrado (Excel não abriu): {arquivo_final}")
        return True, arquivo_final, timeout
    else:
        print("❌ Nenhum arquivo CSV novo encontrado após timeout")
        return False, None, timeout


def contar_linhas_de_dados(caminho):
    """
    Conta as linhas de dados de um CSV exportado do Protheus (desconsidera a
    linha com o nome da tabela, ex.: "SD3", e o cabeçalho das colunas).

    Returns:
        Quantidade de linhas de dados, ou None se não foi possível ler o arquivo.
    """
    try:
        with open(caminho, encoding='cp1252', errors='ignore') as f:
            linhas = [l for l in f if l.strip()]
        # o cabeçalho é a primeira linha com separador
        for i, linha in enumerate(linhas):
            if ';' in linha:
                return len(linhas) - i - 1
        return 0
    except Exception as e:
        print(f"Erro ao ler o arquivo {caminho}: {e}")
        return None


def fechar_excel():
    """Fecha todas as instâncias do Excel abertas"""
    try:
        fechou_algum = False
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and 'EXCEL.EXE' in proc.info['name'].upper():
                proc.kill()
                fechou_algum = True
        
        if fechou_algum:
            print("📊 Excel fechado com sucesso")
            time.sleep(4)  # Aguarda o processo finalizar
        return True
    except Exception as e:
        print(f"Erro ao fechar Excel: {e}")
        return False