**Проект api_yamdb**
В этом проекте реализовано API для получения произведений, их жанров и категорий. А также отзывов к произведениям и коментариев. 

**Установка проекта на локальной машине**

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/yandex-praktikum/kittygram.git
```

```
cd kittygram
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/scriptable/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

**Примеры запросов к API**

Получение списка всех произведений
```
GET http://127.0.0.1:8000/api/v1/titles/
```
Ответ
```
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{
"id": 0,
"name": "string",
"year": 0,
"rating": 0,
"description": "string",
"genre": [],
"category": {}
}
]
}
```

Добавление нового отзыва
```
POST http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
{
"text": "string",
"score": 1
}
```

Ответ
```
{
"id": 0,
"text": "string",
"author": "string",
"score": 1,
"pub_date": "2019-08-24T14:15:22Z"
}
```

Получение комментария к отзыву
```
GET http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

```

Ответ
```
{
"id": 0,
"text": "string",
"author": "string",
"pub_date": "2019-08-24T14:15:22Z"
}
```

**Managment команда для заполнения БД**
Заполняет пустую БД данными из csv файлов
```

python managment.py load_csv

```