# Generated by Django 2.1.4 on 2018-12-29 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20181228_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='aa',
            field=models.DateTimeField(auto_now=True),
        ),
    ]