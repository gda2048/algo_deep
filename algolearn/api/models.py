from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User


class Course(models.Model):
    """
    Stores all information about a course
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField('Название', max_length=30, unique=True)
    description = models.TextField('Описание', blank=True)
    photo = models.CharField('Фотография',max_length=100, null=True)
    topic = models.CharField('Тема', max_length=50)
    type = models.CharField('Тип курса', max_length=50, default='Free')
    time = models.IntegerField('Время прохождения в часах', default=1)

    def __str__(self):
        return str(self.name)

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

    class Meta:
        """
        Course model settings
        """
        db_table = 'lessons'
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        abstract = True


class Quiz(Lesson):
    questions = JSONField(null=True)
    answers = JSONField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz_lessons')

    def __str__(self):
        return str(self.name)

    class Meta:
        """
        Course model settings
        """
        db_table = 'quizes'
        verbose_name = 'тест'
        verbose_name_plural = 'тесты'


class Theory(Lesson):
    link_description = models.CharField('Описание ссылки', max_length=100, null=True)
    theory_link = models.URLField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='theory_lessons')

    def __str__(self):
        return str(self.name)

    class Meta:
        """
        Course model settings
        """
        db_table = 'lections'
        verbose_name = 'теория'
        verbose_name_plural = 'теория'


class ChatBot(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login = models.CharField('Логин', max_length=30, primary_key=True)
    bot_id = models.CharField('id', max_length=20, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        """
        Chatbot model settings
        """
        db_table = 'telebot'
        verbose_name = 'бот'
        verbose_name_plural = 'боты'


class Solution(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    res = models.IntegerField('Результат', default=0)

    def __str__(self):
        return str(self.user.username)+' '+str(self.quiz.name)
