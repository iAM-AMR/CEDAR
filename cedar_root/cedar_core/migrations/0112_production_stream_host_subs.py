# Generated by Django 4.0.4 on 2022-05-29 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0111_alter_production_stream_host_main'),
    ]

    operations = [
        migrations.AddField(
            model_name='production_stream',
            name='host_subs',
            field=models.ManyToManyField(to='cedar_core.host_02'),
        ),
    ]
