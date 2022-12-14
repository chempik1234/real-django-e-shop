# Generated by Django 4.1.2 on 2022-10-15 14:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import usadba_app.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usadba_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroundType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=8)),
            ],
            options={
                'db_table': 'ground_type',
            },
        ),
        migrations.CreateModel(
            name='RipeningPeriods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'ripening_periods',
            },
        ),
        migrations.CreateModel(
            name='SeedsCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'seed_categories',
            },
        ),
        migrations.CreateModel(
            name='TomatoTypeOfPlant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=19)),
            ],
            options={
                'db_table': 'tomato_type_of_plant',
            },
        ),
        migrations.RenameField(
            model_name='opinion',
            old_name='pr_type',
            new_name='pr_table',
        ),
        migrations.RemoveField(
            model_name='opinion',
            name='pr_title',
        ),
        migrations.AddField(
            model_name='opinion',
            name='pr_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='opinion',
            name='text',
            field=models.CharField(max_length=1200, null=True),
        ),
        migrations.AlterModelTable(
            name='opinion',
            table='opinion',
        ),
        migrations.CreateModel(
            name='TomatoSeeds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ripe_form', models.CharField(max_length=40, null=True)),
                ('ground_growing_conditions', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usadba_app.groundtype')),
                ('type_of_plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usadba_app.tomatotypeofplant')),
            ],
            options={
                'db_table': 'tomato_seeds',
            },
            bases=(models.Model, usadba_app.models.SimpleSeeds),
        ),
        migrations.CreateModel(
            name='Rates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('pr_table', models.CharField(max_length=255, null=True)),
                ('pr_id', models.IntegerField(null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'rates',
            },
        ),
    ]
