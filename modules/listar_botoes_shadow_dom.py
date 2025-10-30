def listar_botoes_shadow_dom(driver):
    """
    Função de DEBUG: Lista TODOS os web components com shadow DOM (inclusive aninhados)
    
    USO:
        listar_botoes_shadow_dom(driver)
    """
    script = """
        var components = [];
        
        function exploreShadowDOM(root, depth) {
            var elements = root.querySelectorAll('*');
            
            for (var i = 0; i < elements.length; i++) {
                var el = elements[i];
                
                if (el.shadowRoot) {
                    var info = {
                        tagName: el.tagName.toLowerCase(),
                        id: el.id || null,
                        part: el.getAttribute('part') || null,
                        title: el.getAttribute('title') || null,
                        caption: el.getAttribute('caption') || null,
                        class: el.className || null,
                        innerText: null,
                        depth: depth
                    };
                    
                    var innerBtn = el.shadowRoot.querySelector('button');
                    if (innerBtn) {
                        info.innerText = innerBtn.textContent.trim();
                    }
                    
                    components.push(info);
                    
                    // Explorar recursivamente
                    exploreShadowDOM(el.shadowRoot, depth + 1);
                }
            }
        }
        
        exploreShadowDOM(document, 0);
        return components;
    """
    
    try:
        componentes = driver.execute_script(script)
        
        print("\n" + "=" * 80)
        print("🔍 WEB COMPONENTS COM SHADOW DOM (INCLUINDO ANINHADOS):")
        print("=" * 80)
        
        if not componentes:
            print("⚠️ Nenhum componente encontrado!")
            return []
        
        for idx, comp in enumerate(componentes, 1):
            indent = "  " * comp.get('depth', 0)
            print(f"\n{idx}. {indent}<{comp['tagName']}>")
            
            if comp.get('depth', 0) > 0:
                print(f"{indent}   🔗 Nível: {comp['depth']} (aninhado)")
            if comp['id']:
                print(f"{indent}   📌 id: '{comp['id']}'")
            if comp['part']:
                print(f"{indent}   🏷️  part: '{comp['part']}'")
            if comp['title']:
                print(f"{indent}   📋 title: '{comp['title']}'")
            if comp['caption']:
                print(f"{indent}   💬 caption: '{comp['caption']}'")
            if comp['innerText']:
                print(f"{indent}   📝 texto: '{comp['innerText']}'")
            
            print(f"\n{indent}   💡 Como usar:")
            if comp['part']:
                print(f"{indent}      clicar_botao_shadow_dom(driver, 'part', '{comp['part']}')")
            if comp['caption']:
                print(f"{indent}      clicar_botao_shadow_dom(driver, 'caption', '{comp['caption']}')")
            if comp['innerText']:
                print(f"{indent}      clicar_botao_shadow_por_texto(driver, '{comp['innerText']}')")
        
        print("\n" + "=" * 80)
        return componentes
        
    except Exception as e:
        print(f"❌ Erro ao listar componentes: {e}")
        return []