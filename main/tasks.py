import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from main.models import Subscription, Course
from users.models import User


@shared_task
def send_email(course_id):
    course = Course.objects.get(pk=course_id)
    users_email = []

    if Subscription.objects.filter(course=course_id).exists():
        subscriptions = Subscription.objects.filter(course=course_id)
        for subscription in subscriptions:
            users_email.append(subscription.user.email)

        email_message = EmailMultiAlternatives(
            subject=f'Курс {course.title} был изменен',
            body='Курс был обновлен, перейдите в материалы, чтобы не пропустить изменения',
            from_email=settings.EMAIL_HOST_USER,
            to=users_email
        )
        email_message.send()

    print('письмо отправлено')


def check_users_last_login():
    users = User.objects.all()
    current_time = datetime.datetime.now()
    print(f'Задача исполняется, время {current_time}')

    for user in users:
        delta = (current_time - user.last_login).total_seconds()
        if delta > 2419200:
            user.is_active = False
