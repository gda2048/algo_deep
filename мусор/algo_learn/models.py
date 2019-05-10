from django.db import models
from django.utils import timezone


class Person(models.Model):
    pe_id = models.AutoField(primary_key=True)
    pe_login = models.CharField(max_length=20)
    pe_name = models.CharField(max_length=20)
    pe_surname = models.CharField(max_length=20)
    pe_patronymic = models.CharField(null=True, max_length=20)
    pe_email = models.EmailField()
    pe_birthdate = models.DateTimeField()
    pe_todaydate = models.DateTimeField()
    LOAN_STATUS = (
        ('s', 'Студент'),
        ('t', 'Преподаватель'),
    )
    pe_status = models.CharField(max_length=20, help_text="your status", choices=LOAN_STATUS, default='s')
    pe_admin = models.BooleanField(default=False, null=True)
    pe_password = models.CharField(max_length=20)
    pe_query = models.TextField(default='')

    class Meta:
        ordering = ["pe_name"]


class Student(models.Model):
    st_id = models.AutoField(primary_key=True)
    st_rate = models.IntegerField(default=0)
    st_profile = models.ForeignKey(Person, on_delete=models.CASCADE)


class Teacher(models.Model):
    te_id = models.AutoField(primary_key=True)
    te_profile = models.ForeignKey(Person, on_delete=models.CASCADE)


class Group(models.Model):
    gr_id = models.AutoField(primary_key=True)
    gr_name = models.CharField(max_length=20)
    gr_students = models.ManyToManyField(Student)
    gr_teachers = models.ManyToManyField(Teacher)


class Algorithm(models.Model):
    al_id = models.AutoField(primary_key=True)
    al_type=models.CharField(max_length=20)
    al_name=models.CharField(max_length=20)
    al_comment = models.CharField(max_length=200, null=True)
    al_theory = models.URLField(null=True)
    al_visualization = models.URLField(null=True)

    class Meta:
        ordering = ["al_name"]


class Problem(models.Model):
    pr_id = models.AutoField(primary_key=True)
    pr_name = models.CharField(max_length=20)
    pr_checkdate = models.DateTimeField()
    pr_algo = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    pr_group = models.ForeignKey(Group, on_delete=models.CASCADE)

    @property
    def is_past_due(self):
        return timezone.now() > self.pr_checkdate


    class Meta:
        ordering = ["pr_name"]


class Order(models.Model):
    order_problem = models.CharField(max_length=20)
    order_algorithm = models.CharField(max_length=20)
    order_group = models.CharField(max_length=20)
    order_teacher = models.CharField(max_length=20)
    order_student = models.CharField(max_length=20)
    order_person = models.CharField(max_length=20)


class Solving(models.Model):
    so_id = models.AutoField(primary_key=True)
    so_res = models.IntegerField(default=-1)
    so_todaydate = models.DateTimeField()
    so_problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    so_student = models.ForeignKey(Student, on_delete=models.CASCADE)

