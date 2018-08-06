# -*- coding: utf-8 -*-

from gmail.gmail import Gmail
import json
from bs4 import BeautifulSoup
import re
import requests
import urllib
import logging
import sys
import unicodedata
import datetime
import os

import location_master
from PIL import Image

import hashman


reload(sys)
sys.setdefaultencoding("utf-8")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def read_config():
    try:
        with open("config.json") as json_file:
            json_data = json.load(json_file)
            return json_data
    except Exception:
        exit("Config read error.")


def get_mail(gid, pw, sender):
    g = Gmail()
    g.login(gid, pw)
    mails = g.inbox().mail(sender=sender)
    m = []
    d = []
    for mail in mails:
        mail.fetch()
        logging.debug(mail.sent_at)
        m.append(mail.html)
        d.append(mail.sent_at)

    g.logout()
    return [m, d]


def get_visible_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    visible_text = soup.getText(strip=True)
    return visible_text


def parse_url(url_string):
    urls = re.findall('(http[s]?://[a-z0-9]+([\-.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(/.*)?$)', url_string)
    urls = [tuple(j for j in i if j)[0] for i in urls]

    return urls


def db_insert():
    pass


def download_image(url, path):
    try:
        r = requests.get(url)
    except Exception:
        logging.error("Cannot access :" + url)
        return False

    logging.debug(r.headers['content-type'])
    logging.debug(r)
    header = r.headers['content-type'].split('/')
    if header[0] == "image":
        logging.debug("Image detected: " + url)

        if r.url.find('/'):
            filename = r.url.rsplit('/', 1)[1]
            filename = unicodedata.normalize('NFC', unicode(urllib.unquote(str(filename)))).decode()
        else:
            logging.error("url error.")
            return False

        with open(path + "/" + filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)

        logging.debug(filename + " download successful.")
        return filename

    logging.error(url + " is not image or 404.")
    return False


def downloader(url, path):
    logging.debug("start test url: " + url)

    d_filename = False

    while d_filename is False:
        d_filename = download_image(url, path)

        if len(url) is 0:
            logging.debug("failed.")
            return False

        url = url[0:-1]
        logging.debug("download Failed. retry: ")
        pass
    else:
        logging.debug("Perfect!")
        pass

    logging.debug("ok. success.")
    return d_filename


def postman(mail, time):
    dirname = cfg['image_dir'] + time.strftime('%Y-%m-%d')
    filename = False
    gps_data = 'N/A'

    # constructor
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # downloader
    for url in parse_url(get_visible_text(mail)):
        filename = downloader(url, dirname)

    # gps_finder
    if filename is not False:
        try:
            image = Image.open(dirname + '/' + filename)
            gps_data = location_master.get_exif_data(image)
        except Exception:
            pass
    else:
        return

    # hashman
    hash_data = hashman.hashall(dirname + '/' + filename)

    # stenographer

    # map_drawer

    # treasure_hunter

    # print(mail)


    pass


# download_image('http://fl0ckfl0ck.info/%E1%84%88%E1%85%A9%E1%84%88%E1%85%B5.jpg')

gps_finder('./2018-08-03/druwa.jpg')

exit()
global cfg
cfg = read_config()
mailbox = get_mail(cfg["account_user"], cfg["account_pass"], cfg["mail_sender"])

for idx, mail in enumerate(mailbox[0]):
    postman(mail, mailbox[1][idx])
