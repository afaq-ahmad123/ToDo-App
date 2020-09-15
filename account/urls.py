from . import views
from django.urls import path, re_path

urlpatterns = [
    path('login/', views.login_view, name="login-url"),
    path('register/', views.signup_view, name="sign-url"),
    path('logout/', views.logout_user, name="logout-url"),
    path('user-list-api/', views.UserListAPI.as_view()),
    path('auth-api/', views.AuthenticationAPI.as_view()),
    re_path('^user-edit-api/(?P<id>[0-9]+)$', views.UserUpdateAPI.as_view()),
    re_path(r'^prof/(?P<pk>[0-9]+)/$', views.EditProfile.as_view(), name="prof-url"),
]