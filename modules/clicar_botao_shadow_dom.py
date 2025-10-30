import time

def clicar_botao_shadow_dom(driver, atributo, valor, seletor_interno='button', timeout=10, descricao=None):
    """
    Função para clicar em botões dentro de Shadow DOM ANINHADO
    
    Args:
        driver: Instância do Selenium WebDriver
        atributo: Atributo do elemento host (ex: 'part', 'title', 'caption')
        valor: Valor do atributo (ex: 'btn-ok', 'Botão confirmar')
        seletor_interno: Seletor CSS do elemento interno (padrão: 'button')
        timeout: Tempo máximo de espera
        descricao: Descrição para logs
    
    Exemplos:
        clicar_botao_shadow_dom(driver, 'part', 'btn-ok')
        clicar_botao_shadow_dom(driver, 'caption', 'Ok')
        clicar_botao_shadow_dom(driver, 'title', 'Botão confirmar')
    """
    try:
        desc = descricao or f"{atributo}='{valor}'"
        print(f"🔍 Procurando botão Shadow DOM ({desc})...")
        
        time.sleep(1)
        
        # Script JavaScript que lida com Shadow DOM ANINHADO (recursivo)
        script = f"""
            // Função recursiva para buscar em shadow DOM aninhado
            function findInShadowDOM(root, attribute, value) {{
                // Buscar em todos os elementos do root atual
                var elements = root.querySelectorAll('*');
                
                for (var i = 0; i < elements.length; i++) {{
                    var el = elements[i];
                    
                    // Verificar se o elemento corresponde ao atributo
                    var attrValue = el.getAttribute(attribute);
                    if (attrValue === value || (attrValue && attrValue.includes(value))) {{
                        console.log('✓ Elemento encontrado:', el.tagName, attrValue);
                        return el;
                    }}
                    
                    // Se tem shadowRoot, buscar recursivamente DENTRO dele
                    if (el.shadowRoot) {{
                        var found = findInShadowDOM(el.shadowRoot, attribute, value);
                        if (found) return found;
                    }}
                }}
                
                return null;
            }}
            
            // Buscar em toda a página (incluindo shadows aninhados)
            var targetElement = findInShadowDOM(document, '{atributo}', '{valor}');
            
            if (!targetElement) {{
                console.error('❌ Elemento não encontrado');
                return {{success: false, found: false}};
            }}
            
            console.log('🎯 Elemento alvo encontrado:', targetElement.tagName);
            
            // Se o elemento tem shadowRoot, buscar o button interno
            if (targetElement.shadowRoot) {{
                var innerBtn = targetElement.shadowRoot.querySelector('{seletor_interno}');
                
                if (innerBtn) {{
                    console.log('✓ Botão interno encontrado, clicando...');
                    innerBtn.click();
                    return {{success: true, found: true, method: 'inner_button'}};
                }} else {{
                    console.log('⚠️ Botão interno não encontrado, clicando no host');
                    targetElement.click();
                    return {{success: true, found: true, method: 'host_click'}};
                }}
            }} else {{
                console.log('✓ Clicando diretamente no elemento');
                targetElement.click();
                return {{success: true, found: true, method: 'direct_click'}};
            }}
        """
        
        resultado = driver.execute_script(script)
        
        if resultado.get('success'):
            metodo = resultado.get('method', 'unknown')
            print(f"✅ Botão clicado! (método: {metodo}) - {desc}")
            time.sleep(0.5)
            return True
        else:
            print(f"❌ Botão não encontrado - {desc}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao clicar no botão Shadow DOM ({desc}): {e}")
        import traceback
        traceback.print_exc()
        return False
