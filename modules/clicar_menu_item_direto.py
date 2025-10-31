def clicar_menu_item_direto(driver, caption_texto=None, menu_id=None):
    """
    Clica em wa-menu-item que está diretamente no document (não em Shadow DOM)
    
    Args:
        driver: WebDriver do Selenium
        caption_texto: Texto do caption (ex: "Relatórios")
        menu_id: ID do elemento (ex: "COMP3072")
    
    Returns:
        bool: True se clicou, False caso contrário
    """
    try:
        if menu_id:
            print(f"🔍 Procurando menu por ID: {menu_id}")
            script = f"""
                let item = document.querySelector('wa-menu-item#{menu_id}');
                if (item) {{
                    item.click();
                    return true;
                }}
                return false;
            """
        elif caption_texto:
            print(f"🔍 Procurando menu por caption: {caption_texto}")
            script = f"""
                let items = document.querySelectorAll('wa-menu-item');
                for (let item of items) {{
                    let caption = item.getAttribute('caption') || '';
                    if (caption.includes('{caption_texto}')) {{
                        item.click();
                        return true;
                    }}
                }}
                return false;
            """
        else:
            print("❌ Precisa informar caption_texto ou menu_id")
            return False
        
        resultado = driver.execute_script(script)
        
        if resultado:
            print(f"✅ Menu clicado com sucesso!")
            return True
        else:
            print(f"❌ Menu não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao clicar no menu: {e}")
        return False