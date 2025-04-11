#!/bin/bash

cd electronics_project

gnome-terminal -- bash -c "source ../venv/bin/activate && python manage.py runserver"
gnome-terminal -- bash -c "source ../venv/bin/activate && celery -A electronics_project worker --loglevel=info"
gnome-terminal -- bash -c "source ../venv/bin/activate && celery -A electronics_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler"
