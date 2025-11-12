import os
import time
import psutil
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
                   if f.endswith(extensao)]
        if not arquivos:
            return None, None
        arquivo_mais_recente = max(arquivos, key=os.path.getctime)
        timestamp = os.path.getctime(arquivo_mais_recente)
        return arquivo_mais_recente, timestamp
    except Exception as e:
        print(f"Erro ao buscar arquivo: {e}")
        return None, None

def aguardar_download_completo(diretorio_temp, timeout=200, intervalo_verificacao=2):
    """
    Aguarda o download ser concluído monitorando:
    1. Criação de novo arquivo CSV
    2. Abertura automática do Excel
    
    Args:
        diretorio_temp: diretório onde os arquivos são baixados
        timeout: tempo máximo de espera em segundos (padrão: 200s)
        intervalo_verificacao: intervalo entre verificações em segundos (padrão: 2s)
    
    Returns:
        tuple: (sucesso, arquivo_path, tempo_decorrido)
    """
    print("🔍 Monitorando download...")
    
    # Registra o arquivo CSV mais recente ANTES do download
    arquivo_anterior, timestamp_anterior = obter_arquivo_mais_recente(diretorio_temp, '.csv')
    
    tempo_inicio = time.time()
    tempo_decorrido = 0
    excel_detectado = False
    
    while tempo_decorrido < timeout:
        # Verifica se um novo arquivo CSV foi criado
        arquivo_atual, timestamp_atual = obter_arquivo_mais_recente(diretorio_temp, '.csv')
        
        # Condição 1: Novo arquivo CSV detectado
        novo_arquivo_detectado = False
        if arquivo_atual and (arquivo_atual != arquivo_anterior or 
                             (timestamp_atual and timestamp_anterior and timestamp_atual > timestamp_anterior)):
            novo_arquivo_detectado = True
            print(f"✅ Novo arquivo detectado: {os.path.basename(arquivo_atual)}")
        
        # Condição 2: Excel foi aberto automaticamente
        if not excel_detectado and verificar_excel_aberto():
            excel_detectado = True
            print("✅ Excel detectado aberto (download em progresso/concluído)")
        
        # Se ambas condições forem atendidas, considera download completo
        if novo_arquivo_detectado and excel_detectado:
            # Aguarda mais um pouco para garantir que o arquivo está completo
            print("⏳ Aguardando estabilização do arquivo...")
            time.sleep(5)
            
            tempo_decorrido = time.time() - tempo_inicio
            print(f"✅ Download concluído em {tempo_decorrido:.1f} segundos!")
            return True, arquivo_atual, tempo_decorrido
        
        # Aguarda antes da próxima verificação
        time.sleep(intervalo_verificacao)
        tempo_decorrido = time.time() - tempo_inicio
        
        # Mostra progresso a cada 10 segundos
        if int(tempo_decorrido) % 10 == 0 and tempo_decorrido > 0:
            print(f"⏱️  Aguardando... {int(tempo_decorrido)}s / {timeout}s")
    
    # Timeout atingido
    print(f"⚠️  Timeout atingido ({timeout}s). Verificando se há arquivo disponível...")
    arquivo_final, _ = obter_arquivo_mais_recente(diretorio_temp, '.csv')
    
    if arquivo_final:
        print(f"📄 Arquivo encontrado (pode estar incompleto): {os.path.basename(arquivo_final)}")
        return True, arquivo_final, timeout
    else:
        print("❌ Nenhum arquivo CSV encontrado após timeout")
        return False, None, timeout


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