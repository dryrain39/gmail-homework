# -*- coding: utf-8 -*-

import requests
import logging


class Mapmaker:
    # 자유자재로 변경가능한 설정 값들.
    locationArray = []
    imageSize = '640x640'
    saveLocation = './all.jpg'
    center = None
    zoom = None

    def __init__(self):
        logging.debug('Mapmaker Loaded!')

    def reform(self):
        # None 스트링이 들어오면 None으로 바꾸어준다.
        if self.center == 'None':
            self.center = None

        if self.zoom == 'None':
            self.zoom = None

    def reset(self):
        # 초기 값으로 되돌리는 함수
        self.locationArray = []
        self.imageSize = '640x640'
        self.saveLocation = './'
        self.center = None
        self.zoom = None

    def add_item(self, item):
        # 좌표를 배열에 추가해준다.
        self.locationArray.append(item)

    def draw_map(self):
        # 지도를 그리는 함수 center 와 zoom이 있으면 설정하고 없으면 비운다.
        ct = 'center=' + self.center + '&' if self.center is not None else ''
        zm = 'zoom=' + self.zoom + '&' if self.zoom is not None else ''

        # 좌표 마커를 설정한다.
        url = 'https://maps.googleapis.com/maps/api/staticmap?' + ct + zm + 'size=' + self.imageSize
        for idx, loc in enumerate(self.locationArray):
            url = url + '&markers=color:red|label:' + str(idx + 1) + '|' + loc

        url = url + '&path=color:0x0000ff80|weight:5'

        # 경로를 설정한다.
        for idx, loc in enumerate(self.locationArray):
            url = url + '|' + loc

        # 이미지를 지정한 위치에 다운로드.
        r = requests.get(url)
        header = r.headers['content-type'].split('/')
        if header[0] == "image":
            with open(self.saveLocation, 'wb') as f:
                for chunk in r:
                    f.write(chunk)

        self.locationArray = []

