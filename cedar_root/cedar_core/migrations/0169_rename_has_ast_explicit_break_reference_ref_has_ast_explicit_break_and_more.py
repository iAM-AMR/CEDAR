# Generated by Django 4.0.6 on 2022-07-08 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0168_rename_ref_has_ast_explicit_break_reference_hist_ref_has_ast_explicit_break_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reference',
            old_name='has_ast_explicit_break',
            new_name='ref_has_ast_explicit_break',
        ),
        migrations.RenameField(
            model_name='reference',
            old_name='has_ast_mic_table',
            new_name='ref_has_ast_mic_table',
        ),
    ]