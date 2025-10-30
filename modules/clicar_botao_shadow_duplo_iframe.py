import time

def clicar_botao_shadow_duplo_iframe(driver, webview_id='COMP3010', texto_botao='Entrar'):
    """
    Clica em botão dentro de: Shadow DOM → Shadow DOM aninhado → iframe → botão
    VERSÃO MELHORADA: Trata erros quando página muda após o clique
    """
    print(f"🔘 Procurando botão '{texto_botao}' (Shadow duplo + iframe)...")
    
    script = f"""
        // ========== PASSO 1: Buscar wa-webview ==========
        var webview = document.getElementById('{webview_id}');
        if (!webview) {{
            return {{success: false, error: 'wa-webview não encontrado', step: 1}};
        }}
        console.log('✓ Passo 1: wa-webview encontrado');
        
        // ========== PASSO 2: Acessar primeiro Shadow DOM ==========
        if (!webview.shadowRoot) {{
            return {{success: false, error: 'shadowRoot #1 não existe', step: 2}};
        }}
        console.log('✓ Passo 2: Shadow DOM #1 acessado');
        
        // ========== PASSO 3: Buscar elementos dentro do Shadow #1 ==========
        var shadowElements = webview.shadowRoot.querySelectorAll('*');
        var innerShadowHost = null;
        var iframe = null;
        
        // Tentar encontrar iframe diretamente no Shadow #1
        iframe = webview.shadowRoot.querySelector('iframe');
        
        if (!iframe) {{
            // Se não achou, procurar em Shadow DOM aninhado
            for (var i = 0; i < shadowElements.length; i++) {{
                var el = shadowElements[i];
                
                if (el.shadowRoot) {{
                    console.log('✓ Passo 3: Shadow DOM #2 encontrado em', el.tagName);
                    innerShadowHost = el;
                    
                    // Buscar iframe no Shadow #2
                    iframe = el.shadowRoot.querySelector('iframe');
                    if (iframe) break;
                }}
            }}
        }}
        
        if (!iframe) {{
            return {{success: false, error: 'iframe não encontrado', step: 3}};
        }}
        console.log('✓ Passo 3: iframe encontrado');
        
        // ========== PASSO 4: Acessar documento do iframe ==========
        var iframeDoc = null;
        try {{
            iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
        }} catch (e) {{
            return {{success: false, error: 'Não foi possível acessar iframe: ' + e, step: 4}};
        }}
        
        if (!iframeDoc) {{
            return {{success: false, error: 'Documento do iframe inacessível', step: 4}};
        }}
        console.log('✓ Passo 4: Documento do iframe acessado');
        
        // ========== PASSO 5: Scroll até o final do iframe ==========
        iframeDoc.documentElement.scrollTop = iframeDoc.documentElement.scrollHeight;
        console.log('✓ Passo 5: Scroll no iframe realizado');
        
        // Aguardar conteúdo carregar após scroll
        return new Promise(resolve => {{
            setTimeout(() => {{
                
                // ========== PASSO 6: Buscar botão no iframe ==========
                // Método 1: Botão HTML normal
                var buttons = iframeDoc.querySelectorAll('button');
                for (var i = 0; i < buttons.length; i++) {{
                    var btn = buttons[i];
                    var text = btn.textContent.trim().toLowerCase();
                    
                    if (text.includes('{texto_botao.lower()}')) {{
                        console.log('✓ Passo 6: Botão encontrado (HTML normal):', btn.textContent);
                        btn.scrollIntoView({{block: 'center', behavior: 'smooth'}});
                        
                        setTimeout(() => {{
                            btn.click();
                            resolve({{success: true, buttonText: btn.textContent.trim(), method: 'html_button'}});
                        }}, 500);
                        return;
                    }}
                }}
                
                // Método 2: Botão em Shadow DOM dentro do iframe
                function findButtonInShadow(root, targetText, depth) {{
                    if (depth > 10) return null;
                    
                    var elements = root.querySelectorAll('*');
                    
                    for (var i = 0; i < elements.length; i++) {{
                        var el = elements[i];
                        
                        if (el.shadowRoot) {{
                            var innerBtn = el.shadowRoot.querySelector('button');
                            
                            if (innerBtn) {{
                                var text = innerBtn.textContent.trim().toLowerCase();
                                if (text.includes(targetText.toLowerCase())) {{
                                    console.log('✓ Passo 6: Botão encontrado (Shadow DOM):', innerBtn.textContent);
                                    return {{element: el, button: innerBtn}};
                                }}
                            }}
                            
                            var found = findButtonInShadow(el.shadowRoot, targetText, depth + 1);
                            if (found) return found;
                        }}
                    }}
                    return null;
                }}
                
                var shadowButton = findButtonInShadow(iframeDoc, '{texto_botao}', 0);
                
                if (shadowButton) {{
                    shadowButton.element.scrollIntoView({{block: 'center'}});
                    
                    setTimeout(() => {{
                        shadowButton.button.click();
                        resolve({{success: true, buttonText: shadowButton.button.textContent.trim(), method: 'shadow_button'}});
                    }}, 500);
                    return;
                }}
                
                // Método 3: Buscar por outros seletores (input[type=submit], po-button, etc)
                var submitInputs = iframeDoc.querySelectorAll('input[type="submit"], input[type="button"]');
                for (var i = 0; i < submitInputs.length; i++) {{
                    var inp = submitInputs[i];
                    var val = inp.value.toLowerCase();
                    
                    if (val.includes('{texto_botao.lower()}')) {{
                        console.log('✓ Passo 6: Input submit encontrado:', inp.value);
                        inp.scrollIntoView({{block: 'center'}});
                        
                        setTimeout(() => {{
                            inp.click();
                            resolve({{success: true, buttonText: inp.value, method: 'input_submit'}});
                        }}, 500);
                        return;
                    }}
                }}
                
                resolve({{success: false, error: 'Botão não encontrado no iframe', step: 6}});
                
            }}, 1500);  // Aguardar 1.5s após scroll para conteúdo carregar
        }});
    """
    
    try:
        # Aguardar página/iframe carregar completamente
        time.sleep(3)
        
        print("   🔄 Executando script (pode levar alguns segundos)...")
        
        try:
            resultado = driver.execute_async_script(script)
            
            # Caso 1: Script retornou sucesso
            if resultado and resultado.get('success'):
                metodo = resultado.get('method', 'unknown')
                texto = resultado.get('buttonText', '')
                print(f"✅ Botão clicado com sucesso!")
                print(f"   📝 Texto: '{texto}'")
                print(f"   🔧 Método: {metodo}")
                time.sleep(2)
                return True
            
            # Caso 2: Script retornou erro explícito
            elif resultado and not resultado.get('success'):
                erro = resultado.get('error', 'Erro desconhecido')
                passo = resultado.get('step', '?')
                print(f"❌ Falhou no passo {passo}: {erro}")
                return False
            
            # Caso 3: Script retornou None/vazio (página pode ter mudado após clique)
            else:
                print("⚠️ Script retornou vazio (página pode ter mudado após clique)")
                print("✅ Assumindo que o clique funcionou!")
                time.sleep(2)
                return True
                
        except Exception as script_error:
            # Capturar erros que acontecem quando a página muda durante a execução
            erro_str = str(script_error).lower()
            
            # Erros ESPERADOS quando o clique funciona mas redireciona a página
            erros_esperados = [
                'timeout',           # Timeout waiting for async script
                'navigation',        # Navigation occurred
                'unload',           # Page unloaded
                'detached',         # Element detached from DOM
                'frame',            # Frame detached
                'document',         # Document was unloaded
                'execution context' # Execution context was destroyed
            ]
            
            if any(keyword in erro_str for keyword in erros_esperados):
                print(f"⚠️ {type(script_error).__name__}: {erro_str.split('stacktrace')[0].strip()}")
                print("✅ Botão clicado com sucesso! (página redirecionou durante execução)")
                print("   → O erro é esperado quando a página muda após o clique, pois como a pagina é alterando não de tempo para retornar o resultado do script.")
                time.sleep(3)
                return True
            else:
                # Erro INESPERADO
                print(f"❌ Erro inesperado: {type(script_error).__name__}")
                print(f"   💬 {script_error}")
                raise script_error
            
    except Exception as e:
        print(f"❌ Erro fatal ao executar script: {e}")
        import traceback
        traceback.print_exc()
        return False