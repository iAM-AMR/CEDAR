# Generated by Django 4.0.4 on 2022-05-29 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0100_alter_location_02_fk_location_02_location_01_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location_sub',
            name='iso_3166_1_alpha2',
            field=models.ForeignKey(db_column='iso_3166_1_alpha2', help_text='The ISO 3166 alpha-2 country code, i.e. "CA" for Canada', on_delete=django.db.models.deletion.DO_NOTHING, to='cedar_core.location_01', to_field='iso_country_code_2'),
        ),
    ]