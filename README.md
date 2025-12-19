# Manager-of-Clinical-recommendation-documents

## Как развернуть локально (всё производится на Windows)

Установите зависимости:

   pip install -r requirements.txt

Установите mkcert

        mkcert -install

Создайте папку .cert (в корне проекта)

        mkdir -p .cert

Если mkcert уставновлено в другом месте, то поменяйте и выполните команду

         & "C:\ProgramData\chocolatey\bin\mkcert.exe" -key-file ./.cert/key.pem -cert-file ./.cert/cert.pem localhost 127.0.0.1 ::1


Создаем базу данных "clinical_recommendations"

Запускаем *.sql из папки bd для создания таблиц. 

Запускаем функцию minzdav_excel из docs_processing/upload_files ()


        clinical_recommendations(lst2[:5])



Уменьшаем/увеличиваем количество загружаемых документов, например до 10 (т.к. всего загружается 600+ документов, и это занимает около получаса). По умолчанию стоит 5.


        clinical_recommendations(lst2[:100])


Запустите скрипт run.py 