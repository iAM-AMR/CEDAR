# Generated by Django 4.0.4 on 2022-05-29 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0109_host_02_is_prod_stream_beef_production_stream'),
    ]

    operations = [
        migrations.RenameField(
            model_name='production_stream',
            old_name='host_main_id',
            new_name='host_main',
        ),
    ]
