from .models import Course, Theory, Quiz, ChatBot
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    quiz_lessons = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    theory_lessons = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'topic', 'quiz_lessons', 'theory_lessons', 'type', 'time')


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = ('id', 'name', 'description', 'questions', 'course')


class TheorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Theory
        fields = ('id', 'name', 'description', 'theory_link', 'link_description', 'course')


class BotSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatBot
        fields = ('login', 'bot_id')
