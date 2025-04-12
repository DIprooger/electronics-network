# 🚀 Electronics Project

Django REST API-проект для управления сетью торговых узлов, сотрудниками и продуктами.  
Использует Celery для асинхронных задач, Redis как брокер, и PostgreSQL как базу данных.  

## 📦 Возможности

- API с авторизацией по токену (DRF)
- Связь объектов с конкретным пользователем
- Админ-панель Django
- Асинхронные задачи (очистка долгов, отправка QR-кодов)
- Swagger-документация
- Уведомления на email

---

## 🚀 Быстрый запуск

Проект запускается **одной командой**:

```bash
./start.sh
```

> Убедись, что скрипт имеет права на выполнение (`chmod +x start.sh`).

---

## ⚙️ Настройка `.env`

Создай файл `.env` в корне проекта (на одном уровне с `manage.py`) и пропиши переменные:

```env
# 🔐 Секретный ключ Django
SECRET_KEY=your-secret-key

# 🔧 Режим отладки
DEBUG=True

# 🗄️ Использовать PostgreSQL (True) или SQLite (False)
POSTGRES=True

# 📚 Настройки базы данных PostgreSQL
DB_NAME_POST=your_db_name
DB_USER_POS=your_db_user
DB_PASSWORD_POS=your_db_password
DB_HOST_POS=localhost
DB_PORT_POS=5432

# 🐇 Настройки Celery и Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_ACCEPT_CONTENT=json
CELERY_TASK_SERIALIZER=json

# 📧 Email-настройки для отправки писем
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

> Для отправки писем через Gmail нужно создать **пароль приложения** (не обычный пароль).

---

## ✅ Как протестировать

После запуска:

1. Перейди в [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) — админка Django  
2. Перейди в [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) — Swagger UI  
3. Зарегистрируйся через `/register/` и получи токен  
4. Подставь токен в Swagger (кнопка "Authorize")  
5. Создавай и редактируй свои объекты: `nodes`, `products`, `employees` — всё ограничено по пользователю  
6. Запусти Celery в отдельном окне:
   ```bash
   celery -A electronics_project worker -l info
   ```
---

## 📁 Структура проекта

```
electronics_project/
│
├── electronics_project/      # Настройки проекта
├── network/                  # Основное приложение
├── .env                      # Настройки окружения
├── start.sh                  # Скрипт для запуска
└── manage.py
```

---

## 🔧 Зависимости

Устанавливаются автоматически при запуске скрипта, но если нужно вручную:

```bash
pip install -r requirements.txt
```

> Убедись, что у тебя установлен и запущен Redis:
```bash
sudo apt install redis
redis-server
```

---

## 📫 Обратная связь

Если что-то не работает — смотри логи Celery, проверяй `.env` и консоль Django.  
Всё остальное уже готово для запуска и тестов 🔥