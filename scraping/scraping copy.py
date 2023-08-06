# %%
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import time
import json
import os
import pandas as pd
from datetime import date as dt

# %%
download =  os.getcwd() + "\data\empower_input"
print(download)

print("Hello")
print(os.getcwd())
print(os.listdir())
# %%
# add options
chrome_options = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--user-data-dir=C:/Users/Phan/Downloads/Github/automate-personal-finance/scraping/UserData")
# chrome_options.add_argument("--headless=chrome")
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument('--disable-dev-shm-usage')   
chrome_options.add_argument('--remote-debugging-port=9222')


# open driver
driver = webdriver.Chrome(service=Service(),options=chrome_options)

driver.get("https://home.personalcapital.com/page/login/goHome")
with open("./scraping/cookies.txt", "r") as f:
    cookies = eval(f.read())

for cookie in cookies:
    driver.add_cookie(cookie)
driver.implicitly_wait(20)


params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download}}
driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
driver.execute("send_command", params)

time.sleep(5)

# %%
#read json file for credentials
f= open('./scraping/credentials.json')
data = json.load(f)
username = data['username']
password = data['password']

try:  
    input = driver.find_element(By.NAME,"username")
    input.send_keys(username)
    input.send_keys(Keys.RETURN)
except:
    pass

try:
    input = driver.find_element(By.NAME,"passwd")
    input.send_keys(password)
    input.send_keys(Keys.RETURN)
except:
    pass
    
time.sleep(30)

# %%
driver.get("https://home.personalcapital.com/page/login/app#/net-worth")
time.sleep(10)

driver.get_screenshot_as_file("./scraping/screenshot.png")

# find investment account and their balance from Net Worth page of Empower
data = []
for i in driver.find_element(By.ID,"allTable_wrapper").find_elements(By.XPATH,"//tr[@data-group='-1-investment']"):
    acc = i.find_element(By.CLASS_NAME,"pc-datagrid__row-description").text
    amt = i.find_element(By.CLASS_NAME,"tabular-numbers").text.replace('$',"").replace(',',"")
    data.append([acc,amt,dt.today()])

# add their values to a dataframe for later use
df = pd.DataFrame(data, columns = ['Account', 'Balance', 'Last Updated'])
df["Balance"] = pd.to_numeric(df["Balance"])
df.to_csv('./data/other_input/investment_balance.csv',encoding='utf-8', index=False)

# %%
driver.get("https://home.personalcapital.com/page/login/app#/all-transactions")
time.sleep(10)

driver.find_element(By.XPATH,"//button[@class='pc-btn pc-btn--tiny qa-export-csv-btn']").click()
time.sleep(5)

cookies = driver.get_cookies()
with open("./scraping/cookies.txt", "w") as f:
    f.write(str(cookies))

# %%
driver.quit()

