# Generated by Django 3.1.7 on 2021-09-10 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0053_auto_20210910_1253'),
    ]

    operations = [
        migrations.DeleteModel(
            name='reference_history_join',
        ),
    ]