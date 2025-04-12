# Electronics Project

Django REST API-проект для управления сетью торговых узлов, сотрудниками и продуктами.  
Использует Celery для асинхронных задач, Redis как брокер, и PostgreSQL как базу данных.  

## Возможности

- API с авторизацией по токену (DRF)
- Связь объектов с конкретным пользователем
- Админ-панель Django
- Асинхронные задачи (очистка долгов, отправка QR-кодов)
- Swagger-документация
- Уведомления на email

## Запуск через Docker

Создание и запуск контейнеров:

```bash
docker-compose up --build
```

Остановка контейнеров:

```bash
docker-compose down
```

---

## Настройка `.env`

Создай файл `.env` рядом с `docker-compose.yml`:

```env
SECRET_KEY=your-secret-key
DEBUG=True

POSTGRES=True
DB_NAME_POST=your_db_name
DB_USER_POS=your_db_user
DB_PASSWORD_POS=your_db_password
DB_HOST_POS=db
DB_PORT_POS=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_ACCEPT_CONTENT=json
CELERY_TASK_SERIALIZER=json

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

---

## Проверка работы

После запуска контейнеров:

- Админка Django: [http://localhost:8000/admin](http://localhost:8000/admin)
- Swagger UI: [http://localhost:8000/swagger](http://localhost:8000/docs)

---

## Структура проекта

```
electronics_project/
│
├── electronics_project/      # Настройки Django
├── network/                  # Основное приложение
├── .env                      # Переменные окружения
├── Dockerfile                # Dockerfile
├── docker-compose.yml        # Конфигурация Docker Compose
├── requirements.txt          # Зависимости Python
├── start.sh                  # Скрипт запуска
└── manage.py
```

---

Всё готово для запуска и проверки работы приложения 🚀🔥


