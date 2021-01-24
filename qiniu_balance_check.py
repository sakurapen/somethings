"""
七牛 SDK 接口未提供財務相關查詢
測試後發現必須 cookie 參數為 PORTAL_SESSION
此參數在登入當下的 set-cookie 未提供
須下載與主機 Chrome 版本一致的 chromedriver 與腳本一同放置
https://sites.google.com/a/chromium.org/chromedriver/downloads
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def qiniu_balance_check():
    options = Options()
    options.add_argument("--disable-notifications")

    chrome = webdriver.Chrome('./chromedriver', options=options)
    chrome.get("https://portal.qiniu.com/financial/overview")

    time.sleep(30)

    email = chrome.find_element_by_id("email")
    password = chrome.find_element_by_id("password")
    login = chrome.find_element_by_xpath("//button[@id='login-button']")

    email.send_keys('qiniu_account')
    password.send_keys('qiniu_password')
    login.click()

    time.sleep(30)

    balance = chrome.find_elements_by_xpath("//div[@class='cost-wrapper']//span")[0]
    chrome.quit()
    return balance.text


qiniu_balance_check()
