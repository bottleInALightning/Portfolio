from django.urls import path

from . import views


urlpatterns = [
    path('', views.index),
    path("projects/",views.projects),
    path("blog/",views.blog),
    path("comments/",views.comment),
    path("personal/",views.personal),
    path("login_page/",views.login_page),
    path("register/",views.register),
    path("login_page/logout",views.logout_page),
]