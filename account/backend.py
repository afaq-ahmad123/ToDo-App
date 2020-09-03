from .models import User
from rest_framework.authtoken.models import Token


class AuthBackend(object):

    def authenticate(self, username=None, password=None, **kwargs):
        user = self.get_user(username)
        if user and user.check_password(password):
            return user
        else:
            None

    @staticmethod
    def login(request, user):
        for users in User.objects.all():
            Token.objects.get_or_create(user=users)
        request.session['user'] = user.username
        request.user = user
        request.auth = Token.objects.get(user=user).key
        request.session['token'] = Token.objects.get(user=user).key

    @staticmethod
    def logout(request):
        if 'user' in request.session:
            del request.session['user']
        if 'token' in request.session:
            del request.session['token']
        try:
            request.user = None
            request.auth = None
        except AttributeError:
            print("attr error")
        return request

    def get_user(self, user_id):
        try:
            user = User.objects.get(username=user_id)
            return user
        except User.DoesNotExist:
            return None
