import time
from modules.centro_de_custo import automation_centro_de_custo
from auth.login_manager import autenticar, url_sistema
from modules.calcular_competencia import calcular_competencia
from config.config_driver import setup_driver
from modules.clicar_botao_shadow_dom import clicar_botao_shadow_dom
from auth.fazer_login import fazer_login_selenium
from modules.clicar_botao_shadow_por_texto import clicar_botao_shadow_por_texto
from modules.clicar_botao_shadow_duplo_iframe import clicar_botao_shadow_duplo_iframe
from modules.tirar_screenshot import tirar_screenshot

if __name__ == "__main__":
    
    print("=" * 60)
    print("🚀 INICIANDO AUTOMAÇÃO SELENIUM - SHADOW DOM ANINHADO")
    print("=" * 60)
    
    # Carregar credenciais
    NOME_APP, EMAIL, SENHA, TITULO_JANELA = autenticar()

    URL_APP = url_sistema()
    
    driver = None
    
    try:
        # 1. Configurar driver
        print("⚙️ Configurando driver...")
        driver = setup_driver(headless=False)  # False para ver o que está acontecendo
        
        # 2. Navegar para a aplicação
        driver.get(URL_APP)
        time.sleep(3)
        
        # # 3. DEBUG: Listar todos os botões Shadow DOM (DESCOMENTE PARA DEBUG)
        # print("\n🔍 Listando todos os componentes Shadow DOM...")
        # listar_botoes_shadow_dom(driver)
        
        # 4. Clicar no botão OK no Shadow DOM aninhado (ANTES do login)
        print("\n🔘 Clicando no botão OK (Shadow DOM aninhado)...")
        
        # Método 1: Por atributo 'part'
        if clicar_botao_shadow_dom(driver, 'part', 'btn-ok', descricao="Botão OK via part"):
            time.sleep(2)
        # Método 2: Por caption
        elif clicar_botao_shadow_dom(driver, 'caption', 'Ok', descricao="Botão OK via caption"):
            time.sleep(2)
        # Método 3: Por texto visível
        elif clicar_botao_shadow_por_texto(driver, 'Ok'):
            time.sleep(2)
        else:
            print("⚠️ Botão OK não encontrado, continuando...")
            # se n'ao encontrar parar o processo
            raise Exception("Botão OK não encontrado")
    
        time.sleep(5)
        
        # 5. Fazer login
        if not fazer_login_selenium(driver, EMAIL, SENHA, URL_APP):
            raise Exception("Falha no login")
        
        # 6. Aguardar página carregar
        time.sleep(3)

        # 7. Calcular competência
        competencia = calcular_competencia()
        print(f"📅 Competência: {competencia}")

        # 8. Aguardar webview e iframe carregarem
        print("\n⏳ Aguardando webview e iframe carregarem...")
        time.sleep(5)  # IMPORTANTE: dar tempo para o iframe renderizar

        # 9. Clicar no botão Entrar (Shadow duplo + iframe)
        print("\n🔘 Clicando no botão Entrar...")

        if clicar_botao_shadow_duplo_iframe(driver, webview_id='COMP3010', texto_botao='Entrar'):
            print("✓ Processo concluído! Avançando para próxima etapa...")
            time.sleep(3)
        else:
            print("\n⚠️ BOTÃO NÃO ENCONTRADO!")
            print("📸 Tirando screenshot para debug...")
            tirar_screenshot(driver, "erro_botao_entrar.png")
            
            # Tentar listar o que tem no iframe
            print("\n🔍 Listando conteúdo do iframe para debug...")
            debug_script = """
                var webview = document.getElementById('COMP3010');
                if (!webview || !webview.shadowRoot) return {error: 'webview não encontrado'};
                
                var iframe = webview.shadowRoot.querySelector('iframe');
                if (!iframe) {
                    // Tentar em shadow aninhado
                    var els = webview.shadowRoot.querySelectorAll('*');
                    for (var i = 0; i < els.length; i++) {
                        if (els[i].shadowRoot) {
                            iframe = els[i].shadowRoot.querySelector('iframe');
                            if (iframe) break;
                        }
                    }
                }
                
                if (!iframe) return {error: 'iframe não encontrado'};
                
                var doc = iframe.contentDocument;
                if (!doc) return {error: 'documento inacessível'};
                
                return {
                    title: doc.title,
                    buttons: Array.from(doc.querySelectorAll('button')).map(b => b.textContent.trim()),
                    inputs: Array.from(doc.querySelectorAll('input[type="submit"], input[type="button"]')).map(i => i.value)
                };
            """
            
            info = driver.execute_script(debug_script)
            print(f"📄 Info do iframe: {info}")
            
            raise Exception("Botão Entrar não encontrado")
        
        # 10. Chamar automação de centro de custo
        print("🏢 Iniciando automação de centro de custo...")
        automation_centro_de_custo(competencia, driver=driver)
        
        print("\n" + "=" * 60)
        print("✅ AUTOMAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⚠️ Automação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        
        if driver:
            tirar_screenshot(driver, "erro_screenshot.png")
    
    finally:
        if driver:
            print("\n🔚 Fechando driver...")
            driver.quit()
    
    input("\nPressione Enter para finalizar...")