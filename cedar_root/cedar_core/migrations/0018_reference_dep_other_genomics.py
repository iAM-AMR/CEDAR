# Generated by Django 3.1.5 on 2021-02-10 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0017_auto_20210210_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='DEP_other_genomics',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]