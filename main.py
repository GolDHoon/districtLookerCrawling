from typing import Final
from datetime import datetime
from art import *
import custom_json
import custom_csv
import custom_google_sheet
import main_logic

GA4_FILENAME_VIVATICKET = 'GA4_vivaticket.csv'
GA4_FILENAME_WEB = 'GA4_web.csv'

def getConfig():
    return custom_json.read_json()

if __name__ == '__main__':
    all_config: Final = getConfig()

    print("\n\n" + text2art("LV START"))
    print("라스베가스 BOS ORDER LIST 업데이트 시작 (" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ")")
    main_logic.data_update('local', 'lv', all_config)
    print("라스베가스 BOS ORDER LIST 업데이트 완료 (" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ")")

    print("\n\n" + text2art("DB START"))
    print("두바이 BOS ORDER LIST 업데이트 시작 (" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ")")
    main_logic.data_update('local', 'db', all_config)
    print("두바이 BOS ORDER LIST 업데이트 완료 (" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ")")
