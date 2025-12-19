# Manager-of-Clinical-recommendation-documents
## Инструкция по развёртыванию и запуску (на Windows)
Необходимо установить mkcert и npm, затем выполнить команду 
```mkcert -install```
Затем создайте папку certs в корне проекта
```mkdir certs```
Следующий шаг - создание сертификата и ключа
```mkcert -key-file certs/key.pem -cert-file certs/cert.pem localhost 127.0.0.1 ::1```
Подготовка проекта
```npm install```
Далее компиляция проекта
```npm run serve```
Страница должна быть доступна по адресу https://localhost:8080

### Запуск после первичного
```npm run serve```
Страница должна быть доступна по адресу https://localhost:8080