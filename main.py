from gmail import Gmail
import json
from bs4 import BeautifulSoup


# Read configuration before start.
def read_config():
    try:
        with open("config.json") as json_file:
            json_data = json.load(json_file)
            return json_data
    except Exception:
        exit("Config read error.")


cfg = read_config()

g = Gmail()
g.login(cfg["account_user"], cfg["account_pass"])

mails = g.inbox().mail(sender=cfg["mail_sender"])

for mail in mails:
    mail.fetch()
    print(mail.body)


g.logout()
