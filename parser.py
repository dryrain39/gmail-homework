from bs4 import BeautifulSoup
import re


def text(html):
    soup = BeautifulSoup(html, 'html.parser')
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    visible_text = soup.getText(strip=True)
    return visible_text


def url(url_string):
    urls = re.findall('(http[s]?://[a-z0-9]+([\-.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(/.*)?$)', url_string)
    urls = [tuple(j for j in i if j)[0] for i in urls]

    return urls
