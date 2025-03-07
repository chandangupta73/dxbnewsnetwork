# Generated by Django 4.1 on 2023-12-18 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_management', '0008_alter_category_order_alter_newspost_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='videonews',
            name='BreakingNews',
            field=models.BooleanField(default=False, verbose_name='Breaking News'),
        ),
        migrations.AddField(
            model_name='videonews',
            name='Head_Lines',
            field=models.BooleanField(default=False, verbose_name='Head Lines'),
        ),
        migrations.AddField(
            model_name='videonews',
            name='articles',
            field=models.BooleanField(default=False, verbose_name='Articles'),
        ),
        migrations.AddField(
            model_name='videonews',
            name='trending',
            field=models.BooleanField(default=False, verbose_name='Trending'),
        ),
    ]
