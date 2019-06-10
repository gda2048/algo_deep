from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.registration.views import SocialLoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from .models import *
from .forms import SignUpForm
import requests
import json


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
            print(res)
            print(url)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration.html', {'form': form})



def main(request, *args):
    courses = Course.objects.all()
    return render(request, "main.html", {'courses': courses})


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