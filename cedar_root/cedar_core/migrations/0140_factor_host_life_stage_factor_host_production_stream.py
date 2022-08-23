# Generated by Django 4.0.4 on 2022-06-21 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0139_rename_host_main_production_stream_host_level_01'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='host_life_stage',
            field=models.ForeignKey(help_text='[ID] The host animal life stage (e.g., "Egg", "Chick", "Adult"; "Calf", "Heifer", "Backgrounder").', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.host_life_stage'),
        ),
        migrations.AddField(
            model_name='factor',
            name='host_production_stream',
            field=models.ForeignKey(help_text='[ID] The host animal production stream (e.g., "Beef Cattle", "Dairy Cattle").', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.production_stream'),
        ),
    ]