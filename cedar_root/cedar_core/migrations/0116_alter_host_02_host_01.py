# Generated by Django 4.0.4 on 2022-05-29 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0115_remove_host_02_fk_host_02_host_01_id_host_02_host_01'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host_02',
            name='host_01',
            field=models.ForeignKey(help_text='The ID of the parent host', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.host_01'),
        ),
    ]