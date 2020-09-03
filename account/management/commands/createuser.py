from django.core.management.base import BaseCommand
from account.models import User
import random
import string


class Command(BaseCommand):

    def handle(self, *args, **options):
        i = 0
        letters = string.ascii_letters + string.digits
        mail_id = string.ascii_lowercase + string.digits
        while i < 1:
            i += 1
            username = ''.join(random.choice(letters) for i in range(10))
            password = ''.join(random.choice(letters) for i in range(10))
            email = ''.join(random.choice(mail_id) for i in range(6))
            email = email + '@gmail.com'
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                print(user)
                print(' '.join([user.username, user.email, password]))
            except ValueError as e:
                print(e)
                i -= 1
                continue

