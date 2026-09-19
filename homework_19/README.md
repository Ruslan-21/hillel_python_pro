# Bookstore

[![Django CI](https://github.com/Ruslan-21/hillel_python_pro/actions/workflows/django.yml/badge.svg?branch=homework_19)](https://github.com/Ruslan-21/hillel_python_pro/actions/workflows/django.yml)
[![Coverage](https://img.shields.io/badge/coverage-89.49%25-brightgreen)](https://github.com/Ruslan-21/hillel_python_pro/actions)

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

## Архітектура

Проєкт складається з двох окремих Django-сервісів:

- **ProjectA** — основний книжковий магазин.
- **ProjectB** — сервіс керування складськими залишками.

ProjectA взаємодіє з ProjectB через REST API.

Схема взаємодії:

    Client
       |
       v
    NGINX
       |
       v
    ProjectA (Bookstore)
       |
       | REST API + JWT
       v
    ProjectB (Warehouse)
       |
       +--> PostgreSQL
       +--> Redis
       +--> Celery / Celery Beat

Обидва проєкти використовують Docker Compose та мають окремі Django-конфігурації.

## ProjectA — Bookstore

Основний функціонал:

- книги та категорії;
- користувачі та авторизація;
- JWT authentication;
- кошик;
- замовлення;
- Stripe;
- Redis caching;
- Celery та Celery Beat;
- email та фонові задачі;
- REST API;
- Swagger / OpenAPI;
- інтеграція з ProjectB.

API:

    http://localhost:8000/api/

Swagger / OpenAPI:

    http://localhost:8000/api/docs/

## ProjectB — Warehouse

ProjectB відповідає за складські залишки.

Основний функціонал:

- inventory API;
- PostgreSQL;
- Redis;
- Celery;
- JWT authentication;
- REST API;
- Docker;
- NGINX;
- Gunicorn.

ProjectA передає JWT-токен користувача до ProjectB під час запиту залишків.

Якщо складський сервіс недоступний, ProjectA повертає HTTP 503.

Якщо для книги відсутній запис про залишок, ProjectA повертає HTTP 404.

## Запуск ProjectB

Перейти до каталогу сервісу:

    cd project_b

Запустити Docker Compose:

    docker compose up -d

Перевірити контейнери:

    docker compose ps

Запустити тести:

    docker compose exec web pytest

Після запуску повернутися до кореня проєкту:

    cd ..

## Тести

Запуск усіх тестів:

    docker compose exec web pytest

Запуск тестів моделей:

    docker compose exec web pytest tests/test_models.py

## Coverage

Для перевірки покриття коду:

    docker compose exec web pytest --cov=. --cov-report=term-missing

Поточний результат:

    75 passed

Загальний coverage:

    89.49%

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