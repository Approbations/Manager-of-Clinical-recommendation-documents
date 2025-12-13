import datetime
import requests
import threading
import pyexcel as pe
from concurrent.futures import ThreadPoolExecutor
from .db.postgres import DataManager

db_lock = threading.Lock()


def minzdrav_excel():
    '''с сайта скачивается документ, который имеет названия, которые не используются,
    поэтому подчищаем так чтобы было как можно меньше документов на выброс'''

    url = "https://apicr.minzdrav.gov.ru/api.ashx"
    params = {'op': 'GetJsonClinrecsFilterV2Excel'}
    data = {'filter': {"status": [1], "search": "",    "year": "",    "specialties": []}}

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://apicr.minzdrav.gov.ru',
        'Referer': 'https://apicr.minzdrav.gov.ru/',
    }
    try:
        response = requests.post(url, params=params, json=data, headers=headers)
        response.raise_for_status()

        sheets = pe.get_array(file_content=response.content, file_type='xlsx')
        lst = []
        for i in range(len(sheets)):
            if (type(sheets[i][6]) != datetime.datetime) or (sheets[i][5] == 'Нет'): continue

            lst.append(sheets[i])
        print(len(lst))

        lst.sort(key=lambda x: x[0])

        lst2 = [lst[-1]]
        for i in range(len(lst) - 1, 0, -1):
            if lst[i - 1][0][:-1] == lst[i][0][:-1]:
                continue
            lst2.append(lst[i - 1])
        print(len(lst2))
        # print(*lst2, sep='\n')

        del lst, sheets

    except Exception as e:
        print(f"Ошибка: {e}")
        return []
    clinical_recommendations(lst2)


def clinical_recommendations(data: list):
    data_base = DataManager()
    if data_base.database_exists():

        with ThreadPoolExecutor(max_workers=15) as pool:
            futures = [pool.submit(download, line, data_base) for line in data]

            completed = 0
            for future in futures:
                try:
                    future.result()
                    completed += 1
                except Exception as e:
                    print(f"Ошибка в потоке: {e}")
                print(completed)
        print(f"Загрузка данных в БД ({len(data_base.upload_list)} записей)")
        data_base.upload_data()
    else:
        print("Вы не создали базу данных")


def download(line: list, data_base: DataManager):
    print(f"Получена строка: {line}")
    print(f"Длина строки: {len(line)}")

    try:
        # Извлекаем данные из line
        doc_id = line[0]
        title = line[1]
        MCB = line[2]
        age_category = line[3]
        developer = line[4]

        placement_data = line[6]

        if isinstance(placement_data, datetime.datetime):
            placement_date = placement_data.date()
        else:
            placement_date = datetime.date.today()

        print(f"Данные: doc_id={doc_id}, placement_date={placement_date}")

        # Скачиваем PDF
        url = f"https://apicr.minzdrav.gov.ru/api.ashx?op=GetClinrecPdf&id={doc_id[:-2]}"
        print(f"Загружаем: {url}")
        response = requests.get(url)

        if response.status_code == 200:
            file_content = response.content
            print(f"Загружено {len(file_content)} байт для {doc_id}")

            with db_lock:
                data_base.add_to_upload_list(
                    id_cr=doc_id,
                    title=title,
                    MCB=MCB,
                    age_category=age_category,
                    developer=developer,
                    placement_date=placement_date,
                    data=file_content,
                    creator="Минздрав"
                )
            print(f"Успешно добавлен в список: {doc_id}")
        else:
            print(f"Ошибка загрузки {doc_id}: статус {response.status_code}")

    except Exception as e:
        print(f"Ошибка в download: {e}")
        import traceback
        traceback.print_exc()


# раскоментируйте для скачивания
# minzdrav_excel()
