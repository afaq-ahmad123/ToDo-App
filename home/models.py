from django.db import models
# from django.contrib.auth import get_user_model
from account.models import User
from datetime import datetime
from django.urls import reverse

# Create your models here.
# User = get_user_model()


class TaskModel(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100)
    complete = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
                        User,
                        on_delete=models.CASCADE,
                    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('edit-url', kwargs={'pk': self.pk})

