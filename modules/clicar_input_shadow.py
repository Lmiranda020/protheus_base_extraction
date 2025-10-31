def clicar_input_shadow(driver, elemento_id):
    """
    Clica e foca em um input dentro de Shadow DOM
    """
    script = f"""
        function focarInput() {{
            function findById(root, id) {{
                let el = root.querySelector('#{id}');
                if (el) return el;
                
                let all = root.querySelectorAll('*');
                for (let item of all) {{
                    if (item.shadowRoot) {{
                        let found = findById(item.shadowRoot, id);
                        if (found) return found;
                    }}
                }}
                return null;
            }}
            
            let waInput = findById(document, '{elemento_id}');
            if (!waInput || !waInput.shadowRoot) {{
                console.log('❌ Elemento não encontrado');
                return false;
            }}
            
            let input = waInput.shadowRoot.querySelector('input');
            if (!input) {{
                console.log('❌ Input interno não encontrado');
                return false;
            }}
            
            // Clicar e focar no input
            input.click();
            input.focus();
            
            console.log('✅ Input focado');
            return true;
        }}
        
        return focarInput();
    """
    
    try:
        if driver.execute_script(script):
            print(f"✅ Input '{elemento_id}' focado!")
            return True
        else:
            print(f"❌ Falha ao focar input")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False