# БОБР
## Бэкенд сайта для настоящих бобров!

## Описание

#### Регистрация
Для регистрации отправьте POST запрос на адрес /api/registration/ с json вида:
#### `{"email": "test@mail.com", "nick": "test", "password": "pass"}`
Вы получите JWT токен, который можно использовать для дальнейшего подтверждения личности

## Стек БОБРа
1. Flask
2. Flask-JWT-Simple
3. PostgreSQL
4. Docker
---

## Варианты запуска
### 1. Docker
```bash
git clone https://github.com/MrRegrit/bobr-backend.git

cd bobr-backend

docker-compose up
```
### 2. Обычная установка
```bash
git clone https://github.com/MrRegrit/bobr-backend.git

cd bobr-backend

pip install -r requirements.txt

cd server

python app.py
```
