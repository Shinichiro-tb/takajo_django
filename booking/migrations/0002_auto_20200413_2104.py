# Generated by Django 3.0.4 on 2020-04-13 12:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='利用日'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.TimeField(verbose_name='終了時間'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start',
            field=models.TimeField(verbose_name='開始時間'),
        ),
    ]
