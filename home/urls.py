from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth

urlpatterns = [
    re_path(r'^(?P<i>[0-9]+)/$', views.shortlist, name="home2-url"),
    path('', views.TaskListView.as_view(), name="home-url"),
    path('task-list-api/', views.TaskApi.as_view(), name="task_api"),
    re_path('^task-edit-api/(?P<pk>[0-9]+)$', views.TaskUpdateAPI.as_view()),
    re_path('^task-delete-api/(?P<pk>[0-9]+)$', views.TaskDeleteAPI.as_view()),
    # path('login/', auth.LoginView.as_view()),
    re_path(r'^delete/(?P<pk>[0-9]+)/$', views.delete, name="delete-url"),
    re_path(r'^edit/(?P<pk>[0-9]+)/$', views.TaskUpdateView.as_view(), name="edit-url"),
    re_path(r'^complete/(?P<pk>[0-9]+)/$', views.complete, name="complete-url"),
    re_path('^add/$', views.add_task, name='add-url'),
    re_path(r'^update/(?P<i>[0-9]+)/$', views.shortlist, name="update_tasks"),
]