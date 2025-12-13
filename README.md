# Manager-of-Clinical-recommendation-documents

## Как развернуть локально

Установите зависимости:

   pip install -r requirements.txt

Создаем базу данных "clinical_recommendations". 

Запускаем *.sql из папки bd для создания таблиц. 

Запускаем функцию minzdav_excel из docs_processing/upload_files ()


    with ThreadPoolExecutor(max_workers=15) as pool:
        futures = [pool.submit(download, line, data_base) for line in data]


Уменьшаем количество загружаемых документов, например до 10 (т.к. всего загружается 600+ документов, и это занимает около получаса)


    with ThreadPoolExecutor(max_workers=15) as pool:
        futures = [pool.submit(download, line, data_base) for line in data[:10]]

Запускаем с помощью uvicorn

    uvicorn main:app --host 0.0.0.0 --port 8002 --reload

## Запуск с помощью докера
1. Убедитесь, что свободен 8002 порт.
2. Поднимите контейнеры:

        docker compose up --build

   Приложение будет доступно на `http://localhost:8002`.
3. При необходимости переопределите переменные окружения через `.env` файл.
