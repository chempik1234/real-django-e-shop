# Generated by Django 4.1.2 on 2022-10-19 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usadba_app', '0011_tomatoseeds_delete_simpleseeds'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tomatoseeds',
            name='category',
        ),
        migrations.RemoveField(
            model_name='tomatoseeds',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tomatoseeds',
            name='name',
        ),
        migrations.RemoveField(
            model_name='tomatoseeds',
            name='price',
        ),
        migrations.RemoveField(
            model_name='tomatoseeds',
            name='ripe_color',
        ),
        migrations.RemoveField(
            model_name='tomatoseeds',
            name='ripe_form',
        ),
        migrations.RemoveField(
            model_name='tomatoseeds',
            name='ripe_weight_grams',
        ),
        migrations.RemoveField(
            model_name='tomatoseeds',
            name='ripening_period',
        ),
        migrations.RemoveField(
            model_name='tomatoseeds',
            name='yield_kg_div_m2',
        ),
    ]
