from django.urls import path, re_path
from django.conf.urls import url, include
from django.contrib import admin
from algo_learn import views


from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Pastebin API')
urlpatterns = [
        url(r'^schema$', schema_view),
        re_path(r'^log_in/', views.log_in, name="login"),
        re_path(r'^log_out/', views.log_out, name="logout"),

        path('', views.index, name='index'),
        re_path(r'^index$', views.index, name='index'),
        re_path(r'order', views.order),
        re_path(r'arbitrary_q', views.arbitrary),
        re_path(r'search', views.search),

        re_path(r'^report1/', views.report1),
        re_path(r'^report2/', views.report2),
        re_path(r'^checkin', views.checkin),
        re_path(r'^group_me', views.group_me, name="group_me"),
        re_path(r'^admin/', admin.site.urls),
        re_path('(?P<pr_id>[0-9]+)/createsolving/', views.createsolving),

        re_path(r'solve/(?P<pr_id>[0-9]+)', views.solve),

        re_path(r'deletetask/(?P<pr_id>(\d+))/', views.deletetask),
        re_path(r'createtask/', views.createtask),
        re_path(r'edittask/(?P<pr_id>(\d+))/', views.edittask),
        path(r'problems/<int:gr_id>/', views.problems),

        path('create/', views.create),
        path('edit/<int:pe_id>/', views.edit),
        path('delete/<int:pe_id>/', views.delete),

        re_path(r'createalgo/', views.createalgo),
        re_path(r'editalgo/(?P<al_id>(\d+))', views.editalgo),
        re_path(r'deletealgo/(?P<al_id>(\d+))', views.deletealgo),
        re_path(r'^algonew', views.algonew),
        re_path(r'^tasknew', views.tasknew),
        re_path(r'editgr_people/(?P<gr_id>(\d+))/$', views.editgr_people),

        re_path(r'add/(?P<pe_id>(\d+))', views.add),
        re_path(r'del/(?P<pe_id>(\d+))', views.remove),
        re_path(r'creategroup/$', views.creategroup),
        re_path(r'editgroup/(?P<gr_id>(\d+))$', views.editgroup),
        re_path(r'deletegroup/(?P<gr_id>(\d+))$', views.deletegroup),
        re_path(r'^group_add/', views.group_add, name="group_add"),

]