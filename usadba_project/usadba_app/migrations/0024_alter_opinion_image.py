# Generated by Django 4.1.2 on 2022-11-05 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usadba_app', '0023_alter_opinion_image_alter_opinion_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='opinion'),
        ),
    ]
