# Generated by Django 3.1.7 on 2021-10-13 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0067_auto_20211013_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factor',
            name='DEP_exclude_iam',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='DEP_exclude_iam_reason',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='DEP_total_obs',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='OLD_resistance_id',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='OLD_short_name',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='OLD_use_id',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='TEMP_use_id',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='factor_v0_id',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='microbe_02_old_id',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='v12_ID_factor_v1',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='v12_ID_reference_v1',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='v12_ID_reference_v2_initial',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='v12_is_v1_import',
        ),
        migrations.RemoveField(
            model_name='factor',
            name='v12_solo_extraction_2016',
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='DEP_exclude_iam',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='DEP_exclude_iam_reason',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='DEP_total_obs',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='OLD_resistance_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='OLD_short_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='OLD_use_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='TEMP_use_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='factor_v0_id',
            field=models.IntegerField(blank=True, help_text='The factor ID from v0 of CEDAR (CEDAR 2016), often used in model identifiers prior to 2020.', null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='microbe_02_old_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='v12_ID_factor_v1',
            field=models.IntegerField(blank=True, help_text='The factor ID used within CEDAR v1.', null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='v12_ID_reference_v1',
            field=models.IntegerField(blank=True, help_text='The reference ID to which the factor belonged in v1.', null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='v12_ID_reference_v2_initial',
            field=models.IntegerField(blank=True, help_text='The reference ID assigned during import of v1 to v2, prior to reassignment of duplicates.', null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='v12_is_v1_import',
            field=models.BooleanField(blank=True, help_text='The factor is imported from v1.', null=True),
        ),
        migrations.AddField(
            model_name='res_outcome',
            name='v12_solo_extraction_2016',
            field=models.BooleanField(blank=True, help_text='These are v1 factors that were migrated to v2 references, that will not be dual extracted, as they were thoroughly reviewed by Ashley or Daniella in v1', null=True),
        ),
    ]
