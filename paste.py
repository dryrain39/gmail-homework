json_f = """{
  "/": "## Account option ##",
  "account_user": "",
  "account_pass": "",
  "selenium_pass": "",

  ".": "## Mail receive option ##",
  "mail_sender": "fl0ckfl0ck@hotmail.com",

  "_": "## file option ##",
  "csv_path": "./db.csv",
  "image_dir": "./images/",
  "sel_image_dir": "./sel-images/",
  "map_preset": [
    ["AUTO", "None", "None"],
    ["Seoul", "37.1369993,126.7354759", "8"],
    ["Maynila","16.3611357,120.6427479", "7"]
  ],
  "sel_driver_path": "./chromedriver_win32.exe",
  "debug_lvl": 2
}
"""


def json_file():
    return json_f
