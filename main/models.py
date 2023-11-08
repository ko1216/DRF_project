from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название курса')
    preview = models.ImageField(verbose_name='Картинка', **NULLABLE)
    description = models.TextField(verbose_name='Описание')
    monthly_price_rub = models.IntegerField(default=100000, verbose_name='Стоимость месячной подписки', **NULLABLE)
    price_rub = models.IntegerField(default=200000, verbose_name='Стоимость оплаты в рублях', **NULLABLE)
    last_updated = models.DateTimeField(verbose_name='Послдеднее обновление', **NULLABLE)

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
    last_updated = models.DateTimeField(verbose_name='Послдеднее обновление', **NULLABLE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, related_name='lessons', verbose_name='Курс')

    def __str__(self):
        return f'{self.title}, ссылка на урок: {self.video_link}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Subscription(models.Model):
    is_active = models.BooleanField(default=False, verbose_name='Активно')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='subscription')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f'Подписка {self.user} на курс: {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class PaymentMethod(models.TextChoices):
    cash = 'наличными'
    card = 'по карте'


class Payments(models.Model):
    #  Я установил для всех FK полей SET_NULL, чтобы логи оплат не удалялись в случае удаления пользователя/курсов,
    #  так записи в этой таблице влияют на аналитические метрики
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, verbose_name='Пользователь')

    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, default=None, verbose_name='Курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, default=None, verbose_name='Урок', **NULLABLE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, default=None, verbose_name='Подписка', **NULLABLE)
    amount = models.IntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=9, choices=PaymentMethod.choices, default=PaymentMethod.card, verbose_name='Способ оплаты')

    card_number = models.CharField(max_length=16, verbose_name='Номер карты', **NULLABLE)
    expiration_date = models.CharField(max_length=7, verbose_name='Дата окончания срока действия карты', **NULLABLE)
    cvc = models.CharField(max_length=3, verbose_name='CVC-код', **NULLABLE)
    payment_id = models.CharField(max_length=100, verbose_name='ID платежа', **NULLABLE)

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
