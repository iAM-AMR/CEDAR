# Generated by Django 4.0.4 on 2022-05-29 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0121_alter_reference_study_sample_method'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reference',
            old_name='fk_publisher_id',
            new_name='publisher',
        ),
        migrations.RenameField(
            model_name='reference',
            old_name='publish_name_alt',
            new_name='publisher_name_alt',
        ),
    ]
