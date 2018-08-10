# -*- coding: utf-8 -*-

import logging
import stenographer
import sys
import json
import os


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


if len(sys.argv) < 2:
    print("[....] Check system config...")
    cfg = read_config()
    if cfg is False:
        print("[ERR!] Please download system config! --> https://github.com/dryrain39/gmail-homework")
        sys.exit('Config Not Found')

    if cfg['account_pass'] == '' or cfg['account_user'] == '' or cfg['mail_sender'] == '':
        print("[ERR!] Set your credential in config.json")
        sys.exit('Config Not Set')

    print("[....] Check system database...")
    if not os.path.exists(cfg["csv_path"]):
        logging.debug("[INFO] Database not found. Create new system database...")
        stenographer.make_new(cfg["csv_path"])

    print("[INFO] Everything OK.")

    ans = True
    while ans:
        print ("""
        1. Sync Gmail now.
        2. Add Schedule task.
        3. Remove Schedule task.
        4. Exit/Quit
        """)
        ans = raw_input("SELECT >")
        if ans == "1":
            start_gmail()
        elif ans == "2":
            print("\n Student Deleted")
        elif ans == "3":
            print("\n Student Record Found")
        elif ans == "4":
            sys.exit('USER EXIT')
        else:
            print("\n Not Valid Choice. Try again")


else:

    if sys.argv[1] == 'gmail':
        start_gmail()
        pass

    if sys.argv[1] == 'reg_service':
        pass

    if sys.argv[1] == 'del_service':
        pass

    if sys.argv[1] == 'exit':
        sys.exit('USER EXIT')
        pass
