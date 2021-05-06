# Generated by Django 3.1.5 on 2021-02-10 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0019_auto_20210210_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='factor',
            name='DEP_exclude_iam',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='DEP_exclude_iam_reason',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='DEP_total_obs',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='OLD_resistance_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='OLD_short_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='OLD_use_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='TEMP_use_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='exclude_cedar',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='exclude_cedar_reason',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='microbe_02_old_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='factor',
            name='odds_ratio_confidence',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True),
        ),
    ]