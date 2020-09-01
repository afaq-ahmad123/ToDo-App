from .models import User


class AuthBackend(object):

    def authenticate(self, username=None, password=None, **kwargs):
        user = self.get_user(username)
        if user and user.check_password(password):
            return user
        else:
            None

    @staticmethod
    def login(request, user):
        request.session['user'] = user.username
        request.user = user
        # return

    @staticmethod
    def logout(request):
        if 'user' in request.session:
            del request.session['user']
        try:
            print(request.user)
            del request.user
            print(request.user)
        except AttributeError:
            print("attr error")
        return request

    def get_user(self, user_id):
        try:
            user = User.objects.get(username=user_id)
            return user
        except User.DoesNotExist:
            return None
