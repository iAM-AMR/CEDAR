# Generated by Django 3.1.7 on 2022-03-29 00:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0097_auto_20220328_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='res_outcome',
            name='extract_date_ro',
            field=models.DateField(default=datetime.datetime(2022, 3, 29, 0, 1, 51, 395175, tzinfo=utc), help_text='The date at which the resistance outcome was extracted'),
        ),
    ]