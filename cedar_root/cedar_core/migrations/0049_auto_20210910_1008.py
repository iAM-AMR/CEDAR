# Generated by Django 3.1.7 on 2021-09-10 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0048_auto_20210909_1515'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reference',
            old_name='ref_has_mic_table',
            new_name='ref_has_ast_mic_table',
        ),
        migrations.RemoveField(
            model_name='reference',
            name='ref_has_explicit_break',
        ),
    ]
