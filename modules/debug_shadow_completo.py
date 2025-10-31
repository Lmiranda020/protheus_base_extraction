def debug_estrutura_completa(driver):
    """
    Faz um debug completo da estrutura Shadow DOM, incluindo iframes
    """
    print("\n" + "="*80)
    print("🔍 DEBUG COMPLETO DA ESTRUTURA")
    print("="*80)
    
    script = """
        function debugCompleto() {
            let resultados = {
                shadowRoots: [],
                iframes: [],
                waInputs: [],
                elementosComId: []
            };
            
            function analisarElemento(root, caminho = 'document', nivel = 0) {
                if (nivel > 10) return;
                
                let indent = '  '.repeat(nivel);
                
                // 1. Buscar todos os elementos com ID que começam com 'COMP'
                let compElements = root.querySelectorAll('[id^="COMP"]');
                compElements.forEach(el => {
                    let info = {
                        id: el.id,
                        tagName: el.tagName.toLowerCase(),
                        caminho: caminho,
                        temShadow: !!el.shadowRoot,
                        atributos: {}
                    };
                    
                    ['label', 'placeholder', 'caption', 'type', 'value'].forEach(attr => {
                        if (el.hasAttribute(attr)) {
                            info.atributos[attr] = el.getAttribute(attr);
                        }
                    });
                    
                    resultados.elementosComId.push(info);
                });
                
                // 2. Buscar wa-input e wa-text-input
                let waInputs = root.querySelectorAll('wa-input, wa-text-input');
                waInputs.forEach(el => {
                    let info = {
                        id: el.id || 'sem-id',
                        tagName: el.tagName.toLowerCase(),
                        label: el.getAttribute('label') || '',
                        placeholder: el.getAttribute('placeholder') || '',
                        caminho: caminho,
                        temShadow: !!el.shadowRoot
                    };
                    
                    if (el.shadowRoot) {
                        let inputInterno = el.shadowRoot.querySelector('input, textarea');
                        if (inputInterno) {
                            info.inputInterno = {
                                type: inputInterno.type || inputInterno.tagName.toLowerCase(),
                                value: inputInterno.value || '',
                                placeholder: inputInterno.placeholder || ''
                            };
                        }
                    }
                    
                    resultados.waInputs.push(info);
                });
                
                // 3. Analisar iframes
                let iframes = root.querySelectorAll('iframe');
                iframes.forEach((iframe, idx) => {
                    let info = {
                        id: iframe.id || `iframe-${idx}`,
                        src: iframe.src || 'about:blank',
                        caminho: caminho,
                        acessivel: false
                    };
                    
                    try {
                        if (iframe.contentDocument) {
                            info.acessivel = true;
                            info.title = iframe.contentDocument.title;
                            analisarElemento(
                                iframe.contentDocument, 
                                caminho + ` > iframe#${info.id}`, 
                                nivel + 1
                            );
                        }
                    } catch (e) {
                        info.erro = e.toString();
                    }
                    
                    resultados.iframes.push(info);
                });
                
                // 4. Buscar em Shadow DOM
                let todosElementos = root.querySelectorAll('*');
                for (let el of todosElementos) {
                    if (el.shadowRoot) {
                        let tagName = el.tagName.toLowerCase();
                        let elId = el.id ? '#' + el.id : '';
                        
                        resultados.shadowRoots.push({
                            elemento: tagName + elId,
                            caminho: caminho
                        });
                        
                        analisarElemento(
                            el.shadowRoot, 
                            caminho + ` > ${tagName}${elId} (shadow)`, 
                            nivel + 1
                        );
                    }
                }
            }
            
            analisarElemento(document);
            return resultados;
        }
        
        return debugCompleto();
    """
    
    try:
        resultados = driver.execute_script(script)
        
        # Exibir Shadow Roots
        print("\n🌑 SHADOW ROOTS ENCONTRADOS:")
        if resultados['shadowRoots']:
            for sr in resultados['shadowRoots']:
                print(f"  • {sr['elemento']}")
                print(f"    📍 {sr['caminho']}")
        else:
            print("  ❌ Nenhum Shadow Root encontrado")
        
        # Exibir iframes
        print("\n🖼️  IFRAMES ENCONTRADOS:")
        if resultados['iframes']:
            for iframe in resultados['iframes']:
                print(f"  • {iframe['id']}")
                print(f"    📍 {iframe['caminho']}")
                print(f"    🔗 src: {iframe['src'][:80]}...")
                print(f"    ✓ Acessível: {iframe['acessivel']}")
                if 'title' in iframe:
                    print(f"    📄 Título: {iframe['title']}")
                if 'erro' in iframe:
                    print(f"    ❌ Erro: {iframe['erro']}")
        else:
            print("  ❌ Nenhum iframe encontrado")
        
        # Exibir wa-inputs
        print("\n📝 WA-INPUTS ENCONTRADOS:")
        if resultados['waInputs']:
            for inp in resultados['waInputs']:
                print(f"  • ID: {inp['id']} <{inp['tagName']}>")
                print(f"    Label: {inp['label']}")
                print(f"    Placeholder: {inp['placeholder']}")
                print(f"    📍 {inp['caminho']}")
                print(f"    Shadow: {inp['temShadow']}")
                if 'inputInterno' in inp:
                    print(f"    ➜ Input interno: {inp['inputInterno']['type']}")
                    print(f"      Valor: '{inp['inputInterno']['value']}'")
        else:
            print("  ❌ Nenhum wa-input encontrado")
        
        # Exibir elementos com ID COMP*
        print("\n🆔 ELEMENTOS COM ID 'COMP*':")
        if resultados['elementosComId']:
            comp4539_proximos = [
                el for el in resultados['elementosComId'] 
                if abs(int(el['id'].replace('COMP', '')) - 4539) < 20
            ]
            
            if comp4539_proximos:
                print("\n  📍 ELEMENTOS PRÓXIMOS A COMP4539:")
                for el in sorted(comp4539_proximos, key=lambda x: x['id']):
                    print(f"  • {el['id']} <{el['tagName']}>")
                    print(f"    📍 {el['caminho']}")
                    print(f"    Shadow: {el['temShadow']}")
                    if el['atributos']:
                        print(f"    Atributos: {el['atributos']}")
            
            comp4539 = next((el for el in resultados['elementosComId'] if el['id'] == 'COMP4539'), None)
            if comp4539:
                print("\n  🎯 ENCONTRADO COMP4539!")
                print(f"  • Tag: {comp4539['tagName']}")
                print(f"  • Caminho: {comp4539['caminho']}")
                print(f"  • Shadow: {comp4539['temShadow']}")
                print(f"  • Atributos: {comp4539['atributos']}")
            else:
                print("\n  ❌ COMP4539 NÃO ENCONTRADO!")
        else:
            print("  ❌ Nenhum elemento com ID 'COMP*' encontrado")
        
        print("\n" + "="*80)
        
        return resultados
        
    except Exception as e:
        print(f"\n❌ Erro no debug: {e}")
        import traceback
        traceback.print_exc()
        return None


def buscar_elemento_por_vizinhos(driver, texto_label_proximo):
    """
    Tenta encontrar um input baseado em um label ou texto próximo
    """
    print(f"\n🔍 Buscando input próximo ao texto '{texto_label_proximo}'...")
    
    script = f"""
        function buscarPorVizinho() {{
            function buscarEmRoot(root, caminho = 'document') {{
                let walker = document.createTreeWalker(
                    root,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );
                
                let results = [];
                let node;
                
                while (node = walker.nextNode()) {{
                    if (node.textContent.toLowerCase().includes('{texto_label_proximo}'.toLowerCase())) {{
                        let parent = node.parentElement;
                        
                        let inputs = [];
                        
                        if (parent.parentElement) {{
                            inputs = inputs.concat(
                                Array.from(parent.parentElement.querySelectorAll('input, textarea, wa-input, wa-text-input'))
                            );
                        }}
                        
                        results.push({{
                            texto: node.textContent.trim(),
                            caminho: caminho,
                            parentTag: parent.tagName.toLowerCase(),
                            parentId: parent.id || 'sem-id',
                            inputsProximos: inputs.map(inp => ({{
                                tag: inp.tagName.toLowerCase(),
                                id: inp.id || 'sem-id',
                                type: inp.type || 'N/A'
                            }}))
                        }});
                    }}
                }}
                
                let all = root.querySelectorAll('*');
                for (let el of all) {{
                    if (el.shadowRoot) {{
                        let tagName = el.tagName.toLowerCase();
                        let elId = el.id ? '#' + el.id : '';
                        results = results.concat(
                            buscarEmRoot(el.shadowRoot, caminho + ` > ${{tagName}}${{elId}} (shadow)`)
                        );
                    }}
                }}
                
                return results;
            }}
            
            return buscarEmRoot(document);
        }}
        
        return buscarPorVizinho();
    """
    
    try:
        resultados = driver.execute_script(script)
        
        if resultados:
            print(f"\n✅ Encontrados {len(resultados)} elementos com o texto:")
            for i, res in enumerate(resultados, 1):
                print(f"\n  [{i}] Texto: '{res['texto'][:50]}...'")
                print(f"      Parent: <{res['parentTag']}> id='{res['parentId']}'")
                print(f"      Caminho: {res['caminho']}")
                if res['inputsProximos']:
                    print(f"      Inputs próximos:")
                    for inp in res['inputsProximos']:
                        print(f"        • <{inp['tag']}> id='{inp['id']}' type='{inp['type']}'")
        else:
            print(f"❌ Nenhum elemento encontrado com o texto '{texto_label_proximo}'")
        
        return resultados
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None