# Generated by Django 4.1.2 on 2022-10-24 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usadba_app', '0017_opinion_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opinion',
            name='rate',
        ),
    ]
