# Generated by Django 4.0.6 on 2022-07-07 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0158_alter_ast_breakpoint_source_ast_breakpoint_std_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ast_method',
            new_name='ast_method_old',
        ),
    ]
