import json
from datetime import datetime

from django_celery_beat.models import IntervalSchedule, PeriodicTask


def set_schedule(*args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=5,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.create(
        interval=schedule,
        name='Ban user if inactive for 28 days',
        task='main.tasks.check_users_last_login',
        args=json.dumps([]),
    )
