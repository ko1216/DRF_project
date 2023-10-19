from django.db import models

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

    def __str__(self):
        return f'{self.title}, ссылка на урок: {self.video_link}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural ='Уроки'
