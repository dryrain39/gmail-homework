# -*- coding: utf-8 -*-

import logging
import stenographer
import sys
import os
import shutil
from mapmaker import Mapmaker
import paste
import conf
import sel_test_gmail


def system_check():
    # 프로그램의 설정 파일을 읽고 초기 설정하는 부분이다.
    # Gmail 계정을 설정하지 않으면 강제로 종료한다.
    global cfg

    print("[....] Check system config...")
    cfg = conf.read()
    if cfg is False:
        with open('config.json', 'w') as json_file:
            json_file.write(paste.json_file())
        print("[ERR!] System config not found! Set your credential in config.json!")
        l = input()
        sys.exit('Config Not Found')

    if cfg['account_pass'] == '' or cfg['account_user'] == '' or cfg['mail_sender'] == '':
        print("[ERR!] Set your credential in config.json")
        l = input()
        sys.exit('Config Not Set')

    print("[....] Check system database...")
    if conf.read_db(cfg["csv_path"]) is False:
        print("[INFO] Database not found. Create system database...")
        stenographer.make_new(cfg["csv_path"])

    # Debug Level 설정 부분. 개발할 때 쓰고 사용하지 않는다.
    print("[....] Set debug level...")

    lv = [logging.DEBUG, logging.WARNING, logging.ERROR]

    logging.basicConfig(level=lv[cfg["debug_lvl"]], format='%(asctime)s - %(levelname)s - %(message)s')

    print("[INFO] Everything OK.")


system_check()
# mapmaker를 로드한다.
maps = Mapmaker()


def map_setting(config):
    # 지도 화면을 설정하는 함수. config에 저장된 프리셋으로 mapmaker의 설정을 변경한다.
    for idx, item in enumerate(config['map_preset']):
        print('        ' + str(idx + 1) + ' - ' + item[0])

    ans = raw_input("[....] SELECT NUMBER >")

    maps.center = config['map_preset'][int(ans) - 1][1]
    maps.zoom = config['map_preset'][int(ans) - 1][2]

    maps.reform()


def update_images():
    # 폴더(날짜)별 지도를 그려주는 함수.
    # 폴더들을 순회하며 csv를 읽고 지도를 그린다.
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


def draw_all():
    # 모든 지도를 그리는 함수 전체 데이터가 저장된 csv를 읽고 지도를 그린다.
    data = stenographer.read(cfg["csv_path"])
    for idx, item in enumerate(data):
        if idx > 0 and item[4] != 'N/A' and item[5] != 'N/A':
            maps.add_item(item[4] + ',' + item[5])

    maps.saveLocation = cfg['image_dir'] + 'all.jpg'
    maps.draw_map()


def start_gmail():
    # gmail 파싱 시작 함수. 예약 작업과 메뉴에서 각각 실행시킬 수 있어야 하기에 따로 함수로 빼 두었다.
    import main
    print("[INFO] Sync started. Please wait...")
    main.start()
    update_images()


if len(sys.argv) < 2:
    # 메뉴 시작
    ans = True
    while ans:
        print ("""
        1. Sync Gmail now.
        2. Add Schedule task.
        3. Remove Schedule task.
        4. [ALL!] Re-Draw Google Map
        5. [EACH] Re-draw Google Map
        6. Map draw setting
        7. Run with Selenium
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
            logging.debug(sys.argv[0])
            os.system('SchTasks /Create /SC DAILY /TN sync1150 /TR "' + str(sys.argv[0]) + ' gmail" /ST 11:50')
            os.system('SchTasks /Create /SC DAILY /TN sync2350 /TR "' + str(sys.argv[0]) + ' gmail" /ST 23:50')

        elif ans == "3":
            os.system('Schtasks /delete /tn sync1150 /f')
            os.system('Schtasks /delete /tn sync2350 /f')

        elif ans == "4":
            draw_all()

        elif ans == "5":
            update_images()

        elif ans == "6":
            map_setting(cfg)

        elif ans == "7":
            sel_test_gmail.run()

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

    # gmail 이라는 인자가 붙으면 즉시 gmail 파싱을 시작한다.
    if sys.argv[1] == 'gmail':
        print("[INFO] Sync Gmail now. Please Wait...")
        start_gmail()
        draw_all()
        pass
