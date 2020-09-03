from django.core.management.base import BaseCommand
from home.models import TaskModel
from datetime import datetime, timedelta


class Command(BaseCommand):

    def handle(self, *args, **options):
        tasks = TaskModel.objects.filter(created_at__lte=datetime.now()-timedelta(hours=24))
        for task in tasks:
            if not task.complete:
                task.complete = True
                task.save()
        print(tasks)
