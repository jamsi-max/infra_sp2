# infra_sp2
✨  ✨  ✨  
`Проект Infra_sp2 это REST API с использованием контейнерезации (docker) для проекта YaMDb который собирает отзывы (Review) пользователей на произведения (Titles).
`
✨ ✨  ✨  
## **Запуск проекта**
##### 1. Клонировать репозиторий
#
```sh
git clone https://github.com/jamsi-max/infra_sp2.git
```
##### 2. Сооздать файл ".env" рядом с **"manage .py"** следующего содержания:
#
> DB_ENGINE=django.db.backends.postgresql
> DB_NAME=postgres
> POSTGRES_USER=postgres
> POSTGRES_PASSWORD=postgres
> DB_HOST=db
> DB_PORT=5432

##### 3. Cоздать и активировать виртуальное окружение:
#
```sh
python -m venv env
```
> для Linux:
```sh
source env/bin/activate
```
> для Windows:
```sh
venv\Scripts\acrivate
```

##### 4. Обновить pip:
#
```sh
python -m pip install --upgrade pip
```
##### 5. Установить зависимости из файла requirements.txt:
#
```sh
pip install -r requirements.txt
```
##### 6. Перейти в директорию "infra_sp2\infra" где находиться файл **"docker-compose.yaml"** запустить консоль и выполнить команду для запуска проекта в контейнерах:
`Внимание! Docker уже должен быть установлен и запущен`
```sh
docker-compose up -d
```
##### 7. Выполнить миграции:
#
```sh
docker-compose exec web python manage.py migrate
```
##### 8. Заполнить базу тестовыми данными:
#
```sh
docker-compose exec web python manage.py loaddata fixtures.json
```
##### 9. Создать суперпользователя:
#
```sh
docker-compose exec web python manage.py createsuperuser
```
##### 10. При необходимости собрать статику если стили и картинки не отображаются:
#
```sh
docker-compose exec web python manage.py collectstatic --no-input
```

### Проект доступен по адресу http://localhost/redoc
#
### Перед остановкой проекта создать резервную копию базы:
#
```sh
docker-compose exec web python manage.py dumpdata > /app/api_yamdb/fixtures.json
```
##### Для остановки проекта используйте команду:
#
```sh
docker-compose down
```

## Лицензия

MIT

**Бесплатный софт**
##### Автор проекта: Макс
##### Связь с автором(телеграмм): https://t.me/jony2024 
##### © Copyright **[jamsi-max](https://github.com/jamsi-max)**



