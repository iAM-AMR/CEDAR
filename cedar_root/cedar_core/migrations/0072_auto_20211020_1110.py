# Generated by Django 3.1.7 on 2021-10-20 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0071_auto_20211020_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='res_outcome',
            name='urid',
            field=models.PositiveIntegerField(blank=True, help_text='The canonical resistance outcome ID. The URID is shared between resistance outcomes (ROs) that have been extracted in duplicate', null=True),
        ),
    ]