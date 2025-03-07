# Generated by Django 4.1 on 2024-01-18 16:31

from django.db import migrations, models
import django.utils.timezone
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('post_management', '0013_newspost_event_newspost_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='newspost',
            name='Eventend_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Event End Date'),
        ),
        migrations.AddField(
            model_name='newspost',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='newspost',
            name='viewcounter',
            field=models.IntegerField(default=0, null=True, verbose_name='Views'),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='Event_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Event Start Date'),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='is_active',
            field=models.BooleanField(default=True, null=True, verbose_name='Latest News'),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='order',
            field=models.IntegerField(default=5, null=True, verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='post_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='newspost',
            name='post_image',
            field=image_cropping.fields.ImageCropField(default=None, max_length=255, null=True, upload_to='blog/', verbose_name='News Image (1200X750px)'),
        ),
    ]
