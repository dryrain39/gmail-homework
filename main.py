# -*- coding: utf-8 -*-
from gmail.gmail import Gmail
from PIL import Image

import json
import logging
import sys
import os

import location_master
import hashman
import downloader
import parser
import stenographer

reload(sys)
sys.setdefaultencoding("utf-8")

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


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


def postman(mail, time):
    data = {
        'Date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'Short URL': "",
        'Full URL': "",
        'Filename': "",
        'Latitude': "N/A",
        'Longitude': "N/A",
        'MD5': None,
        'SHA1': None
    }
    dirname = cfg['image_dir'] + time.strftime('%Y-%m-%d')

    # constructor
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # downloader
    for url in parser.url(parser.text(mail)):
        downloader_result = downloader.download(url, dirname)

        if downloader_result is False:
            return None

        data["Filename"] = downloader_result['filename']
        data["Short URL"] = downloader_result['short_url']
        data["Full URL"] = downloader_result['full_url']

    path = dirname + '/' + data["Filename"]

    # gps_finder
    try:
        image = Image.open(path)
        gps_data = location_master.get_exif_data(image)
        gps_data = location_master.get_lat_lon(gps_data)
        data['Latitude'] = 'N/A' if gps_data[0] is None else gps_data[0]
        data['Longitude'] = 'N/A' if gps_data[1] is None else gps_data[1]
    except Exception:
        pass

    # hashman
    hash_data = hashman.hashall(path)
    data["MD5"] = hash_data["MD5"]
    data["SHA1"] = hash_data["SHA1"]

    # stenographer
    stenographer.write(data, "./db.csv")

    # map_drawer

    # watchmaker

    # treasure_hunter

    # print(mail)

    pass


def start():
    global cfg
    cfg = read_config()
    mailbox = get_mail(cfg["account_user"], cfg["account_pass"], cfg["mail_sender"])

    for idx, mail in enumerate(mailbox[0]):
        postman(mail, mailbox[1][idx])
