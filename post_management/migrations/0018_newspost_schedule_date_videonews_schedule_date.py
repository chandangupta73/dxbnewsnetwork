# Generated by Django 4.1 on 2024-03-22 08:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post_management', '0017_alter_videonews_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspost',
            name='schedule_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Schedule Date'),
        ),
        migrations.AddField(
            model_name='videonews',
            name='schedule_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Schedule Date'),
        ),
    ]
