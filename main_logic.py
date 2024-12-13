from typing import Final

from exceptiongroup import catch

import custom_csv
import custom_google_sheet
import threading
import datetime
import time
import pandas as pd


GA4_FILENAME_VIVATICKET = 'GA4_vivaticket.csv'
GA4_FILENAME_WEB = 'GA4_web.csv'

def data_update(env, prj_keyword, all_config):
    print("================================")
    sheet_id: Final = all_config[env][prj_keyword]["sheet_id"]
    print("GA4_ticket 데이터 read start")
    GA4_data_path: Final = all_config[env][prj_keyword]["GA4_data_path"]

    GA4_data_vivaticket = custom_csv.read_csv_as_list(GA4_data_path, GA4_FILENAME_VIVATICKET)

    print("누적 Data 량 : " + str(len(GA4_data_vivaticket)) + "rows")
    print("GA4_ticket 데이터 read end")
    print("================================")
    print("GA4_web 데이터 read start")

    GA4_data_web = custom_csv.read_csv_as_list(GA4_data_path, GA4_FILENAME_WEB)

    print("누적 Data 량 : " + str(len(GA4_data_web)) + "rows")
    print("GA4_web 데이터 read end")
    print("================================")
    print("bos_order_list 시트 업데이트 start")

    bos_oder_list_range = "bos_order_list!A"
    csv_file_path: Final = all_config[env][prj_keyword]["csv_file_path"]

    order_data = custom_csv.read_csv_as_list(csv_file_path)

    print("BOS데이터 <-> GA4데이터 매핑 start")

    combination_data = data_combination(prj_keyword, order_data, GA4_data_vivaticket, GA4_data_web)

    print("BOS데이터 <-> GA4데이터 매핑 end")

    chunked_combination_data = [combination_data[i:i + 5000] for i in range(0, len(combination_data), 5000)]

    rows = 0
    loof = 1
    for data in chunked_combination_data:
        sheet_range = bos_oder_list_range + str(loof) + ":AE"
        custom_google_sheet.google_sheet_update(sheet_id, sheet_range, data)
        loof += 5000
        rows += len(data)

    print("누적 Data 량 : " + str(rows) + "rows")
    print("bos_order_list 시트 업데이트 end")
    print("================================")

def data_combination(prj_keyword, order_data, GA4_data_vivaticket, GA4_data_web):
    GA4_dict_vivaticket = {item[0]: item[1] for item in GA4_data_vivaticket}
    GA4_data_web = {item[1]: [item[0], item[2],item[3],item[4]] for item in GA4_data_web}

    checker = True
    result = list()

    for order in order_data:
        try:
            result_row = list()
            if checker:
                result_row.append('ReservationAK')
                result_row.append('Quantity')
                result_row.append('TotalAmount')

                if prj_keyword == 'lv':
                    result_row.append('hhk_lasvegas_ga_session_id')
                else:
                    result_row.append('hhk_dubai_ga_session_id')

                result_row.append('web 방문 날짜')
                result_row.append('세션 소스/매체')
                result_row.append('세션 캠페인')
                result_row.append('캠페인')

                checker = False
            else:
                result_row.append(order[13].replace("\"",""))
                quantity = order[10]
                if (prj_keyword == 'lv'):
                    quantity = str(float(quantity) / 2)
                result_row.append(quantity)
                result_row.append(order[11])
                sessionId = GA4_dict_vivaticket.get(order[13].replace("\"",""), '')
                if sessionId != '':
                    result_row.append(sessionId)
                    web_data = GA4_data_web.get(sessionId, ([]))
                    if len(web_data) > 0:
                        date = pd.to_datetime(web_data[0], format="%Y. %m. %d.", errors='coerce')
                        result_row.append(str(date))
                        result_row.append(web_data[1])
                        result_row.append(web_data[2])
                        result_row.append(web_data[3])
                    else:
                        date = pd.to_datetime(order[3], format="%Y-%m-%d", errors='coerce')
                        result_row.append(str(date))
                        result_row.append('')
                        result_row.append('')
                        result_row.append('')
                else:
                    result_row.append('')
                    date = pd.to_datetime(order[3], format="%Y-%m-%d", errors='coerce')
                    result_row.append(str(date))
                    result_row.append('')
                    result_row.append('')
                    result_row.append('')
        except Exception as e: pass

        result.append(result_row)

    return result

def print_mapping_progress(keyword, sleep_time):
    while True:
        print(keyword)
        time.sleep(sleep_time)