
# Reviews Project (Django + SVM)

Полностью рабочий минималистичный сайт для создания и классификации отзывов (позитив/негатив). 
По умолчанию использует SQLite (без настроек). Модель SVM обучается на крошечном датасете и 
сохраняется в `ml/` при первом запуске.

## Быстрый старт

```bash
# 1) Создай и активируй виртуалку (по желанию)
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 2) Установи зависимости
pip install -r requirements.txt

# 3) Применяй миграции и создай админа
python manage.py migrate
python manage.py createsuperuser

# 4) (Опционально) обучи крошечную модель руками
python manage.py train_sentiment

# 5) Запусти сервер
python manage.py runserver
```

Открой http://127.0.0.1:8000/ — залогинься под суперпользователем, создавай отзывы. 
При первом добавлении отзыва модель автоматически обучится и сохранится в `ml/`.

## Как переключиться на PostgreSQL (если попросят)

В `reviews_site/settings.py` замени секцию `DATABASES` на:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "your_db",
        "USER": "your_user",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

И не забудь установить драйвер:
```bash
pip install psycopg2-binary
```

## Что реализовано
- Авторизация/выход
- Создание, редактирование, удаление отзывов
- Классификация SVM (позитив/негатив), цветовая подсветка
- Админка для просмотра отзывов
- Красивые минимальные шаблоны и стили
