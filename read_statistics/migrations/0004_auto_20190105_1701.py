# Generated by Django 2.1.4 on 2019-01-05 09:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0003_auto_20190105_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdetail',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
