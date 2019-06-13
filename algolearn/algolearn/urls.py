"""algolearn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view
try:
    from algolearn.api.views import *
except Exception:
    pass
from api.views import *


from allauth.account.views import ConfirmEmailView


schema_view = get_swagger_view(title='Algolearn API')
admin.site.site_title = ""
admin.site.index_title = ""

urlpatterns = [
    url(r'^telebot/(?P<pk>[\w\-]+)/$', BotDetail.as_view(), name='agetbot'),
    url(r'^telebot/$', BotCreate.as_view(), name='add_bot'),
]

urlpatterns += [
    url(r'^api/courses/$', CourseList.as_view(), name='user-list'),
    url(r'^api/courses/(?P<pk>\d+)/$', CourseDetail.as_view(), name='user-detail'),
    url(r'^api/lectures/$', TheoryList.as_view(), name='lectures-list'),
    url(r'^api/lectures/(?P<pk>\d+)/$', TheoryDetail.as_view(), name='lectures-detail'),
    url(r'^api/quizes/$', QuizList.as_view(), name='lectures-list'),
    url(r'^api/quizes/(?P<pk>\d+)/$', QuizDetail.as_view(), name='lectures-detail'),
    url(r'^quiz/(?P<pk>\d+)/$', quiz, name='quiz'),
    url(r'^quizes/(?P<pk>\d+)/$', quizes, name='quizes'),
    url(r'^lectures/(?P<pk>\d+)/$', lectures, name='lectures'),

    url(r'^course/(?P<pk>\d+)/$', course, name='course'),


    url(r'^accounts/login/', alogin, name='login'),
    url(r'^checkin$', checkin, name='checkin'),
    url(r'^api/auth/registration/account-email-verification-sent/', null_view, name='account_email_verification_sent'),
    url(r'^api/auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    url(r'^api/auth/registration/complete/$', complete_view, name='account_confirm_complete'),
    url(r'^api/auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', null_view, name='password_reset_confirm'),
]

urlpatterns += [
    url(r'^$', main, name='main'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^profile/$', profile, name='profile'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^schema$', schema_view),
    path('admin/', admin.site.urls),
    url(r'^api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/auth/', include('rest_auth.urls')),
    # url(r'^api/auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    # url(r'^api/auth/twitter/$', TwitterLogin.as_view(), name='twitter_login')
]
