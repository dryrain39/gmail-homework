# -*- coding: utf-8 -*-


import json


def read(conf='config.json'):
    # 프로그램의 설정 파일을 읽는다. conf값이 지정되지 않으면 ./config.json 이 기본이다.
    try:
        with open(conf) as json_file:
            json_data = json.load(json_file)
            return json_data
    except Exception:
        return False


def write(data, conf='config.json'):
    # 프로그램의 설정 파일을 쓴다. conf값이 지정되지 않으면 ./config.json이 기본이다.
    # 디버깅을 위한 함수. 사용하지 않는다.
    try:
        with open(conf, 'w') as json_file:
            json_file.write(json.dumps(data))
    except Exception:
        return False


def read_db(path):
    # .csv 를 읽는 함수이다.
    try:
        with open(path) as json_file:
            a = json_file
            return a
            pass
    except Exception:
        return False
