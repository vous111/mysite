# Generated by Django 2.1.4 on 2019-01-16 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likerecord',
            old_name='liked_num',
            new_name='liked_time',
        ),
    ]