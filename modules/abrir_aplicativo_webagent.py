import subprocess
import time
import psutil
import os

def abrir_aplicativo_webagent(caminho_app, timeout=30):
    """
    Abre o aplicativo WebAgent em segundo plano
    
    Args:
        caminho_app: Caminho completo do executável
        timeout: Tempo máximo para aguardar o app iniciar (segundos)
    
    Returns:
        bool: True se abriu com sucesso, False caso contrário
    """
    print("\n🚀 Abrindo aplicativo WebAgent...")
    
    try:
        # Verificar se o aplicativo já está rodando
        nome_processo = os.path.basename(caminho_app)
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == nome_processo:
                print(f"✅ Aplicativo já está rodando (PID: {proc.pid})")
                return True
        
        # Abrir o aplicativo em segundo plano
        # Use CREATE_NO_WINDOW no Windows para não mostrar janela
        if os.name == 'nt':  # Windows
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0  # SW_HIDE
            
            processo = subprocess.Popen(
                [caminho_app],
                startupinfo=startupinfo,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:  # Linux/Mac
            processo = subprocess.Popen(
                [caminho_app],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        print(f"✅ Aplicativo iniciado (PID: {processo.pid})")
        
        # Aguardar o app inicializar completamente
        print(f"⏳ Aguardando {timeout}s para o aplicativo inicializar...")
        time.sleep(timeout)
        
        # Verificar se o processo ainda está rodando
        if processo.poll() is None:
            print("✅ Aplicativo rodando em segundo plano!")
            return True
        else:
            print("❌ Aplicativo foi fechado inesperadamente")
            return False
            
    except FileNotFoundError:
        print(f"❌ Aplicativo não encontrado em: {caminho_app}")
        return False
    except Exception as e:
        print(f"❌ Erro ao abrir aplicativo: {e}")
        return False