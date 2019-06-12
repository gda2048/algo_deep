from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.account.signals import email_confirmed
from allauth.account.decorators import verified_email_required
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from .models import *
from .forms import SignUpForm
from django.dispatch import receiver
from .serializers import CourseSerializer, TheorySerializer, QuizSerializer, BotSerializer
import json
import requests


class CourseList(generics.ListAPIView):
    """
    API endpoint that represents a list of course.
    """
    model = Course
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseDetail(generics.RetrieveAPIView):
    """
    API endpoint that represents a single course.
    """
    model = Course
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class TheoryDetail(generics.RetrieveAPIView):
    """
    API endpoint that represents a single theory lesson.
    """
    model = Theory
    serializer_class = TheorySerializer
    queryset = Theory.objects.all()


class BotDetail(generics.RetrieveAPIView):
    """
    API endpoint that represents a single bot detail
    """
    model = ChatBot
    serializer_class = BotSerializer
    queryset = ChatBot.objects.all()


class BotCreate(generics.CreateAPIView):
    """
    API endpoint that represents a single bot detail
    """
    model = ChatBot
    serializer_class = BotSerializer
    queryset = ChatBot.objects.all()

    def create(self, request, *args, **kwargs):
        ChatBot.objects.filter(login=request.data['login']).update(bot_id=request.data['bot_id'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TheoryList(generics.ListAPIView):
    """
    API endpoint that represents a list of theory lessons.
    """
    model = Theory
    serializer_class = TheorySerializer
    queryset = Theory.objects.all()


class QuizDetail(generics.RetrieveAPIView):
    """
    API endpoint that represents a single theory lesson.
    """
    model = Quiz
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()


class QuizList(generics.ListAPIView):
    """
    API endpoint that represents a list of theory lessons.
    """
    model = Quiz
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()


@verified_email_required
def profile(request):
    if request.method == 'POST' and request.user.is_authenticated:
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.username = request.POST.get('username')
        telebot = request.POST.get('telebot')
        if telebot:
            try:
                ChatBot.objects.create(user=request.user, login=telebot).save()
            except Exception:
                ChatBot.objects.filter(user=request.user).update(login=telebot)

        request.user.save()
        return HttpResponseRedirect("/")
    telebot = ChatBot.objects.filter(user=request.user)
    if telebot:
        return render(request, "profile.html", {"bot": telebot[0].login})
    else:
        return render(request, "profile.html")


def checkin(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password1')
            url = "http://"+request.get_host() + '/api/auth/registration/'
            data = { "username": username, "email": email, "password1": password1, "password2": password2}
            headers = {'Content-type': 'application/json'}
            try:
                res = requests.post(url, data=json.dumps(data), headers=headers, timeout=5)
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                res = "No response or Timeout"
            return redirect('/accounts/confirm-email/')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration.html', {'form': form})


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = User.objects.get(email=email_address.email)
    user.is_active = True
    user.save()


def main(request, *args):
    courses = Course.objects.all()
    return render(request, "main.html", {'courses': courses})


def alogin(request, *args):
    return redirect("/login")


def quiz(request, pk):
    try:
        quiz_pk = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        raise Http404("Нет такого теста")
    return render(request, "quiz.html", {"quiz": quiz_pk})


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


@api_view()
def null_view(request):
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view()
def complete_view(request):
    return Response("Email account is activated")







