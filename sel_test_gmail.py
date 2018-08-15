# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions

import sys
import os
import logging
import re
import requests
import urllib
import unicodedata
from PIL import Image

import stenographer
import location_master
import hashman
import parseman
import conf

reload(sys)
sys.setdefaultencoding("utf-8")

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

cfg = conf.read()

opts = Options()
opts.add_argument("Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)")

driver = webdriver.Chrome('./driver/chromedriver_mac64', chrome_options=opts)

driver.get('http://mail.google.com/mail/h/')
driver.maximize_window()

time.sleep(2)
emailElem = driver.find_element_by_xpath('//*[@id="identifierId"]')
emailElem.send_keys(cfg['account_user'] + '\n')
time.sleep(2)
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

mails = {
    'body': [],
    'time': []
}

while True:
    searchBox = driver.find_element_by_xpath('//*[@name="q"]')
    searchBox.clear()
    searchBox.send_keys("is:unread from:(fl0ckfl0ck@hotmail.com)" + "\n")

    time.sleep(3)

    try:
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
    mails['body'].append(mailText.text)

    time.sleep(1)
    mailTime = driver.find_element_by_xpath(
        '//*[@bgcolor="#cccccc"]/tbody/tr/td/table/tbody/tr/td[2]')
    print mailTime.text
    mails['time'].append(mailTime.text)

# mails = conf.read("sel_test.json")
for idx, mail in enumerate(mails['body']):
    data = {
        'Date': "",
        'Short URL': "",
        'Full URL': "",
        'Filename': "",
        'Latitude': "N/A",
        'Longitude': "N/A",
        'MD5': None,
        'SHA1': None
    }

    # 2018년 8월 15일 오후 8:31
    t = str(mails['time'][idx].decode()).replace('년 ', '-').replace('월 ', '-').replace('일', '')
    time_data = t.split(' ')[0]
    time_d = time_data.split('-')

    if len(time_d[1]) == 1:
        time_d[1] = '0' + time_d[1]

    if len(time_d[2]) == 1:
        time_d[2] = '0' + time_d[2]

    time_data = '-'.join(time_d)
    data['Date'] = time_data
    dirname = cfg['sel_image_dir'] + time_data + '/'

    # constructor
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        stenographer.make_new(dirname + time_data + '.csv')

    for url in parseman.url(mail.replace('\n', '')):
        if len(url) > 500:
            continue

        while True:
            if len(url) <= 1:
                break

            try:
                driver.get(url)
            except exceptions.WebDriverException:
                break

            time.sleep(1)

            print driver.current_url.split('.')[-1]
            if re.match('(jpg)|(png)|(gif)', driver.current_url.split('.')[-1]):
                data['Short URL'] = url
                data['Full URL'] = driver.current_url

                # image download
                data['Filename'] = unicodedata.normalize('NFC', unicode(
                        urllib.unquote(str(driver.current_url.split('/')[-1])))).decode()

                with open(dirname + data['Filename'], "wb") as f:
                    f.write(requests.get(driver.current_url).content)

                # gps_finder
                try:
                    image = Image.open(dirname + data['Filename'])
                    gps_data = location_master.get_exif_data(image)
                    gps_data = location_master.get_lat_lon(gps_data)
                    data['Latitude'] = 'N/A' if gps_data[0] is None else gps_data[0]
                    data['Longitude'] = 'N/A' if gps_data[1] is None else gps_data[1]
                except Exception:
                    pass

                # hashman
                hash_data = hashman.hashall(dirname + data['Filename'])
                data["MD5"] = hash_data["MD5"]
                data["SHA1"] = hash_data["SHA1"]

                stenographer.write(data, dirname + time_data + '.csv')

                print 'OK'
                break
            else:
                url = url[0:-1]

driver.close()
