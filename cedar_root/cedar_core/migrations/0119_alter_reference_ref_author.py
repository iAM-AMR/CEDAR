# Generated by Django 4.0.4 on 2022-05-29 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0118_alter_reference_ref_abstract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='ref_author',
            field=models.TextField(blank=True, default='', help_text='The name(s) or surname(s) of the authors, in the form of a comma-separated or semi-colon-separated list, i.e. "Chapman, Smith, Otten, Fazil" or "Howe, K.; Linton, A. H.; Osborne, A. D."'),
            preserve_default=False,
        ),
    ]