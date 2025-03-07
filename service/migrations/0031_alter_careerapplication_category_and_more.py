# Generated by Django 4.1 on 2024-01-02 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post_management', '0011_alter_newspost_order'),
        ('service', '0030_careerapplication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='careerapplication',
            name='category',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='post_management.sub_category', verbose_name='Select Category'),
        ),
        migrations.AlterField(
            model_name='careerapplication',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='careerapplication',
            name='mobnumber',
            field=models.CharField(default=None, max_length=100, null=True, verbose_name='Contact Number'),
        ),
        migrations.AlterField(
            model_name='careerapplication',
            name='status',
            field=models.CharField(choices=[('selected', 'Selected'), ('NotSelected', 'Not Selected')], default='NotSelected', max_length=20, null=True),
        ),
    ]
