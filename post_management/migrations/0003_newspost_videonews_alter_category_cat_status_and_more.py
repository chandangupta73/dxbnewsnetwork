# Generated by Django 4.1 on 2023-12-01 10:48

import autoslug.fields
import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('post_management', '0002_post_head_lines_post_articles_post_trending'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(default=None, max_length=65, null=True, verbose_name='News Head Line')),
                ('post_short_des', models.CharField(default=None, max_length=160, null=True, verbose_name='Short Discretion')),
                ('post_des', ckeditor_uploader.fields.RichTextUploadingField(default='No News', null=True, verbose_name='Long Discretion')),
                ('post_image', image_cropping.fields.ImageCropField(default=None, max_length=255, null=True, upload_to='blog/')),
                ('slug', autoslug.fields.AutoSlugField(default=None, editable=False, max_length=100, null=True, populate_from='post_title', unique=True)),
                ('post_tag', models.TextField(default='#trending #latest', null=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='Make Banner')),
                ('Head_Lines', models.BooleanField(default=False, verbose_name='Head Lines')),
                ('articles', models.BooleanField(default=False, verbose_name='Articles')),
                ('trending', models.BooleanField(default=False, verbose_name='Trending')),
                ('post_date', models.DateTimeField(auto_now=True)),
                ('post_status', models.IntegerField(default=0, null=True, verbose_name='Counter')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='VideoNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_title', models.CharField(default=None, max_length=60, null=True, verbose_name='Title (Lenth 60 Char)')),
                ('slug', autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='video_title', unique=True)),
                ('video_short_des', models.CharField(default=None, max_length=160, null=True, verbose_name='Meta/Short Des')),
                ('video_des', ckeditor_uploader.fields.RichTextUploadingField(default=None, null=True, verbose_name='Video Discretion')),
                ('video_url', models.CharField(default=True, max_length=255, null=True, verbose_name='Youtube Video URL')),
                ('video_tag', models.CharField(default=0, max_length=255, null=True)),
                ('video_date', models.DateTimeField(auto_now=True)),
                ('is_active', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=8, verbose_name='Status')),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='cat_status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=8, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='sub_category',
            name='subcat_status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=8, verbose_name='Status'),
        ),
        migrations.DeleteModel(
            name='post',
        ),
        migrations.AddField(
            model_name='videonews',
            name='News_Category',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='post_management.sub_category', verbose_name='Select Cetegory'),
        ),
        migrations.AddField(
            model_name='newspost',
            name='post_cat',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='post_management.sub_category', verbose_name='Select Cetegory'),
        ),
    ]
