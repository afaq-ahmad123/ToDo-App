from django.shortcuts import redirect, reverse
from .models import User


def login_required(some_function):
    def wrapper(*args, **kwargs):
        index = 1
        username = ''
        while index >= 0:
            try:
                if 'user' in args[index].session:
                    username = args[index].session['user']
                else:
                    # print(index)
                    username = args[index].user.username
                    # print(username)
                break
            except IndexError:
                index -= 1
                continue
            except AttributeError:
                break
        # print("out of loop")
        # print(username)
        if not username:
            return redirect(reverse('login-url'))
        user = User.objects.filter(username=username).first()
        args[index].user = user
        return some_function(*args, **kwargs)
    return wrapper
