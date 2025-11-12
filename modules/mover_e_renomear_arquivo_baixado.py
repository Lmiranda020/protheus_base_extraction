import os
import shutil
from pathlib import Path

def obter_arquivo_mais_recente(diretorio, extensao='.csv'):
    """Retorna o arquivo mais recente com a extensão especificada"""
    try:
        arquivos = [os.path.join(diretorio, f) for f in os.listdir(diretorio) 
                   if f.endswith(extensao)]
        if not arquivos:
            return None
        arquivo_mais_recente = max(arquivos, key=os.path.getctime)
        return arquivo_mais_recente
    except Exception as e:
        print(f"Erro ao buscar arquivo: {e}")
        return None

def mover_e_renomear_csv(filial, competencia, diretorio_destino):
    """
    Move o arquivo CSV mais recente e renomeia
    
    Args:
        filial: código da filial
        competencia: competência no formato DD/MM/YYYY
        diretorio_destino: caminho do diretório de destino
    
    Returns:
        bool: True se sucesso, False se erro
    """
    diretorio_temp = os.getenv("DIRETORIO_TEMP")
    
    if not diretorio_temp:
        print("❌ Erro: variável de ambiente DIRETORIO_TEMP não configurada")
        return False
    
    # Busca o arquivo mais recente
    print("🔍 Buscando arquivo CSV mais recente...")
    arquivo_origem = obter_arquivo_mais_recente(diretorio_temp, '.csv')
    
    if not arquivo_origem:
        print("❌ Nenhum arquivo CSV encontrado no diretório temporário")
        return False
    
    print(f"📄 Arquivo encontrado: {os.path.basename(arquivo_origem)}")
    
    # Cria o diretório de destino se não existir
    try:
        Path(diretorio_destino).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"❌ Erro ao criar diretório de destino: {e}")
        return False
    
    # Define o novo nome do arquivo
    competencia_formatada = competencia.replace('/', '-')
    novo_nome = f"Consumo_{filial}_{competencia_formatada}.csv"
    caminho_destino = os.path.join(diretorio_destino, novo_nome)
    
    # Move e renomeia o arquivo
    try:
        shutil.move(arquivo_origem, caminho_destino)
        print(f"✅ Arquivo movido e renomeado com sucesso!")
        print(f"📁 Destino: {caminho_destino}")
        return True
    except Exception as e:
        print(f"❌ Erro ao mover arquivo: {e}")
        return False