# api_final_yatube
## API для проекта yatube

Yatube это социальный блог в котором реализован следующий функционал.

- Добавление постов
- Возможность добовлять комментарии к постам
- Возможность подписываться на авторов постов
- Принадлежность постов к группам
- ✨Аутентификация с помощью JWT✨

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```sh
git clone https://github.com/jamsi-max/api_final_yatube.git
```
```sh
cd api_final_yatube
```
Cоздать и активировать виртуальное окружение:
```sh
python3 -m venv env
```
> для Linux:
```sh
source env/bin/activate
```
> для Windows:
```sh
venv\Scripts\acrivate
```
Обновить pip:
```sh
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```sh
pip install -r requirements.txt
```
Выполнить миграции:
```sh
python3 manage.py migrate
```
Запустить проект:
> для Windows:
```sh
python manage.py runserver
```
> для Linux:
```sh
python3 manage.py runserver
```
## Автор

```sh
Maxon ©
```

## Лицензия

MIT



