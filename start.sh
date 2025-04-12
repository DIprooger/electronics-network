#!/bin/bash

cd electronics_project

#!/bin/bash

echo "💡 Применяем миграции..."
python manage.py migrate
echo "🧪 Проверяем Celery..."
celery -A electronics_project inspect ping || echo "Celery не отвечает"
echo "🎉 Запускаем сервер..."
python manage.py runserver 0.0.0.0:8000
