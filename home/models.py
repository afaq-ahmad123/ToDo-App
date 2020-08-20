from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django.urls import reverse

# Create your models here.
User = get_user_model()


class HomeModel(models.Model):
    name = models.CharField(max_length=100)
    complete = models.BooleanField()
    created = datetime.now()
    user = models.ForeignKey(
                        User,
                        on_delete=models.CASCADE,
                    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('edit-url', kwargs={'pk': self.pk})
