# Generated by Django 2.0.5 on 2018-05-16 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='display_name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
