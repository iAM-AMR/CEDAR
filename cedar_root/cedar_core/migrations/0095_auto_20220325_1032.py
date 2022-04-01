# Generated by Django 3.1.7 on 2022-03-25 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0094_auto_20220325_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='res_outcome',
            name='place_in_text',
            field=models.TextField(blank=True, help_text='The location of the resistance outcome data in-text, i.e. "Table 2". If the data is from the body of the text, use the page and paragraph numbers (Pg. and Para. respectively)', null=True),
        ),
    ]
