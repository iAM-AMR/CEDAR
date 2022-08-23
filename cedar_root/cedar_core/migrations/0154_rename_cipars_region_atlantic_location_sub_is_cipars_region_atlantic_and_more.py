# Generated by Django 4.0.4 on 2022-07-04 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0153_rename_host_name_host_01_host_01_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='location_sub',
            old_name='cipars_region_atlantic',
            new_name='is_cipars_region_atlantic',
        ),
        migrations.RenameField(
            model_name='location_sub',
            old_name='cipars_region_maritimes',
            new_name='is_cipars_region_maritimes',
        ),
        migrations.RenameField(
            model_name='location_sub',
            old_name='cipars_region_national',
            new_name='is_cipars_region_national',
        ),
        migrations.RenameField(
            model_name='location_sub',
            old_name='cipars_region_prairies',
            new_name='is_cipars_region_prairies',
        ),
        migrations.RenameField(
            model_name='microbe_01',
            old_name='microbe_name',
            new_name='microbe_01_name',
        ),
        migrations.RenameField(
            model_name='microbe_02',
            old_name='cedar_esr_microbe_02_id',
            new_name='HIST_cedar_esr_microbe_02',
        ),
        migrations.RenameField(
            model_name='microbe_02',
            old_name='microbe_subtype_name',
            new_name='microbe_02_name',
        ),
        migrations.RenameField(
            model_name='microbe_02',
            old_name='fk_microbe_02_microbe_01_id',
            new_name='microbe_level_01',
        ),
        migrations.RenameField(
            model_name='moa_type',
            old_name='res_format',
            new_name='moa_type_name',
        ),
        migrations.RenameField(
            model_name='moa_unit',
            old_name='res_unit',
            new_name='outcome_unit_name',
        ),
        migrations.RenameField(
            model_name='production_stage',
            old_name='cedar_esr_production_stage_id',
            new_name='HIST_cedar_esr_production_stage',
        ),
        migrations.RenameField(
            model_name='production_stage',
            old_name='stage',
            new_name='production_stage_name',
        ),
        migrations.RenameField(
            model_name='study_design',
            old_name='design',
            new_name='study_design_name',
        ),
        migrations.RemoveField(
            model_name='host_02',
            name='host_01',
        ),
        migrations.RemoveField(
            model_name='microbe_02',
            name='DEP_old_id',
        ),
        migrations.AddField(
            model_name='host_02',
            name='host_level_01',
            field=models.ForeignKey(help_text='The host (level 1) from which the assayed samples were isolated.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.host_01'),
        ),
        migrations.AlterField(
            model_name='res_outcome',
            name='extract_user_legacy',
            field=models.ForeignKey(blank=True, help_text='The user who extracted the record.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.legacy_user'),
        ),
        migrations.AlterField(
            model_name='res_outcome',
            name='microbe_level_01',
            field=models.ForeignKey(blank=True, help_text='The ID of the parent microbe', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.microbe_01'),
        ),
    ]