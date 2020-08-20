from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# Create your models here.


def get_absolute(self):
    return reverse('prof-url'+self.pk, kwargs={'pk': self.pk})


User.get_absolute_url = get_absolute
