# Generated by Django 3.1 on 2020-08-19 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_homemodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homemodel',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
