# Generated by Django 4.1.2 on 2022-11-05 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usadba_app', '0018_remove_opinion_rate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='Cart',
        ),
        migrations.RenameModel(
            old_name='OrderAndProduct',
            new_name='CartAndProduct',
        ),
    ]
