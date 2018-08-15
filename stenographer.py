# -*- coding: utf-8 -*-

import csv


def write(data, path):
    # csv를 작성(추가)한다. fieldnames에 맞는 dictionary가 들어오면 필드에 맞게 csv를 쓴다.
    with open(path, 'a') as csvfile:
        fieldnames = ['Date', 'Short URL', 'Full URL', 'Filename', 'Latitude', 'Longitude', 'MD5', 'SHA1']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writerow(data)
    pass


def make_new(path):
    # 초기 field(첫 번째 라인)을 구성하는 함수이다.
    with open(path, 'w') as csvfile:
        fieldnames = ['Date', 'Short URL', 'Full URL', 'Filename', 'Latitude', 'Longitude', 'MD5', 'SHA1']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
    pass


def read(path):
    # csv파일을 읽는 함수
    with open(path, 'r') as csvfile:
        r = list(csv.reader(csvfile))
        return r
    pass


def check(path):
    # 파일이 존재하는지 확인하는 함수
    # json이 아니더라도 존재만 하면 False를 반환하지 않는다.
    try:
        with open(path) as json_file:
            a = json_file
            return a
            pass
    except Exception:
        return False
