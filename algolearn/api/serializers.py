from .models import Course
from rest_framework import serializers


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields=('id', 'name', 'description', 'topic')