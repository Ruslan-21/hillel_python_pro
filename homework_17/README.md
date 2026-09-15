# Bookstore

Навчальний Django-проєкт книжкового магазину.

## Можливості

- перегляд списку книг;
- перегляд інформації про книгу;
- створення, редагування та видалення книг;
- робота з категоріями;
- кошик;
- створення замовлень;
- відправка email після створення замовлення;
- оплата через Stripe;
- авторизація користувачів;
- асинхронні views;
- тести моделей, форм, views та основних сценаріїв.

## Технології

- Python 3.14
- Django 6.0.5
- PostgreSQL 16
- Redis 7
- Docker
- pytest
- pytest-django
- factory-boy
- pytest-cov
- Stripe

## Запуск проєкту

Для запуску проєкту використовується Docker Compose:

    docker compose up -d

Перевірити стан контейнерів:

    docker compose ps

Проєкт доступний за адресою:

    http://localhost:8000

## Тести

Запуск усіх тестів:

    docker compose exec web pytest

Запуск тестів моделей:

    docker compose exec web pytest tests/test_models.py

## Coverage

Для перевірки покриття коду:

    docker compose exec web pytest --cov=. --cov-report=term-missing

Поточний результат:

    69 passed

Загальний coverage:

    96%

Coverage моделей `books.models`:

    100%

## AI Usage

Під час виконання завдання використовувався ChatGPT для code review, генерації тестів, створення docstrings та покращення документації проєкту.

AI використовувався для:

- code review складних views;
- аналізу використання Django transactions;
- генерації тестів для моделей;
- перевірки зв'язків між моделями;
- підготовки docstrings для views;
- оновлення README;
- підготовки промптів для виконання завдання.

Усі запропоновані AI зміни перевірялися вручну та застосовувалися лише після перевірки їхньої доцільності.

Використані промпти збережені у файлі `AI_PROMPTS.md`.

Результати code review та застосовані зміни збережені у файлі `AI_REVIEW.md`.