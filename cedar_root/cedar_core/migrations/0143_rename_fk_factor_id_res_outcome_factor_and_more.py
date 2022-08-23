# Generated by Django 4.0.4 on 2022-06-22 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0142_rename_fk_ast_breakpoint_source_id_res_outcome_ast_breakpoint_source_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='res_outcome',
            old_name='fk_factor_id',
            new_name='factor',
        ),
        migrations.RenameField(
            model_name='res_outcome',
            old_name='fk_group_observe_production_stage_id',
            new_name='group_observe_production_stage',
        ),
        migrations.RenameField(
            model_name='res_outcome',
            old_name='fk_microbe_01_id',
            new_name='microbe_level_01',
        ),
        migrations.RenameField(
            model_name='res_outcome',
            old_name='fk_res_outcome_microbe_02_id',
            new_name='microbe_level_02',
        ),
        migrations.RenameField(
            model_name='res_outcome',
            old_name='fk_moa_type_id',
            new_name='moa_type',
        ),
        migrations.RenameField(
            model_name='res_outcome',
            old_name='fk_moa_unit_id',
            new_name='moa_unit',
        ),
        migrations.RenameField(
            model_name='res_outcome',
            old_name='fk_resistance_atc_vet_id',
            new_name='resistance',
        ),
        migrations.RenameField(
            model_name='res_outcome',
            old_name='fk_genetic_element_id',
            new_name='resistance_gene',
        ),
    ]