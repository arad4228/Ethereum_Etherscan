from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://etherscan.io/directory/Exchanges?q=&p=1"
driver.get(url)
cex_list = []

while True:
    wait = WebDriverWait(driver, 5)
    try:
        btn_next = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@aria-label='Next']"))
        )
    except TimeoutException:
        # "Next" 버튼이 없으면 루프 종료
        print("Last page reached or 'Next' button not found.")
        break

    EtherScan_html = driver.page_source
    EtherScan_soup = bs(EtherScan_html, 'html.parser')

    data_list = EtherScan_soup.find_all('a', class_='fs-5 link-dark')
    for data in data_list:
        cex = data.get_text(strip=True)
        cex_list.append(cex)
    
    time.sleep(3)
    btn_next.click()

df = pd.DataFrame({"Cex's Name": cex_list})
df.to_csv('cex_list.csv', encoding='UTF-8')