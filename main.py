from gmail import Gmail
import json
from bs4 import BeautifulSoup
import re

DEBUG = True


def debug(text):
    if DEBUG is True:
        print(text)


# Read configuration before start.
def read_config():
    try:
        with open("config.json") as json_file:
            json_data = json.load(json_file)
            return json_data
    except Exception:
        exit("Config read error.")


def get_mail(gid, pw, sender):
    g = Gmail()
    g.login(gid, pw)
    mails = g.inbox().mail(sender=sender)
    m = []
    for mail in mails:
        mail.fetch()
        debug(mail.html)
        m.append(mail.html)

    g.logout()
    return m


def get_visible_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    visible_text = soup.getText(strip=True)
    return visible_text


def parse_url(url_string):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url_string)
    return urls


cfg = read_config()
for i in get_mail(cfg["account_user"], cfg["account_pass"], cfg["mail_sender"]):
    debug(parse_url(get_visible_text(i)))