# Generated by Django 4.0.4 on 2022-05-29 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0112_production_stream_host_subs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='production_stream',
            name='host_subs',
            field=models.ManyToManyField(db_table='production_stream_join_host_sub', to='cedar_core.host_02'),
        ),
    ]
