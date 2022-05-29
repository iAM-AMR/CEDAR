# Generated by Django 3.1.7 on 2022-03-08 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0078_auto_20220304_1319'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reference',
            old_name='archived_why',
            new_name='archived_reason',
        ),
        migrations.AddField(
            model_name='reference',
            name='capture_2019_reject',
            field=models.BooleanField(blank=True, help_text='The reference was captured in the 2019 literature search', null=True),
        ),
    ]