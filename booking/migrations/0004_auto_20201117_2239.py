# Generated by Django 3.0.4 on 2020-11-17 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_lending_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lending_book',
            name='biketype',
        ),
        migrations.AddField(
            model_name='lending_book',
            name='l_biketype',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='booking.Biketype', verbose_name='利用自転車'),
            preserve_default=False,
        ),
    ]