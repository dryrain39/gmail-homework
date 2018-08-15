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
import parseman
import stenographer
import conf

reload(sys)
sys.setdefaultencoding("utf-8")


def get_mail(gid, pw, sender):
    # Gmail 모듈 활성화
    g = Gmail()
    g.login(gid, pw)

    # Gmail 에서 안 읽은 메일 리스트를 가져온다.
    mails = g.inbox().mail(sender=sender, unread=True)
    m = []
    d = []

    # 메일 데이터를 배열에 저장하고 읽음 상태로 쳐리한다.
    for mail in mails:
        mail.fetch()
        mail.read()
        logging.debug(mail.sent_at)
        m.append(mail.html)
        d.append(mail.sent_at)

    # 로그아웃 필수
    g.logout()

    # 메일 내용과 날짜를 리턴
    return [m, d]


def postman(mail, time):
    # 사실상 여기가 메인 함수
    # 초기 데이터를 구성한다
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

    # 날짜별로 폴더 이름을 설정한다.
    dirname = cfg['image_dir'] + time.strftime('%Y-%m-%d')

    # constructor
    # 폴더가 없으면 생성한다.
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    # downloader.py, parseman.py
    # mail의 텍스트를 파싱하고 url을 훑는다.
    for url in parseman.url(parseman.text(mail)):
        # url 길이가 200자 이상이면 종료.
        if len(url) > 200:
            return None

        # download에서 넘어온 결과값을 저장한다.
        downloader_result = downloader.download(url, dirname)

        # download가 정상적인 URL이 아니거나 이미지를 못 찾으면 False 반환, 종료.
        if downloader_result is False:
            return None

        # 데이터 변수에 값을 담는다
        data["Filename"] = downloader_result['filename']
        data["Short URL"] = downloader_result['short_url']
        data["Full URL"] = downloader_result['full_url']

    path = dirname + '/' + data["Filename"]

    # location_master.py
    # 이미지의 GPS를 파싱한다.
    try:
        image = Image.open(path)
        gps_data = location_master.get_exif_data(image)
        gps_data = location_master.get_lat_lon(gps_data)
        # location_master에서 None이 리턴되면 'N/A'라고 기록한다.
        data['Latitude'] = 'N/A' if gps_data[0] is None else gps_data[0]
        data['Longitude'] = 'N/A' if gps_data[1] is None else gps_data[1]
    except Exception:
        pass

    # hashman.py
    # 해시값을 계산한다.
    hash_data = hashman.hashall(path)
    data["MD5"] = hash_data["MD5"]
    data["SHA1"] = hash_data["SHA1"]

    # 날짜별 폴더마다 CSV파일로 저장한다.
    local_csv = dirname + '/' + time.strftime('%Y-%m-%d') + '.csv'
    if stenographer.check(local_csv) is False:
        stenographer.make_new(local_csv)
    stenographer.write(data, local_csv)

    # stenographer.py
    # 전체 데이터를 저장한다.
    stenographer.write(data, cfg['csv_path'])
    pass


def start():
    global cfg

    # 프로그램의 config를 체크하고 바로잡는다.
    logging.debug("check system config...")
    cfg = conf.read()

    logging.debug("check system database...")
    if not os.path.exists(cfg["csv_path"]):
        logging.debug("create new system database...")
        stenographer.make_new(cfg["csv_path"])

    # 이메일을 가져오고 postman으로 넘겨준다.
    mailbox = get_mail(cfg["account_user"], cfg["account_pass"], cfg["mail_sender"])

    for idx, mail in enumerate(mailbox[0]):
        postman(mail, mailbox[1][idx])
