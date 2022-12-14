# Generated by Django 4.1.2 on 2022-10-19 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usadba_app', '0012_remove_tomatoseeds_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tomatoseeds',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='usadba_app.seedscategories'),
        ),
        migrations.AddField(
            model_name='tomatoseeds',
            name='ripe_color',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='tomatoseeds',
            name='ripe_form',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tomatoseeds',
            name='ripe_weight_grams',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='tomatoseeds',
            name='ripening_period',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='usadba_app.ripeningperiods'),
        ),
        migrations.AddField(
            model_name='tomatoseeds',
            name='yield_kg_div_m2',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
