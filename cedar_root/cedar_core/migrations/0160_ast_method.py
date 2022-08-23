# Generated by Django 4.0.6 on 2022-07-07 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0159_rename_ast_method_ast_method_old'),
    ]

    operations = [
        migrations.CreateModel(
            name='ast_method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ast_method_name', models.CharField(help_text=None, max_length=100)),
                ('ast_method_accno', models.CharField(help_text=None, max_length=100)),
                ('ast_method_type_name', models.CharField(help_text=None, max_length=100)),
                ('ast_method_type_accno', models.CharField(help_text=None, max_length=100)),
                ('ast_method_is_ast_type', models.BooleanField(help_text=None)),
                ('hist_ast_method_id', models.IntegerField(help_text=None, max_length=100)),
            ],
        ),
    ]