from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название курса')
    preview = models.ImageField(verbose_name='Картинка', **NULLABLE)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=250, verbose_name='Урок')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(verbose_name='Картинка', **NULLABLE)
    video_link = models.URLField(verbose_name='Ссылка на урок')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, related_name='lessons', verbose_name='Курс')

    def __str__(self):
        return f'{self.title}, ссылка на урок: {self.video_link}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payments(models.Model):
    #  Я установил для всех FK полей SET_NULL, чтобы логи оплат не удалялись в случае удаления пользователя/курсов,
    #  так записи в этой таблице влияют на аналитические метрики
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, verbose_name='Пользователь')

    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, default=None, verbose_name='Курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, default=None, verbose_name='Урок', **NULLABLE)
    amount = models.IntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=50, verbose_name='Способ оплаты')

    def __str__(self):
        if self.course:
            return (
                f'Оплата {self.payment_method} за {self.course}.'
                f'Сумма оплаты {self.amount}, дата платежа: {self.date}'
                f'Плательщик: {self.user}'
                    )
        else:
            return (
                f'Оплата {self.payment_method} за {self.lesson}.'
                f'Сумма оплаты {self.amount}, дата платежа: {self.date}'
                f'Плательщик: {self.user}'
            )

    class Meta:
        verbose_name = 'Платежи'
        verbose_name_plural = 'Платежи'
