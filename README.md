# Manager-of-Clinical-recommendation-documents

## Как развернуть локально
Создаем базу данных "clinical_recommendations". 

Запускаем *.sql из папки bd для создания таблиц. 

Запускаем функцию minzdav_excel из docs_processing/upload_files ()


    with ThreadPoolExecutor(max_workers=15) as pool:
        futures = [pool.submit(download, line, data_base) for line in data]


Уменьшаем количество загружаемых документов, например до 10 (т.к. всего загружается 600+ документов, и это занимает около получаса)


    with ThreadPoolExecutor(max_workers=15) as pool:
        futures = [pool.submit(download, line, data_base) for line in data[:10]]

Запускаем с помощью uvicorn

    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

## Запуск с помощью докера
Ещё тестируется