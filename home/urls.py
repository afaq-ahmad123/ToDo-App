from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    path('', views.home, name="home-url"),
    path('login/', auth.LoginView.as_view()),
    re_path(r'^(?P<pk>[0-9]+)/$', views.delete, name="delete-url"),
    re_path(r'^complete/(?P<pk>[0-9]+)/$', views.complete, name="complete-url"),
    path('add/', views.add_task, name='add-url')
]