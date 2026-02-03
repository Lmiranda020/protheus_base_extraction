import pyautogui
import time
import os
from dotenv import load_dotenv
from modules.clicar_imagem import clicar_imagem
from modules.centro_de_custo import automacao_centro_de_custo
from modules.calcular_competencia import calcular_competencia
from modules.consumo import automacao_consumo
from modules.conectar_vpn import conectar_vpn
from modules.abrir_app_agent import habilitar_app_agent

if __name__ == "__main__":

    # calcula a competencia
    competencia_anterior = calcular_competencia()

    conectar_vpn()

    # Carregar variáveis do arquivo .env
    load_dotenv()
    
    # carregar variáveis de ambiente
    try:
        NOME_APP = os.getenv("NOME_APP")
        USER = os.getenv("USER")
        SENHA = os.getenv("SENHA")
        
        # Verificar se as variáveis foram carregadas
        if not NOME_APP or not USER or not SENHA:
            print("Erro: Variáveis de ambiente não configuradas!")
            print(f"NOME_APP: {NOME_APP}")
            print(f"EMAIL: {USER}")
            print(f"SENHA: {'***' if SENHA else None}")
            exit(1)
            
        print("Variáveis carregadas com sucesso!")

    except Exception as e:
        print("Erro ao carregar variáveis de ambiente:", e)
        exit(1)

    # abrir o menu iniciar
    pyautogui.press('win')

    # digitar o nome do programa
    pyautogui.write(NOME_APP, interval=0.1) 

    # clicar entrar no programa
    pyautogui.press('enter')

    # aguardar o programa abrir
    time.sleep(10)

    # expandir a tel
    pyautogui.press('f11')

    # clicar entrar para configurar
    pyautogui.press('enter')

    time.sleep(8)

    habilitar_app_agent()

    # aguardar a tela de login carregar
    time.sleep(15)

    # selecionar o campo de email e limpar
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')
    pyautogui.press('backspace')

    # digitar o email
    pyautogui.write(USER.upper(), interval=0.1)

    # pressionar tab para ir para o campo de senha
    pyautogui.press('tab')

    # digitar a senha
    pyautogui.write(SENHA, interval=0.1)

    # pressionar enter para fazer login
    pyautogui.press('enter')

    # clicar no meio da tela para garantir o foco
    time.sleep(5)
    pyautogui.click(x=100, y=200)

    # rolar até o final da página de login
    time.sleep(5)   
    pyautogui.press('end')

    # clicar no botão "Confirmar"
    time.sleep(2)
    if not clicar_imagem("data/botao_entrar.png", confidence=0.8, timeout=15, descricao="Botão entrar"):
        print("Erro ao clicar no botão entrar.")
        exit(1)
    
    time.sleep(3)

    # inicia a execução da automação de consumo
    automacao_consumo(competencia_anterior)

    # inicia a execução da automação de centro de custo
    # automacao_centro_de_custo(competencia_anterior)

    # fechar o app, final da automação
    print("Automação concluída com sucesso!")

    # fazer logouf
    pyautogui.keyDown('ctrl')
    pyautogui.press('q')
    pyautogui.keyUp('ctrl')
    time.sleep(1)

    #pressiona finalizar
    if not clicar_imagem("data/botao_finalizar.png", confidence=0.8, timeout=15, descricao="Botão Finalizar"):
        print("Erro ao clicar no botão finalizar.")

    # minimizar a tela
    pyautogui.press('f11')


    # Fecha a janela
    pyautogui.keyDown('alt')
    pyautogui.press('f4')
    pyautogui.keyUp('alt')

    # encerra o script
    exit(0)
