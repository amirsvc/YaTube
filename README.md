# YaTube - аналог живого журнала для блогеров.

## Описание проекта

Yatube - живой журнал для авторов и подписчиков. Пользователи могут создавать посты, подписываться на авторов, оставлять комментари к постам, прикреплять изображения к публикуемым постам.

Проект реализован на MVT-архитектуре, реализована система регистрации новых пользователей, восстановление паролей пользователей через почту, система тестирования проекта на unittest, пагинация постов и кэширование страниц. Проект имеет верстку с адаптацией под размер экрана устройства пользователя.

----------

Язык программирования: Python 3.7, реализация Вофтпщ 2.2

**Используемые библиотеки и пакеты:**

    Django==2.2.16
    mixer==7.1.2
    Pillow==8.3.1
    pytest==6.2.4
    pytest-django==4.4.0
    python-dotenv==0.21.0
    pytest-pythonpath==0.7.3
    requests==2.26.0
    six==1.16.0
    sorl-thumbnail==12.7.0
    Faker==12.0.1


## Инструкция по развёртыванию проекта

1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:amirsvc/Yatube.git
```

```
cd Yatube
```

2. Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

- Если у вас Linux/macOS

  ```
  source venv/bin/activate
  ```

- Если у вас windows

  ```
  source venv/scripts/activate
  ```

3. Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Выполнить миграции:
```
cd yatube

python3 manage.py migrate
```
5. Запустить проект (в режиме сервера Django):
```
python3 manage.py runserver
```

В проекте используется база данных SQLite

## Пример заполнения файла .env
```
SECRET_KEY =^!$edal%skvl+xn25$8eswd5ufylb!m63ia9pksjd3rd@oe%_m
ALLOWED_HOSTS= localhost,127.0.0.1,[::1]
```

Разработчик: Исиналинов Амир https://t.me/Amir_Isinalinov
