# Generated by Django 4.0.6 on 2022-07-07 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0161_alter_ast_method_hist_ast_method_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ast_breakpoint_source',
            new_name='ast_reference_standard',
        ),
        migrations.RenameField(
            model_name='ast_reference_standard',
            old_name='ast_breakpoint_std_accno',
            new_name='ast_reference_std_accno',
        ),
        migrations.RenameField(
            model_name='ast_reference_standard',
            old_name='ast_breakpoint_std_acronym',
            new_name='ast_reference_std_acronym',
        ),
        migrations.RenameField(
            model_name='ast_reference_standard',
            old_name='ast_breakpoint_std_desc',
            new_name='ast_reference_std_desc',
        ),
        migrations.RenameField(
            model_name='ast_reference_standard',
            old_name='ast_breakpoint_std',
            new_name='ast_reference_std_name',
        ),
    ]
