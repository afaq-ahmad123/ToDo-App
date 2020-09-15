from django.shortcuts import redirect, reverse
from .models import User


def login_required(some_function):
    def wrapper(*args, **kwargs):
        index = 1
        try:
            request = args[1]
        except IndexError:
            request = args[0]
            index = 0

        if 'user' in request.session:
            username = request.session['user']
        else:
            username = request.user.username

        if not username:
            return redirect(reverse('login-url'))
        user = User.objects.filter(username=username).first()
        args[index].user = user
        return some_function(*args, **kwargs)
    return wrapper
