# Generated by Django 2.0.4 on 2018-05-15 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180508_0339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='city',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='date_birth',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='description',
        ),
    ]
