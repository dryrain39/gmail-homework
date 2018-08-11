import requests


class Mapmaker:
    locationArray = ['37.49848938888889,127.01871491666667', '37.52779008333333,126.90460966666667']
    imageSize = '600x300'

    def add_item(self, item):
        self.locationArray.append(item)

    def draw_map(self):
        url = 'https://maps.googleapis.com/maps/api/staticmap?size=' + self.imageSize + '0&maptype=roadmap'
        for idx, loc in enumerate(self.locationArray):
            url = url + '&markers=color:red|label:' + str(idx + 1) + '|' + loc

        url = url + '&path=color:0x0000ff80|weight:5'

        for idx, loc in enumerate(self.locationArray):
            url = url + '|' + loc

        r = requests.get(url)
        header = r.headers['content-type'].split('/')
        if header[0] == "image":
            with open("timehere.jpg", 'wb') as f:
                for chunk in r:
                    f.write(chunk)

    def __init__(self):
        pass


ps = Mapmaker()
ps.draw_map()
