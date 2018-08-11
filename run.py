# -*- coding: utf-8 -*-

import logging
import stenographer
import sys
import json
import os
from mapmaker import Mapmaker


def start_gmail():
    import main
    main.start()


def read_config():
    try:
        with open("config.json") as json_file:
            json_data = json.load(json_file)
            return json_data
    except Exception:
        return False


def read_database(path):
    try:
        with open(path) as json_file:
            a = json_file
            return a
            pass
    except Exception:
        return False


if len(sys.argv) < 2:
    print("[....] Check system config...")
    cfg = read_config()
    if read_config() is False:
        print("[ERR!] Please download system config! --> https://github.com/dryrain39/gmail-homework")
        sys.exit('Config Not Found')

    if cfg['account_pass'] == '' or cfg['account_user'] == '' or cfg['mail_sender'] == '':
        print("[ERR!] Set your credential in config.json")
        sys.exit('Config Not Set')

    print("[....] Check system database...")
    if read_database(cfg["csv_path"]) is False:
        print("[INFO] Database not found. Create system database...")
        stenographer.make_new(cfg["csv_path"])

    print("[INFO] Everything OK.")

    ans = True
    while ans:
        print ("""
        1. Sync Gmail now.
        2. Add Schedule task.
        3. Remove Schedule task.
        4. Draw Google Map
        q. Exit/Quit
        """)
        ans = raw_input("SELECT >")
        if ans == "1":
            start_gmail()
        elif ans == "2":
            print("\n Student Deleted")
        elif ans == "3":
            print("\n Student Record Found")
        elif ans == "4":
            maps = Mapmaker()
            maps.imageSize = '2000x3000'
            data = stenographer.read(cfg["csv_path"])
            for idx, item in enumerate(data):
                if idx > 1 and item[4] != 'N/A' and item[5] != 'N/A':
                    maps.add_item(item[4] + ',' + item[5])

            maps.draw_map()
            pass
        elif ans == "q":
            sys.exit('USER EXIT')
        else:
            print("\n Not Valid Choice. Try again")

else:

    if sys.argv[1] == 'gmail':
        print("[INFO] Sync Gmail now. Please Wait...")
        start_gmail()
        pass

    if sys.argv[1] == 'reg_service':
        pass

    if sys.argv[1] == 'del_service':
        pass

    if sys.argv[1] == 'exit':
        sys.exit('USER EXIT')
        pass
