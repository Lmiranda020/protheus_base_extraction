import psutil

def fechar_aplicativo_protheus(nome_processo="web-agent-windows-x64.exe"):
    """
    Fecha o aplicativo ao final da automação
    """
    print(f"\n🔚 Fechando aplicativo {nome_processo}...")
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == nome_processo:
                proc.kill()
                print(f"✅ Aplicativo fechado (PID: {proc.pid})")
                return True
        print("⚠️ Aplicativo não encontrado rodando")
        return False
    except Exception as e:
        print(f"❌ Erro ao fechar aplicativo: {e}")
        return False