# Generated by Django 4.0.4 on 2022-06-21 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0137_rename_host_production_life_stage_host_02_host_life_stage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='production_stream',
            name='host_subs',
        ),
    ]
