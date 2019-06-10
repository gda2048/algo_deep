from django.db import models
from django.contrib.postgres.fields import JSONField


class Course(models.Model):
    """
    Stores all information about a course
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField('Название', max_length=30, unique=True)
    description = models.TextField('Описание', blank=True)
    photo = models.CharField('Фотография',max_length=100, null=True)
    topic = models.CharField('Тема', max_length=50)

    class Meta:
        """
        Course model settings
        """
        db_table = 'courses'
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """
        Stores all information about a lesson
        """
    id = models.AutoField(primary_key=True)
    name = models.CharField('Название', max_length=30, unique=True)
    description = models.TextField('Описание', blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        """
        Course model settings
        """
        db_table = 'lessons'
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Quiz(Lesson):
    lesson = models.OneToOneField(Lesson, parent_link=True, on_delete=models.CASCADE)
    questions = JSONField()
    answers = JSONField()

    class Meta:
        """
        Course model settings
        """
        db_table = 'quizes'
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'


class Theory(Lesson):
    lesson = models.OneToOneField(Lesson, parent_link=True, on_delete=models.CASCADE)
    theory_link = models.URLField(null=True)

    class Meta:
        """
        Course model settings
        """
        db_table = 'lections'
        verbose_name = 'теория'
        verbose_name_plural = 'теория'