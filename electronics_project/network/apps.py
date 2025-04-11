from django.apps import AppConfig


class NetworkConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "network"

    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
        from django.db.utils import OperationalError, ProgrammingError

        try:
            interval_schedule, _ = IntervalSchedule.objects.get_or_create(
                every=3,
                period=IntervalSchedule.HOURS
            )
            if not PeriodicTask.objects.filter(name='Увеличивайте долг каждые 3 часа').exists():
                PeriodicTask.objects.create(
                    interval=interval_schedule,
                    name='Увеличивайте долг каждые 3 часа',
                    task='network.tasks.increase_debt',
                )

            crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
                minute='30',
                hour='6',
                day_of_week='*',
                day_of_month='*',
                month_of_year='*',
            )
            if not PeriodicTask.objects.filter(name='Уменьшить долг в 6:30').exists():
                PeriodicTask.objects.create(
                    crontab=crontab_schedule,
                    name='Уменьшить долг в 6:30',
                    task='network.tasks.decrease_debt',
            )
        except (OperationalError, ProgrammingError):
            pass
