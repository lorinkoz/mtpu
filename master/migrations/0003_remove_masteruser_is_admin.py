# Generated by Django 2.0.5 on 2018-05-17 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_masteruser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='masteruser',
            name='is_admin',
        ),
    ]
