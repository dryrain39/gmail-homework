# -*- coding: utf-8 -*-

import logging
import stenographer
import sys
import json
import os
import shutil
from mapmaker import Mapmaker


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


def system_check():
    global cfg

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

    print("[....] Set debug level...")

    lv = [logging.DEBUG, logging.WARNING, logging.ERROR]

    logging.basicConfig(level=lv[cfg["debug_lvl"]], format='%(asctime)s - %(levelname)s - %(message)s')

    print("[INFO] Everything OK.")


system_check()
maps = Mapmaker()


def map_setting(config):
    for idx, item in enumerate(config['map_preset']):
        print('\t\t' + str(idx + 1) + ' - ' + item[0])

    ans = raw_input("[....] SELECT NUMBER >")

    maps.center = config['map_preset'][int(ans) - 1][1]
    maps.zoom = config['map_preset'][int(ans) - 1][2]

    maps.reform()


def update_images():
    print("[WARN] Your map draw setting has been deleted.")
    maps.reset()

    for root, dirs, files in os.walk(cfg["image_dir"]):
        for f in files:
            if f.endswith('.csv'):
                data = stenographer.read(root + '/' + f)
                skip = True
                for idx, item in enumerate(data):
                    if idx > 0 and item[4] != 'N/A' and item[5] != 'N/A':
                        skip = False
                        maps.add_item(item[4] + ',' + item[5])

                if skip is False:
                    maps.saveLocation = root + '/' + root.split("/")[-1] + '.jpg'
                    maps.draw_map()


def start_gmail():
    import main
    print("[INFO] Sync started. Please wait...")
    main.start()
    update_images()


if len(sys.argv) < 2:

    ans = True
    while ans:
        print ("""
        1. Sync Gmail now.
        2. Add Schedule task.
        3. Remove Schedule task.
        4. [ALL] Draw Google Map
        5. [EACH] Re-draw Google Map
        6. Map draw setting
        q. Exit
        r. Reload
        D. Delete all data
        """)
        ans = raw_input("[....] SELECT >")
        if ans is True:
            pass
        elif ans == "1":
            start_gmail()

        elif ans == "2":
            print("\n Student Deleted")

        elif ans == "3":
            print("\n Student Record Found")

        elif ans == "4":
            data = stenographer.read(cfg["csv_path"])
            for idx, item in enumerate(data):
                if idx > 0 and item[4] != 'N/A' and item[5] != 'N/A':
                    maps.add_item(item[4] + ',' + item[5])

            maps.saveLocation = cfg['image_dir'] + 'all.jpg'
            maps.draw_map()

        elif ans == "5":
            update_images()

        elif ans == "6":
            map_setting(cfg)

        elif ans == "q":
            sys.exit('USER EXIT')

        elif ans == "r":
            print("[INFO] Reloading...")
            system_check()

        elif ans == "D":
            shutil.rmtree(cfg['image_dir'])

            os.remove(cfg['csv_path'])
            os.mkdir(cfg['image_dir'])
            system_check()

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
