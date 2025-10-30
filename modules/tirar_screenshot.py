def tirar_screenshot(driver, nome_arquivo="debug.png"):
    """Tira screenshot para debug"""
    driver.save_screenshot(nome_arquivo)
    print(f"📸 Screenshot salva: {nome_arquivo}")