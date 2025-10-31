def clicar_input_shadow(driver, elemento_id, debug=True):
    """
    Clica e foca em um input dentro de Shadow DOM (wa-input ou wa-text-input)
    
    Args:
        driver: WebDriver do Selenium
        elemento_id: ID do elemento wa-input ou wa-text-input (deve ser uma STRING)
        debug: Se True, exibe informações de debug
    
    Returns:
        bool: True se conseguiu focar, False caso contrário
    """
    if not isinstance(elemento_id, str):
        print(f"❌ ERRO: elemento_id deve ser uma string, recebeu {type(elemento_id)}")
        raise TypeError(f"elemento_id deve ser string, não {type(elemento_id).__name__}")
    
    print(f"\n🔍 Procurando input Shadow DOM com ID '{elemento_id}'...")
    
    # ETAPA 1: Verificar se o elemento existe e qual é seu tipo
    if debug:
        debug_script = """
            function debugElement(elementId) {
                function findById(root, id, path = 'document') {
                    let el = root.querySelector('#' + id);
                    if (el) {
                        return {
                            found: true,
                            path: path,
                            tagName: el.tagName,
                            hasShadow: !!el.shadowRoot,
                            attributes: Array.from(el.attributes).map(a => `${a.name}="${a.value}"`).join(' ')
                        };
                    }
                    
                    let all = root.querySelectorAll('*');
                    for (let i = 0; i < all.length; i++) {
                        let item = all[i];
                        if (item.shadowRoot) {
                            let newPath = path + ' > ' + item.tagName.toLowerCase() + 
                                         (item.id ? '#' + item.id : '');
                            let found = findById(item.shadowRoot, id, newPath + ' (shadow)');
                            if (found.found) return found;
                        }
                    }
                    
                    return {found: false};
                }
                
                return findById(document, elementId);
            }
            
            return debugElement(arguments[0]);
        """
        
        try:
            debug_info = driver.execute_script(debug_script, elemento_id)
            if debug_info['found']:
                print(f"✅ Elemento encontrado!")
                print(f"   📍 Caminho: {debug_info['path']}")
                print(f"   🏷️  Tag: {debug_info['tagName']}")
                print(f"   🌑 Tem Shadow: {debug_info['hasShadow']}")
                print(f"   📋 Atributos: {debug_info['attributes']}")
            else:
                print(f"❌ Elemento '{elemento_id}' não encontrado no DOM!")
                return False
        except Exception as e:
            print(f"⚠️ Erro no debug: {e}")
    
    # ETAPA 2: Focar no input (suporta wa-input e wa-text-input)
    script = """
        function focarInput(elementId) {
            // Função recursiva para buscar em Shadow DOM
            function findById(root, id) {
                let el = root.querySelector('#' + id);
                if (el) return el;
                
                let all = root.querySelectorAll('*');
                for (let item of all) {
                    if (item.shadowRoot) {
                        let found = findById(item.shadowRoot, id);
                        if (found) return found;
                    }
                }
                return null;
            }
            
            // Buscar o elemento (wa-input ou wa-text-input)
            let waInput = findById(document, elementId);
            if (!waInput) {
                console.error('❌ Elemento não encontrado');
                return {success: false, error: 'elemento_nao_encontrado'};
            }
            
            if (!waInput.shadowRoot) {
                console.error('❌ Elemento não tem shadowRoot');
                return {success: false, error: 'sem_shadow_root'};
            }
            
            // Tentar encontrar o input de várias formas
            let input = null;
            
            // Método 1: Buscar input direto
            input = waInput.shadowRoot.querySelector('input');
            
            // Método 2: Buscar input em shadow aninhado
            if (!input) {
                let shadowEls = waInput.shadowRoot.querySelectorAll('*');
                for (let el of shadowEls) {
                    if (el.shadowRoot) {
                        input = el.shadowRoot.querySelector('input');
                        if (input) break;
                    }
                }
            }
            
            // Método 3: Buscar textarea
            if (!input) {
                input = waInput.shadowRoot.querySelector('textarea');
            }
            
            // Método 4: Buscar elemento editável
            if (!input) {
                input = waInput.shadowRoot.querySelector('[contenteditable="true"]');
            }
            
            if (!input) {
                console.error('❌ Input interno não encontrado');
                let children = Array.from(waInput.shadowRoot.querySelectorAll('*'))
                    .map(el => el.tagName.toLowerCase())
                    .slice(0, 10);
                return {
                    success: false, 
                    error: 'input_nao_encontrado',
                    children: children
                };
            }
            
            try {
                // Scroll até o elemento
                input.scrollIntoView({behavior: 'smooth', block: 'center'});
                
                // Remover atributos que impedem edição
                if (input.hasAttribute('readonly')) {
                    input.removeAttribute('readonly');
                }
                if (input.hasAttribute('disabled')) {
                    input.removeAttribute('disabled');
                }
                
                // Focar de múltiplas formas
                input.focus();
                input.click();
                
                // Disparar eventos
                input.dispatchEvent(new Event('focus', {bubbles: true}));
                input.dispatchEvent(new MouseEvent('click', {bubbles: true}));
                input.dispatchEvent(new Event('input', {bubbles: true}));
                
                console.log('✅ Input focado com sucesso');
                return {
                    success: true,
                    value: input.value || '',
                    type: input.type || input.tagName,
                    isDisabled: input.disabled,
                    isReadonly: input.readOnly
                };
            } catch (e) {
                console.error('❌ Erro ao focar:', e);
                return {success: false, error: 'erro_ao_focar', message: e.toString()};
            }
        }
        
        return focarInput(arguments[0]);
    """
    
    try:
        resultado = driver.execute_script(script, elemento_id)
        
        if resultado.get('success'):
            print(f"✅ Input '{elemento_id}' focado com sucesso!")
            if debug and resultado.get('value'):
                print(f"   📝 Valor atual: '{resultado['value']}'")
            if debug:
                print(f"   🔤 Tipo: {resultado.get('type', 'N/A')}")
            return True
        else:
            print(f"❌ Falha ao focar input: {resultado.get('error', 'erro_desconhecido')}")
            if 'children' in resultado:
                print(f"   📋 Elementos encontrados dentro do shadow: {resultado['children']}")
            if 'message' in resultado:
                print(f"   💬 Mensagem: {resultado['message']}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na execução: {e}")
        import traceback
        traceback.print_exc()
        return False


def preencher_input_shadow(driver, elemento_id, texto, limpar_antes=True):
    """
    Preenche um input dentro de Shadow DOM
    
    Args:
        driver: WebDriver do Selenium
        elemento_id: ID do elemento wa-text-input
        texto: Texto a ser inserido
        limpar_antes: Se True, limpa o campo antes de preencher
    
    Returns:
        bool: True se conseguiu preencher, False caso contrário
    """
    print(f"\n📝 Preenchendo input '{elemento_id}' com '{texto}'...")
    
    script = """
        function preencherInput(elementId, texto, limpar) {
            function findById(root, id) {
                let el = root.querySelector('#' + id);
                if (el) return el;
                
                let all = root.querySelectorAll('*');
                for (let item of all) {
                    if (item.shadowRoot) {
                        let found = findById(item.shadowRoot, id);
                        if (found) return found;
                    }
                }
                return null;
            }
            
            let waInput = findById(document, elementId);
            if (!waInput || !waInput.shadowRoot) {
                return {success: false, error: 'elemento_nao_encontrado'};
            }
            
            let input = waInput.shadowRoot.querySelector('input') || 
                       waInput.shadowRoot.querySelector('textarea');
            
            if (!input) {
                let shadowEls = waInput.shadowRoot.querySelectorAll('*');
                for (let el of shadowEls) {
                    if (el.shadowRoot) {
                        input = el.shadowRoot.querySelector('input, textarea');
                        if (input) break;
                    }
                }
            }
            
            if (!input) {
                return {success: false, error: 'input_nao_encontrado'};
            }
            
            try {
                // Focar
                input.focus();
                input.click();
                
                // Limpar se solicitado
                if (limpar) {
                    input.value = '';
                    input.dispatchEvent(new Event('input', {bubbles: true}));
                }
                
                // Preencher
                input.value = texto;
                
                // Disparar eventos
                input.dispatchEvent(new Event('input', {bubbles: true}));
                input.dispatchEvent(new Event('change', {bubbles: true}));
                input.dispatchEvent(new KeyboardEvent('keyup', {bubbles: true}));
                
                return {success: true, value: input.value};
            } catch (e) {
                return {success: false, error: 'erro_ao_preencher', message: e.toString()};
            }
        }
        
        return preencherInput(arguments[0], arguments[1], arguments[2]);
    """
    
    try:
        resultado = driver.execute_script(script, elemento_id, texto, limpar_antes)
        
        if resultado.get('success'):
            print(f"✅ Input preenchido com sucesso!")
            print(f"   📝 Valor final: '{resultado['value']}'")
            return True
        else:
            print(f"❌ Falha ao preencher: {resultado.get('error', 'erro_desconhecido')}")
            if 'message' in resultado:
                print(f"   💬 {resultado['message']}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

