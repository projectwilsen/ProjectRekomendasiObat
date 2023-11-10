from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import json

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
chrome_options = Options()
options = [
    # "--headless",
    f"--user-agent={user_agent}"
]
for option in options:
    chrome_options.add_argument(option)

url = "https://idx.co.id/primary/StockData/GetSecuritiesStock"

try:
    # run in GitHub action
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chrome_options)
    driver.get(url)
    print("driver based on ChromeType.CHROMIUM is working")
except:
    # run in local
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    print(f"driver is working")

all_text = driver.execute_script("return document.body.innerText")

data = json.loads(all_text)
active_company = [entry['Code'] for entry in data['data']]
print(active_company)

# Close the browser window
driver.quit()