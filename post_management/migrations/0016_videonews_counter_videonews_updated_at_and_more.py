# Generated by Django 4.1 on 2024-02-01 08:26

from django.db import migrations, models
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('post_management', '0015_alter_newspost_post_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='videonews',
            name='counter',
            field=models.IntegerField(default=0, null=True, verbose_name='counter'),
        ),
        migrations.AddField(
            model_name='videonews',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='videonews',
            name='video_thumbnail',
            field=image_cropping.fields.ImageCropField(default=None, max_length=255, null=True, upload_to='thumbnail/', verbose_name='Thumbnail (1280X720px)'),
        ),
        migrations.AddField(
            model_name='videonews',
            name='video_type',
            field=models.CharField(choices=[('video', 'Video'), ('reel', 'Reel')], default='video', max_length=8, verbose_name='Video Type'),
        ),
        migrations.AddField(
            model_name='videonews',
            name='viewcounter',
            field=models.IntegerField(default=0, null=True, verbose_name='Views'),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='post_image',
            field=image_cropping.fields.ImageCropField(default=None, max_length=255, null=True, upload_to='blog/', verbose_name='News Image (1280X720px)'),
        ),
        migrations.AlterField(
            model_name='videonews',
            name='video_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
