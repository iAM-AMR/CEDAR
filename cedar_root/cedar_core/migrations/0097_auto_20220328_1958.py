# Generated by Django 3.1.7 on 2022-03-28 23:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0096_auto_20220325_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='res_outcome',
            name='extract_date_ro',
            field=models.DateField(default=datetime.datetime(2022, 3, 28, 19, 58, 13, 594057), help_text='The date at which the resistance outcome was extracted'),
        ),
    ]