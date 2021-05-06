# Generated by Django 3.1.5 on 2021-02-11 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0023_auto_20210211_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='CEDAR_extract_east',
            field=models.BooleanField(blank=True, help_text='Specifies whether this reference is to be extracted by the "east" team (i.e. Guelph/ON)', null=True),
        ),
    ]