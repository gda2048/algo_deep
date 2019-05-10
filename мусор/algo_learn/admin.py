from django.contrib import admin
from .models import Person, Algorithm, Problem, Student, Teacher, Group


admin.site.register(Person)
admin.site.register(Algorithm)
admin.site.register(Problem)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Group)

