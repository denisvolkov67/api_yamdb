# Проект API для YaMDb
____

## О проекте
____

Проект **YaMDb** собирает отзывы (**Review**) пользователей на произведения (**Titles**). Произведения делятся на категории: *«Книги»*, *«Фильмы»*, *«Музыка»*. Список категорий (**Category**) может быть расширен администратором (например, можно добавить категорию *«изобразительное искусство»* или *«Ювелирка»*).

Сами произведения в **YaMDb** не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории *«Книги»* могут быть произведения *«Винни-Пух и все-все-все»* и *«Марсианские хроники»*, а в категории *«Музыка»* — песня *«Давеча»* группы *«Насекомые»* и вторая сюита Баха.

Произведению может быть присвоен жанр (**Genre**) из списка предустановленных (например, *«Сказка»*, *«Рок»* или *«Артхаус»*). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (**Review**) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

## Проект также разделен по пользовательским ролям:
____

* **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
* **Аутентифицированный пользователь** (**user**) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
* **Модератор** (**moderator**) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
* **Администратор** (**admin**) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
* **Суперюзер Django** — обладает правами администратора (admin).

## используемые технологии
____

* Django REST Framework
* Simple JWT - работа с JWT-токеном
* git

## Как запустить проект:
____

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/denisvolkov67/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
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

## Документация к API проекта YaMDb:
____

Более подробную документацию по проекту Вы можете увидеть, запустив проект и пройдя по ссылке http://localhost:8000/redoc/

Примеры запросов:

* GET - Получить список всех произведений

```
http://127.0.0.1:8000/api/v1/titles/
```

* Пример ответа в формате Json:

```
[
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
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
