from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.account.signals import email_confirmed
from allauth.account.decorators import verified_email_required
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from .models import *
from .forms import SignUpForm
from django.dispatch import receiver
from .serializers import CourseSerializer, TheorySerializer, QuizSerializer, BotSerializer
import json
import requests
import coderunner


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
        """
        TODO delete this create
        doesn't work correctly
        """
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
        bot = request.POST.get('telebot')
        if bot:
            try:
                ChatBot.objects.create(user=request.user, login=bot).save()
            except Exception:
                ChatBot.objects.filter(user=request.user).update(login=bot)

        request.user.save()
        return HttpResponseRedirect("/")
    bot = ChatBot.objects.filter(user=request.user)
    if bot:
        return render(request, "profile.html", {"bot": bot[0].login})
    else:
        return render(request, "profile.html")


def checkin(request):
    """
    To checkin
    """
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
                requests.post(url, data=json.dumps(data), headers=headers, timeout=5)
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                pass
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


@verified_email_required
def list_courses(request, *args):
    courses = Course.objects.all()
    return render(request, "list_course.html", {'courses': courses})


def alogin(request, *args):
    return redirect("/login")


@verified_email_required
def lecture(request, pk):
    try:
        l = Theory.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        raise Http404("Нет такой лекции")
    return render(request, "lecture.html", {"lecture": l, 'course': l.course.id})


@verified_email_required
def list_courses(request, *args):
    courses = Course.objects.all()
    return render(request, "list_course.html", {'courses': courses})


@verified_email_required
def quiz(request, pk):
    try:
        quiz_pk = Quiz.objects.get(pk=pk)
        que_type = quiz_pk.questions['questions'][0]['type']
        que_score = int(quiz_pk.answers['answers'][0]['score'])
        que = quiz_pk.questions['questions'][0]
        render_dict = {"quiz": que, 'error': '', 'user_ans': '', 'course': quiz_pk.course.id}
        if request.method == 'POST':
            if que_type == 'code':
                user_ans = {"answers": [{"answer": [request.POST['editor']]}]}
                render_dict['user_ans'] = request.POST['editor']
                try:
                    res = coderunner.Checker(quiz_pk.questions, quiz_pk.answers, user_ans)
                    if res.res == -1:
                        return render(request, "quiz.html", {**render_dict, **{'error': "Ошибка в вашем коде"}})
                    que_score *= len(quiz_pk.answers['answers'][0]['answer'])
                    return add_solution(request, quiz_pk, res.res, que_score, render_dict)
                except TimeoutError:
                    return render(request, "quiz.html", {**render_dict, **{'error': 'TIME LIMIT'}})

            elif que_type in ['checkbox', 'radio']:
                user_ans = {"answers": [{"answer": request.POST.getlist('checks')}]}
                res = coderunner.Checker(quiz_pk.questions, quiz_pk.answers, user_ans)
                return add_solution(request, quiz_pk, res.res, que_score, render_dict)

            elif que_type == 'text':
                user_ans = {"answers": [{"answer": [request.POST['text']]}]}
                res = coderunner.Checker(quiz_pk.questions, quiz_pk.answers, user_ans)
                return add_solution(request, quiz_pk, res.res, que_score, render_dict)

    except Quiz.DoesNotExist:
        raise Http404("Нет такого теста")
    return render(request, "quiz.html", render_dict)


def add_solution(request, quiz_pk, res, score, render_dict):
    if res == score:
        if Solution.objects.filter(user=request.user, quiz=quiz_pk).exists():
            return render(request, "quiz.html",
                          {**render_dict, **{'error': 'Идеально. Еще одно решение. Баллы засчитаны уже за первое'}})
        Solution.objects.create(user=request.user, quiz=quiz_pk, res=res)
        return render(request, "quiz.html", {**render_dict, **{'error': 'Идеально ' + str(res) + ' scores получено'}})
    return render(request, "quiz.html", {**render_dict, **{'error': 'Eще строит поработать'}})


@verified_email_required
def course(request, pk):
    try:
        course_pk = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        raise Http404("Нет такого курса")
    return render(request, "course.html", {"course": course_pk, 'error': '', 'user_ans': ''})


@verified_email_required
def quizes(request, pk):
    q_es = Quiz.objects.filter(course_id=pk)
    return render(request, "quizes.html", {"quizes": q_es, "course": pk})


@verified_email_required
def lectures(request, pk):
    q_es = Theory.objects.filter(course_id=pk)
    return render(request, "lectures.html", {"lectures": q_es, "course": pk})


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







