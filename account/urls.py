from . import views
from django.urls import path, re_path

urlpatterns = [
    path('login/', views.login_view, name="login-url"),
    path('register/', views.signup_view, name="sign-url"),
    path('logout/', views.log_user, name="logout-url"),
    re_path(r'^prof/(?P<pk>[0-9]+)/$', views.EditProfile.as_view(), name="prof-url"),
]