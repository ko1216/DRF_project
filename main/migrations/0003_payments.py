# Generated by Django 4.2.6 on 2023-10-20 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_lesson_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')),
                ('amount', models.IntegerField(verbose_name='Сумма оплаты')),
                ('payment_method', models.CharField(max_length=50, verbose_name='Способ оплаты')),
                ('course', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.course', verbose_name='Курс')),
                ('lesson', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.lesson', verbose_name='Урок')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Платежи',
                'verbose_name_plural': 'Платежи',
            },
        ),
    ]