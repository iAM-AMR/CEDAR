# Generated by Django 3.1.2 on 2020-12-15 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0005_auto_20201130_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location_join',
            name='reference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cedar_core.reference', to_field='other_reference_id'),
        ),
    ]