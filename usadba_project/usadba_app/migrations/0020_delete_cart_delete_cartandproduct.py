# Generated by Django 4.1.2 on 2022-11-05 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usadba_app', '0019_rename_order_cart_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartAndProduct',
        ),
    ]