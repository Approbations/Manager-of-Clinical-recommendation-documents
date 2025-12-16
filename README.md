# Manager-of-Clinical-recommendation-documents

## Как развернуть локально

Установите зависимости:

   pip install -r requirements.txt

Создайте папку ssh

Запустите скрипт generate-certs.py 

Создаем базу данных "clinical_recommendations"

Запускаем *.sql из папки bd для создания таблиц. 

Запускаем функцию minzdav_excel из docs_processing/upload_files ()


        clinical_recommendations(lst2[:5])



Уменьшаем/увеличиваем количество загружаемых документов, например до 10 (т.к. всего загружается 600+ документов, и это занимает около получаса). По умолчанию стоит 5.


        clinical_recommendations(lst2[:100])


Запускаем с помощью uvicorn

    uvicorn main:app --host localhost --port 8002 --ssl-keyfile ssl/key.pem --ssl-certfile ssl/cert.pem

## Запуск с помощью докера
1. Убедитесь, что свободен 8002 порт.
2. Поднимите контейнеры:

        docker compose up --build

   Приложение будет доступно на `https://localhost:8002`.
3. При необходимости переопределите переменные окружения через `.env` файл.
