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

reload(sys)

sys.setdefaultencoding("utf-8")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Read configuration before start.
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
    for mail in mails:
        mail.fetch()
        logging.debug(mail.html)
        m.append(mail.html)

    g.logout()
    return m


def get_visible_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    visible_text = soup.getText(strip=True)
    return visible_text


def parse_url(url_string):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url_string)
    return urls


def db_insert():
    pass


def download_image():
    r = requests.get('http://fl0ckfl0ck.info/%E1%84%88%E1%85%A9%E1%84%88%E1%85%B5.jpg')
    logging.debug(r.headers['content-type'])
    logging.debug(r)
    header = r.headers['content-type'].split('/')
    if header[0] == "image":
        logging.debug("ok")

        if r.url.find('/'):
            filename = r.url.rsplit('/', 1)[1]
            filename = str(filename.decode('utf-8'))

            logging.debug(unicodedata.normalize('NFC', unicode(urllib.unquote(str(filename)))).decode())

        with open(unicodedata.normalize('NFC', unicode(urllib.unquote(str(filename)))).decode(), 'wb') as f:
            for chunk in r:
                f.write(chunk)
    pass


download_image()

exit()
cfg = read_config()
for i in get_mail(cfg["account_user"], cfg["account_pass"], cfg["mail_sender"]):
    logging.debug(parse_url(get_visible_text(i)))
