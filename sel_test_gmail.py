# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
import json
import sys
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def read_config():
    try:
        with open("config.json") as json_file:
            json_data = json.load(json_file)
            return json_data
    except Exception:
        sys.exit("Config read error.")


cfg = read_config()

opts = Options()
opts.add_argument("Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)")

driver = webdriver.Chrome('./driver/chromedriver_mac64', chrome_options=opts)

driver.get('http://mail.google.com/mail/h/')

time.sleep(2)
emailElem = driver.find_element_by_xpath('//*[@id="identifierId"]')
emailElem.send_keys(cfg['account_user'] + '\n')
time.sleep(4)
emailElem = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
emailElem.send_keys(cfg['selenium_pass'] + '\n')

logging.info("Please Solve 2FA")
while True:
    time.sleep(4)
    try:
        returnToDefaultGmail = driver.find_element_by_xpath('//*[@id="maia-main"]/form/p/input')
        returnToDefaultGmail.click()
    except Exception:
        pass

    try:
        asdf = driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[1]/td[1]/h1/a/img')
        logging.debug(asdf)
        logging.info("2FA Solved!")
        break
    except Exception:
        pass

time.sleep(3)

while True:
    searchBox = driver.find_element_by_xpath('//*[@name="q"]')
    searchBox.clear()
    searchBox.send_keys("is:unread from:(fl0ckfl0ck@hotmail.com)" + "\n")

    time.sleep(3)

    try:
    # mailList = driver.find_element_by_xpath(
    #     '/html/body/table[3]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/form/table[2]/tbody/tr[1]/td[3]/a')
        mailList = driver.find_element_by_xpath(
            '/html/body/table[2]/tbody/tr/td[2]/table[1]/tbody/tr/td[2]/form/table[2]/tbody/tr[1]/td[3]/a/span/b'
        )
        mailList.click()
    except Exception:
        break

    time.sleep(1)
    mailText = driver.find_element_by_xpath(
        '//*[@class="msg"]/div')
    print mailText.text

    time.sleep(1)
    mailTime = driver.find_element_by_xpath(
        '//*[@bgcolor="#cccccc"]/tbody/tr/td/table/tbody/tr/td[2]')
    print mailTime.text

# nextButton = driver.find_element_by_id('next')
# nextButton.click()
# time.sleep(1)
# passwordElem = driver.find_element_by_id('Passwd')
# passwordElem.send_keys('')
# signinButton = driver.find_element_by_id('signIn')
# signinButton.click()

driver.close()
