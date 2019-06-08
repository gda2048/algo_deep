from django.db import models
from algolearn.settings import IMAGES


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
