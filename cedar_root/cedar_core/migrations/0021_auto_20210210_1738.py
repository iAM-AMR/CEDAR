# Generated by Django 3.1.5 on 2021-02-10 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0020_auto_20210210_1733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='factor',
            old_name='ID_factor_v0',
            new_name='factor_v0_id',
        ),
        migrations.RenameField(
            model_name='reference',
            old_name='DEP_analysis_unit_ID',
            new_name='DEP_analysis_unit_id',
        ),
        migrations.RenameField(
            model_name='reference',
            old_name='OLD_ID',
            new_name='OLD_country_id',
        ),
        migrations.RenameField(
            model_name='reference',
            old_name='OLD_countryID',
            new_name='OLD_id',
        ),
        migrations.RenameField(
            model_name='reference',
            old_name='OLD_status_ID',
            new_name='OLD_status_id',
        ),
    ]