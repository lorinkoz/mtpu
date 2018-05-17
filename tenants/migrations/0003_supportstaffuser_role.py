# Generated by Django 2.0.5 on 2018-05-17 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0002_auto_20180517_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportstaffuser',
            name='role',
            field=models.PositiveIntegerField(choices=[(1, 'assistant'), (2, 'bodyguard'), (3, 'billing manager'), (4, 'mentor')], default=1),
        ),
    ]