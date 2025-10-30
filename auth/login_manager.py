from dotenv import load_dotenv
import os

load_dotenv()

# Carrega as variáveis do arquivo .env
def autenticar():
    NOME_APP = os.getenv("NOME_APP")
    EMAIL = os.getenv("EMAIL")
    SENHA = os.getenv("SENHA")
    TITULO_JANELA = os.getenv("TITULO_JANELA")
    
    return NOME_APP, EMAIL, SENHA, TITULO_JANELA

def url_sistema():

    URL_APP = os.getenv("URL_APP")
    
    return  URL_APP

