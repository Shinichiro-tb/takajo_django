# Generated by Django 3.0.4 on 2020-11-30 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_lending_book_booking_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end',
            field=models.TimeField(blank=True, verbose_name='終了時間'),
        ),
    ]
