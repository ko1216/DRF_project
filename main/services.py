# import json
# from datetime import datetime
#
# from django_celery_beat.models import IntervalSchedule, PeriodicTask
#
#
# def set_schedule(*args, **kwargs):
#     schedule, created = IntervalSchedule.objects.get_or_create(
#         every=10,
#         period=IntervalSchedule.SECONDS,
#     )
#
#     start_time = datetime.now().replace(hour=18, minute=25, second=0)
#
#     PeriodicTask.objects.create(
#         interval=schedule,
#         name='check_users_last_login',
#         task='main.tasks.check_users_last_login',
#         args=json.dumps([]),
#         start_time=start_time,
#     )
