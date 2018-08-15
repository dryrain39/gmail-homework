# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import logging


def text(html):
    # html이 들어오면 눈에 보이는 텍스트만 넘겨준다. (getText)
    soup = BeautifulSoup(html, 'html.parser')
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    visible_text = soup.getText(strip=True)
    return visible_text


def url(url_string):
    # url을 정규식으로 검색한 후 있으면 반환해 준다.
    urls = re.findall('(http[s]?://[a-z0-9]+([\-.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(/.*)?$)', url_string)
    urls = [tuple(j for j in i if j)[0] for i in urls]
    logging.debug(urls)
    return urls
