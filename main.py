import time
import os
from modules.centro_de_custo import automation_centro_de_custo
from auth.login_manager import autenticar
from modules.calcular_competencia import calcular_competencia
from config.config_driver import setup_driver
from modules.clicar_botao_shadow_dom import clicar_botao_shadow_dom
from auth.fazer_login import fazer_login_selenium
from modules.clicar_botao_shadow_por_texto import clicar_botao_shadow_por_texto
from modules.clicar_botao_shadow_duplo_iframe import clicar_botao_shadow_duplo_iframe
from modules.tirar_screenshot import tirar_screenshot
from modules.clicar_menu_item_direto import clicar_menu_item_direto
from modules.abrir_aplicativo_webagent import abrir_aplicativo_webagent
from modules.fechar_aplicativo_webagent import fechar_aplicativo_webagent

if __name__ == "__main__":
    
    print("=" * 60)
    print("🚀 INICIANDO AUTOMAÇÃO SELENIUM - SHADOW DOM ANINHADO")
    print("=" * 60)
    
    # Carregar credenciais
    NOME_APP, EMAIL, SENHA, TITULO_JANELA = autenticar()

    URL_APP = os.getenv("URL_APP")

    CAMINHO_APP = os.getenv("CAMINHO_APP")
    
    driver = None
    
    # Tempo de espera para o app inicializar (em segundos)
    TEMPO_INICIALIZACAO = 10
    
    try:
        # PASSO 1: Abrir o aplicativo  em segundo plano
        if not abrir_aplicativo_webagent(CAMINHO_APP, timeout=TEMPO_INICIALIZACAO):
            raise Exception("Falha ao abrir aplicativo")
        
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

        print("\n🔍 DEBUG: Analisando estrutura Shadow DOM...")

        debug_script = """
            function analyzeAllShadows(root, level = 0, path = 'document') {
                let indent = '  '.repeat(level);
                let results = [];
                
                // Analisar elementos no nível atual
                let menuItems = root.querySelectorAll('wa-menu-item');
                if (menuItems.length > 0) {
                    results.push(indent + `📍 Encontrados ${menuItems.length} wa-menu-item em ${path}`);
                    menuItems.forEach((item, idx) => {
                        let caption = item.getAttribute('caption') || '';
                        let id = item.getAttribute('id') || '';
                        let text = item.textContent.trim().substring(0, 50);
                        results.push(indent + `  [${idx}] caption="${caption}" id="${id}" text="${text}"`);
                    });
                }
                
                // Buscar em todos os shadow roots
                let elements = root.querySelectorAll('*');
                for (let i = 0; i < elements.length; i++) {
                    let el = elements[i];
                    if (el.shadowRoot) {
                        let tagName = el.tagName.toLowerCase();
                        let elId = el.id ? `#${el.id}` : '';
                        results.push(indent + `🌑 Shadow encontrado: <${tagName}${elId}>`);
                        
                        // Recursão
                        let childResults = analyzeAllShadows(
                            el.shadowRoot, 
                            level + 1, 
                            `${path} > ${tagName}${elId} (shadow)`
                        );
                        results = results.concat(childResults);
                    }
                }
                
                return results;
            }
            
            return analyzeAllShadows(document).join('\\n');
        """

        resultado_debug = driver.execute_script(debug_script)
        print("\n📊 ESTRUTURA ENCONTRADA:")
        print(resultado_debug)
        print("\n" + "="*60)
            
        # Opção 1: Por ID (mais confiável)
        if clicar_menu_item_direto(driver, menu_id="COMP3072"):
            print("✅ Menu aberto!")
            time.sleep(2)

        # Opção 2: Por texto do caption (mais flexível)
        if clicar_menu_item_direto(driver, caption_texto="Relatorios"):
            print("✅ Menu aberto!")
            time.sleep(2)
        
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
            
        # Fechar o aplicativo
        fechar_aplicativo_webagent("web-agent-windows-x64.exe") 
    
    input("\nPressione Enter para finalizar...")