from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_view, name="login-url"),
    path('register/', views.signup_view, name="sign-url"),
    path('logout/', views.log_user, name="logout-url"),
    path('edit/', views.edit_profile, name="edit-url")
]