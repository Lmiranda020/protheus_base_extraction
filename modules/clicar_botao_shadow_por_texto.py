import time

def clicar_botao_shadow_por_texto(driver, texto, seletor_interno='button', timeout=10):
    """
    Clica em um botão Shadow DOM buscando por texto visível
    
    Args:
        texto: Texto visível no botão (ex: 'OK', 'Entrar')
        seletor_interno: Seletor do elemento interno (padrão: 'button')
    
    Exemplo:
        clicar_botao_shadow_por_texto(driver, 'Ok')
    """
    try:
        print(f"🔍 Procurando botão Shadow DOM com texto '{texto}'...")
        
        script = f"""
            function findButtonByText(root, targetText) {{
                var elements = root.querySelectorAll('*');
                
                for (var i = 0; i < elements.length; i++) {{
                    var el = elements[i];
                    
                    if (el.shadowRoot) {{
                        var innerBtn = el.shadowRoot.querySelector('{seletor_interno}');
                        
                        if (innerBtn) {{
                            var text = innerBtn.textContent.trim();
                            if (text === targetText || text.includes(targetText)) {{
                                console.log('✓ Botão encontrado:', text);
                                innerBtn.click();
                                return true;
                            }}
                        }}
                        
                        // Buscar recursivamente
                        if (findButtonByText(el.shadowRoot, targetText)) {{
                            return true;
                        }}
                    }}
                }}
                return false;
            }}
            
            return findButtonByText(document, '{texto}');
        """
        
        resultado = driver.execute_script(script)
        
        if resultado:
            print(f"✅ Botão com texto '{texto}' clicado!")
            time.sleep(0.5)
            return True
        else:
            print(f"❌ Botão com texto '{texto}' não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao clicar por texto '{texto}': {e}")
        return False
    