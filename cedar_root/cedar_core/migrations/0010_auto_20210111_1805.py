# Generated by Django 3.1.5 on 2021-01-11 23:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cedar_core', '0009_auto_20210111_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factor',
            name='factor_description',
            field=models.TextField(blank=True, help_text='A brief description of the factor. Additional information and experimental conditions related to the factor are included here. This includes details such as level of antimicrobial use (dosage), serovar, time period of administration, prior antimicrobial use, etc.', null=True),
        ),
        migrations.AlterField(
            model_name='factor',
            name='odds_ratio_sig',
            field=models.CharField(blank=True, help_text='The significance (p-value) associated with the odds ratio that describes the factor, i.e. "< 0.05". May include symbols, numbers, and letters. There is no significance associated with count or prevalence data, only Odds Ratios. If an odds ratio is provided, without a significance level, please report "NR" for "not reported"', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='name_author',
            field=models.TextField(blank=True, help_text='The name(s) of the authors, in the form of a comma-separated or semi-colon-separated list, i.e. "Chapman, Smith, Otten, Fazil" or "Howe, K.; Linton, A. H.; Osborne, A. D."', null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='publication_year',
            field=models.CharField(blank=True, help_text='The year in which the study was published', max_length=4, null=True, validators=[django.core.validators.RegexValidator('^\\d{4}$')]),
        ),
        migrations.AlterField(
            model_name='reference',
            name='publisher',
            field=models.ForeignKey(blank=True, help_text='The outlet which published the study', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.publisher'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='study_design',
            field=models.ForeignKey(blank=True, help_text='The type of study design applied', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cedar_core.study_design'),
        ),
        migrations.AlterField(
            model_name='reference',
            name='study_design_detail',
            field=models.TextField(blank=True, help_text='The details of the study design. Often, this can be copied from the study directly', null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='study_sample_method',
            field=models.TextField(blank=True, help_text='A description of the sampling method, or of how samples were selected and collected, for the study', null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='study_title',
            field=models.TextField(default='', help_text='The title of the study, in sentence case'),
        ),
        migrations.AlterField(
            model_name='reference_note',
            name='note',
            field=models.TextField(blank=True, help_text='A free-text note describing any challenges with interpreting the study, or extracting the data', null=True),
        ),
    ]