# Generated by Django 4.0.4 on 2022-05-30 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0133_reference_join_location_hist_join_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='reference_join_location_fix',
        ),
    ]