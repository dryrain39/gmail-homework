import requests
import urllib
import logging
import unicodedata


def download_image(url, path):
    try:
        r = requests.get(url)
    except Exception:
        logging.debug("Cannot access :" + url)
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
            logging.debug("url error.")
            return False

        with open(path + "/" + filename, 'wb') as f:
            for chunk in r:
                f.write(chunk)

        logging.debug(filename + " download successful.")
        return {
            "filename": filename,
            "full_url": r.url
        }

    logging.debug(url + " is not image or 404.")
    return False


def download(url, path):
    logging.debug("start test url: " + url)

    d_data = False

    while d_data is False:
        d_data = download_image(url, path)

        if len(url) is 0:
            logging.debug("failed.")
            return False

        if d_data is False:
            url = url[0:-1]
            logging.debug("download Failed. retry: ")
        pass
    else:
        logging.debug("Perfect!")
        pass

    logging.debug("ok. success.")
    d_data["short_url"] = url
    return d_data
