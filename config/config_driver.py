from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def setup_driver(headless=False):
    """Configura o driver do Selenium com opções básicas e compatíveis"""
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

    driver = webdriver.Chrome(options=chrome_options)
    return driver
