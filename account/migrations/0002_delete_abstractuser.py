# Generated by Django 3.1 on 2020-08-20 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20200820_1019'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AbstractUser',
        ),
    ]
