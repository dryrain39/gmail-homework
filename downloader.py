# -*- coding: utf-8 -*-

import requests
import urllib
import logging
import unicodedata


def download_image(url, path):
    # 이미지 다운로드 함수
    try:
        r = requests.get(url)
    except Exception:
        logging.debug("Cannot access :" + url)
        return False

    # content-type을 확인하여 이미지면 다운로드 받고 아니면 걸러낸다.
    logging.debug(r.headers['content-type'])
    logging.debug(r)
    header = r.headers['content-type'].split('/')
    if header[0] == "image":
        logging.debug("Image detected: " + url)

        if r.url.find('/'):
            filename = r.url.rsplit('/', 1)[1]
            # 맥에서 한글을 입력할 경우 윈도우에서 분리되어보이는 현상을 방지하기 위한 코드.
            filename = unicodedata.normalize('NFC', unicode(urllib.unquote(str(filename)))).decode()
        else:
            logging.debug("url error.")
            return False

        with open(path + "/" + filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)

        logging.debug(filename + " download successful.")

        # filename 과 full_url 리턴
        return {
            "filename": filename,
            "full_url": r.url
        }

    logging.debug(url + " is not image or 404.")
    return False


def download(url, path):
    # 다운로드 요청 함수
    logging.debug("start test url: " + url)

    d_data = False

    # d_data가 False가 아닐 때 까지 무한 반복한다.
    while d_data is False:
        # 이미지 다운로드 시도
        d_data = download_image(url, path)

        if len(url) is 0:
            # URL길이가 0이 되면 중단한다.
            logging.debug("failed.")
            return False

        if d_data is False:
            # 다운로드 시도에 실패하면 url에서 한글자를 자른다.
            url = url[0:-1]
            logging.debug("download Failed. retry: ")
        pass
    else:
        # 오류 없이 한번에 다운로드 받았을 경우 perfect!
        logging.debug("Perfect!")
        pass

    # 이미지가 다운로드 된다면 d_data 값을 넘겨준다.
    logging.debug("ok. success.")
    d_data["short_url"] = url
    return d_data
