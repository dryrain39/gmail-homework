import requests
import logging


class Mapmaker:
    imagePath = ''
    locationArray = []
    imageSize = '640x640'
    center = None
    zoom = None

    def __init__(self, imgPath):
        self.imagePath = imgPath
        logging.debug('Mapmaker Loaded!')

    def reform(self):
        if self.center == 'None':
            self.center = None

        if self.zoom == 'None':
            self.zoom = None

    def reset(self):
        self.locationArray = []
        self.imageSize = '640x640'
        self.center = None
        self.zoom = None

    def add_item(self, item):
        self.locationArray.append(item)

    def draw_map(self):
        print self.locationArray

        ct = 'center=' + self.center + '&' if self.center is not None else ''
        zm = 'zoom=' + self.zoom + '&' if self.zoom is not None else ''

        url = 'https://maps.googleapis.com/maps/api/staticmap?' + ct + zm + 'size=' + self.imageSize
        for idx, loc in enumerate(self.locationArray):
            url = url + '&markers=color:red|label:' + str(idx + 1) + '|' + loc

        url = url + '&path=color:0x0000ff80|weight:5'

        for idx, loc in enumerate(self.locationArray):
            url = url + '|' + loc

        print url

        r = requests.get(url)
        header = r.headers['content-type'].split('/')
        if header[0] == "image":
            with open(self.imagePath + "all.jpg", 'wb') as f:
                for chunk in r:
                    f.write(chunk)

        self.locationArray = []

