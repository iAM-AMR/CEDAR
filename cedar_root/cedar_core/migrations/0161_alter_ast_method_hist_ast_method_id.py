# Generated by Django 4.0.6 on 2022-07-07 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0160_ast_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ast_method',
            name='hist_ast_method_id',
            field=models.IntegerField(help_text=None),
        ),
    ]
