# Generated by Django 3.1 on 2020-10-02 20:56

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ast_method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(help_text='Laboratory test used to determine antimicrobial susceptibility', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='atc_vet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('levelname_1', models.CharField(help_text='The first level group: the anatomical main group, i.e. "General antiinfectives for systemic use"', max_length=100)),
                ('levelname_2', models.CharField(blank=True, help_text='The second level group: the therapeutic main group, i.e. "Antibacterials for systemic use"', max_length=100, null=True)),
                ('levelname_3', models.CharField(blank=True, help_text='The third level group: the therapeutic subgroup, i.e. "Beta-lactam antibacterials, penicillins"', max_length=100, null=True)),
                ('levelname_4', models.CharField(blank=True, help_text='The fourth level group: the chemical/therapeutic subgroup, i.e. "Penicillins with extended spectrum"', max_length=200, null=True)),
                ('levelname_4_simple', models.CharField(blank=True, help_text='Simple name for the fourth level group, i.e. "Penicillins" if the fourth level group is "Beta-lactamase sensitive penicillins"', max_length=100, null=True)),
                ('levelname_5', models.CharField(blank=True, help_text='The fifth level group: the chemical substance subgroup, i.e. "Ampicillin"', max_length=100, null=True)),
                ('levelname_5_alt', models.CharField(blank=True, help_text='Alternative name(s) for the fifth level group, i.e. "Penicillin G" for the fifth level group "benzylpenicillin"', max_length=100, null=True)),
                ('levelname_5_comb_example', models.CharField(blank=True, help_text='Example of a specific combination for a fifth level group containing a general combination, i.e. "piperacillin w. tazobactam" for the fifth level group "piperacillin and beta-lactamase inhibitor"', max_length=100, null=True)),
                ('levelcode_1', models.CharField(blank=True, help_text='The code for the first level group (2 characters in length)', max_length=4, null=True)),
                ('levelcode_2', models.CharField(blank=True, help_text='The code for the second level group (4 characters/digits in length)', max_length=8, null=True)),
                ('levelcode_3', models.CharField(blank=True, help_text='The code for the third level group (5 characters/digits in length)', max_length=10, null=True)),
                ('levelcode_4', models.CharField(blank=True, help_text='The code for the fourth level group (6 characters/digits in length)', max_length=12, null=True)),
                ('levelcode_5', models.CharField(blank=True, help_text='The code for the fifth level group (8 characters/digits in length)', max_length=16, null=True)),
                ('is_added', models.BooleanField(help_text='Specifies whether this antimicrobial exists in the ATCvet index.')),
                ('is_gene', models.BooleanField()),
                ('aro_number', models.IntegerField(blank=True, null=True)),
                ('is_duplicate', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='factor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factor_title', models.CharField(blank=True, help_text='A title that describes the factor, in title case. Factors including antimicrobial use should be formatted as "AntiX Use" where AntiX is the antimicrobial(s) administered (e.g. Bambermycin Use, Ceftiofur Use). Factors comparing organic / no antimicrobial use / free-range / conventional production should be titled "Production Type".', max_length=200, null=True)),
                ('factor_description', models.TextField(blank=True, help_text='A brief description of the factor. Additional information and experimental conditions related to the factor are included here. This includes details such as level of antimicrobial use, serovar, time period of administration, prior antimicrobial use, etc.', null=True)),
                ('place_in_text', models.CharField(blank=True, help_text='The location of the factor data in-text, i.e. "Table 2". If the data is from the body of the text, use the page and paragraph numbers, using the abbreviations Pg. and Para. respectively.', max_length=50, null=True)),
                ('group_exposed', models.CharField(blank=True, help_text='A brief description of the exposed group, in title case. Comparison groups are allocated as described in the literature. Factors including antimicrobial use are always given with "AntiX Use" for the exposed group, where AntiX is the antimicrobial(s) administered. The dose should be provided in the main factor description, unless the factor is a comparison of two doses.', max_length=200, null=True)),
                ('group_referent', models.CharField(blank=True, help_text='A brief description of the referent (unexposed) group, in title case. Comparison groups are allocated as described in the literature. If no allocation is provided, the less interventionist (or default practice) should be used as the referent. Factors including antimicrobial use are always given with the less interventionist as the referent (i.e. with "No Use" as the referent group or the lower dose as the referent). The dose should be provided in the main factor description, unless the factor is a comparison of two doses.', max_length=200, null=True)),
                ('contable_a', models.PositiveIntegerField(blank=True, help_text='The number of observations of resistance in the exposed group.', null=True)),
                ('contable_b', models.PositiveIntegerField(blank=True, help_text='The number of observations of susceptibility in the exposed group.', null=True)),
                ('contable_c', models.PositiveIntegerField(blank=True, help_text='The number of observations of resistance in the referent group.', null=True)),
                ('contable_d', models.PositiveIntegerField(blank=True, help_text='The number of observations of susceptibility in the referent group.', null=True)),
                ('ratetable_a', models.DecimalField(blank=True, decimal_places=2, help_text='The proportion of observations of resistance in the exposed group, up to 2 decimal places.', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('ratetable_b', models.DecimalField(blank=True, decimal_places=2, help_text='The proportion of observations of susceptibility in the exposed group, up to 2 decimal places.', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('ratetable_c', models.DecimalField(blank=True, decimal_places=2, help_text='The proportion of observations of resistance in the referent group, up to 2 decimal places.', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('ratetable_d', models.DecimalField(blank=True, decimal_places=2, help_text='The proportion of observations of susceptibility in the referent group, up to 2 decimal places.', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('table_n_exp', models.PositiveIntegerField(blank=True, help_text='The total number of observations in the exposed group.', null=True)),
                ('table_n_ref', models.PositiveIntegerField(blank=True, help_text='The total number of observations in the referent group.', null=True)),
                ('odds_ratio', models.DecimalField(blank=True, decimal_places=2, help_text='The odds ratio that describes the factor, up to 2 decimal places.', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('odds_ratio_lo', models.DecimalField(blank=True, decimal_places=2, help_text='The lower 95% confidence interval of the odds ratio that describes the factor, up to 2 decimal places.', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('odds_ratio_up', models.DecimalField(blank=True, decimal_places=2, help_text='The upper 95% confidence interval of the odds ratio that describes the factor, up to 2 decimal places.', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('odds_ratio_sig', models.CharField(blank=True, help_text='The significance (p-value) associated with the odds ratio that describes the factor, i.e. "< 0.05". May include symbols, numbers, and letters. There is no significance associated with count or rate data, only Odds Ratios. If an odds ratio is provided, without a significance level, please report "NR" for "not reported".', max_length=20, null=True)),
                ('ID_factor_v0', models.IntegerField(blank=True, help_text='The factor ID from v0 of CEDAR (CEDAR 2016), often used in model identifiers prior to 2020.', null=True)),
                ('v12_is_v1_import', models.BooleanField(blank=True, help_text='Specifies whether the factor is imported from v1.', null=True)),
                ('v12_ID_factor_v1', models.IntegerField(blank=True, help_text='The factor ID used within CEDAR v1.', null=True)),
                ('v12_ID_reference_v1', models.IntegerField(blank=True, help_text='The reference ID to which the factor belonged in v1.', null=True)),
                ('v12_ID_reference_v2_initial', models.IntegerField(blank=True, help_text='The reference ID assigned during import of v1 to v2, prior to reassignment of duplicates.', null=True)),
                ('v12_was_replaced', models.BooleanField(blank=True, help_text='Specifies whether the factor was replaced (sole source).', null=True)),
                ('amu_id', models.ManyToManyField(db_table='factor_amu_join', help_text='The ID(s) corresponding to the antimicrobials(s) that were used.', related_name='factors_amu', to='test_cedar_app.atc_vet')),
            ],
        ),
        migrations.CreateModel(
            name='host_01',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(help_text='The name of a host from which an assayed microbe originated, i.e. "Chicken"', max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='legacy_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_user', models.CharField(help_text='The full name of the user, i.e. "John Smith"', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='location_01',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_area', models.TextField(help_text='Country name', unique=True)),
                ('iso_country_code_3', models.CharField(blank=True, help_text='ISO country code (3 characters)', max_length=10, null=True)),
                ('iso_country_code_2', models.CharField(blank=True, help_text='ISO country code (2 characters)', max_length=10, null=True, unique=True)),
                ('iso_country_code_1', models.IntegerField(blank=True, help_text='ISO country code (numerical)', null=True)),
                ('m49_code', models.IntegerField(blank=True, null=True)),
                ('code_global', models.IntegerField(blank=True, null=True)),
                ('name_global', models.TextField(blank=True, null=True)),
                ('code_region', models.IntegerField(blank=True, help_text='Region code', null=True)),
                ('name_region', models.CharField(blank=True, help_text='Region name', max_length=100, null=True)),
                ('code_subregion', models.IntegerField(blank=True, help_text='Subregion code', null=True)),
                ('name_subregion', models.CharField(blank=True, help_text='Subregion name', max_length=100, null=True)),
                ('code_intermediate_subregion', models.IntegerField(blank=True, help_text='Intermediate subregion code', null=True)),
                ('name_intermediate_subregion', models.CharField(blank=True, help_text='Intermediate subregion name', max_length=100, null=True)),
                ('bin_least_developed_countries', models.BooleanField(blank=True, help_text='Specifies whether the country is one of the least developed countries', null=True)),
                ('bin_land_lock_least_developed_countries', models.BooleanField(blank=True, help_text='Specifies whether the country is one of the least developed landlocked countries', null=True)),
                ('bin_small_island_developing_states', models.BooleanField(blank=True, help_text='Specifies whether the country is one of the small island developing states', null=True)),
                ('bin_developing', models.BooleanField(blank=True, help_text='Specifies whether the country is a developing country', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='location_02',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subdivision_code', models.CharField(help_text='The subdivision code specified by the iso_3166_2 code. Normally two or three letters (i.e. "ON" for Ontario), but the numerals 2-9 may also be used', max_length=3)),
                ('subdivision', models.CharField(help_text='The name of the subdivision, i.e. "Ontario"', max_length=100)),
                ('subdivision_type', models.CharField(blank=True, help_text='The type of subdivision within the country, i.e. "Province"', max_length=200, null=True)),
                ('cipars_region_national', models.BooleanField(help_text='Specifies whether the location is within the CIPARS national region.')),
                ('cipars_region_atlantic', models.BooleanField(help_text='Specifies whether the location is within the CIPARS atlantic region.')),
                ('cipars_region_maritimes', models.BooleanField(help_text='Specifies whether the location is within the CIPARS maritimes region.')),
                ('cipars_region_prairies', models.BooleanField(help_text='Specifies whether the location is within the CIPARS prairies region.')),
                ('iso_country_code_2', models.ForeignKey(blank=True, help_text='The ISO 3166 alpha-2 country code, i.e. "CA" for Canada', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.location_01', to_field='iso_country_code_2')),
            ],
        ),
        migrations.CreateModel(
            name='microbe_01',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('microbe_name', models.CharField(help_text='The microbe subjected to AST, i.e. "Escherichia"', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='moa_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_format', models.CharField(help_text='Result format, i.e. "Contingency Table"', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='moa_unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_unit', models.CharField(help_text='Result unit, i.e. "Pooled Sample"', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='production_stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(help_text='The name of a production stage to which a factor applies, or where the effect of a factor is observed, i.e. "Farm"', max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_type', models.CharField(blank=True, help_text='The type of publication, i.e. "Journal"', max_length=50, null=True)),
                ('pub_title', models.TextField(help_text='The title of the publication, i.e. "Nature Reviews Immunology"')),
                ('pub_rank', models.IntegerField(blank=True, help_text='The Scimago numerical rank at the time of import (2018).', null=True)),
                ('pub_issn', models.TextField(blank=True, help_text='The ISSN of the publication, i.e. "15424863, 00079235"', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='reference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_reference_id', models.PositiveIntegerField(help_text='An additional identifier for the reference, from the legacy database.', unique=True)),
                ('name_bibtex', models.CharField(blank=True, help_text='An abbreviated identifier for the reference, given by Bibtex, i.e. "Jones2013"', max_length=200, null=True)),
                ('RWID', models.PositiveIntegerField(blank=True, help_text='The corresponding RefWorks ID for the reference', null=True)),
                ('name_author', models.TextField(blank=True, help_text='The surname(s) of the authors, in the form of a comma-separated or semi-colon-separated list, i.e. "Chapman, Smith, Otten, Fazil" or "Howe, K.; Linton, A. H.; Osborne, A. D."', null=True)),
                ('publication_year', models.CharField(blank=True, help_text='The year in which the study was published.', max_length=4, null=True, validators=[django.core.validators.RegexValidator('^\\d{4}$')])),
                ('ident_doi', models.CharField(blank=True, help_text='The DOI associated with the reference, i.e. 10.3168/jds.2014-8432', max_length=500, null=True)),
                ('ident_pmid', models.CharField(blank=True, help_text='The eight-digit PMID associated with the reference, i.e. 84889799', max_length=8, null=True, validators=[django.core.validators.RegexValidator('^\\d{8}$')])),
                ('study_title', models.TextField(blank=True, help_text='The title of the study, in sentence case.', null=True)),
                ('study_design_detail', models.TextField(blank=True, help_text='The details of the study design. Often, this can be copied from the study directly.', null=True)),
                ('study_sample_method', models.TextField(blank=True, help_text='A description of the sampling method, or of how samples were selected and collected, for the study.', null=True)),
                ('has_breakpoint', models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No'), ('U', 'Unsure'), ('NR', 'Not Reported')], help_text='Specifies whether the study explicitly reports the MIC values used in its susceptibility tests.', max_length=2, null=True)),
                ('has_mic_table', models.CharField(blank=True, choices=[('Y', 'Yes'), ('N', 'No'), ('U', 'Unsure'), ('NR', 'Not Reported')], help_text='Specifies whether the study includes an MIC table.', max_length=2, null=True)),
                ('capture_search_2016', models.BooleanField(help_text='Specifies whether the reference was captured in the 2016 literature search.')),
                ('capture_search_2019', models.BooleanField(help_text='Specifies whether the reference was captured in the 2019 literature search.')),
                ('capture_snowball', models.BooleanField(help_text='Specifies whether the reference was captured through snowballing (searching cited papers, and or reverse citations).')),
                ('capture_submit', models.BooleanField(help_text='Specifies whether the reference was captured through a direct submission to CEDAR.')),
                ('study_objective', models.TextField(blank=True, help_text='The stated objective of the study.', null=True)),
                ('exclude_extraction', models.BooleanField(default=False, help_text='Specifies whether or not to exclude the reference from extraction.')),
                ('exclude_extraction_reason', models.CharField(blank=True, help_text='If the reference is to be excluded, the reason for doing so.', max_length=100, null=True)),
                ('v12_is_v1_import', models.BooleanField(blank=True, help_text='Specifies whether this reference was imported from v1.', null=True)),
                ('v12_is_in_v1_and_v2', models.BooleanField(blank=True, help_text='Specifies whether this reference exists in both v1 and v2.', null=True)),
                ('v12_reference_ID_in_v1', models.PositiveIntegerField(blank=True, help_text='The reference ID used within CEDAR v1. This only exists when the reference is an import from v1.', null=True)),
                ('v12_migrated_from', models.PositiveIntegerField(blank=True, help_text='For v2 references, this is the v1 reference which matched during factor migration from v1 to v2. Factors were migrated from this record.', null=True)),
                ('v12_migrated_to', models.PositiveIntegerField(blank=True, help_text='For v1 references, this is the v2 reference which matched during factor migration from v1 to v2. Factors were migrated to this record.', null=True)),
                ('v12_solo_extraction_2016', models.BooleanField(blank=True, help_text='Specifies whether a v2 reference was identified as previously extracted in v1 by the assigned extractor, and was NOT dual-extracted.', null=True)),
                ('ref_abstract', models.TextField(blank=True, help_text='The abstract of the study.', null=True)),
                ('CEDAR_extract_east', models.BooleanField(blank=True, help_text='Specifies whether this reference is to be extracted by the "east" team (i.e. Guelph/ON)', null=True)),
                ('CEDAR_extract_west', models.BooleanField(blank=True, help_text='Specifies whether this reference is to be extracted by the "west" team (i.e. Alberta)', null=True)),
                ('CEDAR_extract_esr', models.BooleanField(blank=True, null=True)),
                ('topic_tab_cattle', models.BooleanField(blank=True, help_text='Specifies whether the reference pertains to cattle', null=True)),
                ('topic_tab_chicken', models.BooleanField(blank=True, help_text='Specifies whether the reference pertains to chicken', null=True)),
                ('topic_tab_swine', models.BooleanField(blank=True, help_text='Specifies whether the reference pertains to swine', null=True)),
                ('topic_tab_turkey', models.BooleanField(blank=True, help_text='Specifies whether the reference pertains to turkey', null=True)),
                ('topic_tab_ecoli', models.BooleanField(blank=True, help_text='Specifies whether the reference pertains to E. coli', null=True)),
                ('topic_tab_enterococcus', models.BooleanField(blank=True, help_text='Specifies whether the reference pertains to Enterococcus', null=True)),
                ('topic_tab_salmonella', models.BooleanField(blank=True, help_text='Specifies whether the reference pertains to Salmonella', null=True)),
                ('topic_tab_campylobacter', models.BooleanField(blank=True, help_text='Specifies whether the reference pertains to Campylobacter', null=True)),
                ('topic_tab_has_topic', models.BooleanField(blank=True, null=True)),
                ('topic_tab_host_free', models.CharField(blank=True, help_text='Free text description of the animal host(s) the reference pertains to.', max_length=200, null=True)),
                ('topic_tab_microbe_free', models.CharField(blank=True, help_text='Free text description of the microbe(s) the reference pertains to.', max_length=200, null=True)),
                ('ast_method', models.ForeignKey(blank=True, help_text='The antimicrobial susceptibility test type applied in the study', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.ast_method')),
                ('publisher', models.ForeignKey(blank=True, help_text='The outlet which published the study.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.publisher')),
            ],
        ),
        migrations.CreateModel(
            name='reference_history_action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=200)),
                ('action_description', models.TextField(blank=True, null=True)),
                ('action_level', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='study_design',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('design', models.CharField(help_text='Study design category, i.e. "Experimental"', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='reference_note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, help_text='A free-text note describing any challenges with interpreting the study, or extracting the data.', null=True)),
                ('resolved', models.BooleanField(default=False, help_text='Specifies whether or not the note was resolved or addressed')),
                ('reference', models.ForeignKey(blank=True, help_text='The ID corresponding to the reference to which the note pertains.', null=True, on_delete=django.db.models.deletion.CASCADE, to='test_cedar_app.reference', to_field='other_reference_id')),
                ('user', models.ForeignKey(blank=True, help_text='The ID corresponding to the user who made the note.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.legacy_user')),
            ],
        ),
        migrations.CreateModel(
            name='reference_history_join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_date', models.DateField(blank=True, null=True)),
                ('action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.reference_history_action')),
                ('reference', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='test_cedar_app.reference', to_field='other_reference_id')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.legacy_user')),
            ],
        ),
        migrations.AddField(
            model_name='reference',
            name='study_design',
            field=models.ForeignKey(blank=True, help_text='The ID corresponding to the type of study design used in the study.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.study_design'),
        ),
        migrations.CreateModel(
            name='model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(help_text='The name of the iAM.AMR model, i.e. "iAM.AMR.CHI"', max_length=20, unique=True)),
                ('model_description', models.CharField(blank=True, help_text='A simple and brief description or caption of the model.', max_length=100, null=True)),
                ('model_create_date', models.DateField(blank=True, help_text='The date the model/query was created, in <em>YYYY-MM-DD</em> format', null=True)),
                ('model_maintain_date', models.DateField(blank=True, help_text='The date the model/query was last updated, in <em>YYYY-MM-DD</em> format', null=True)),
                ('model_create_user', models.ForeignKey(blank=True, help_text='The ID of the user who created the model/query.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_c', to='test_cedar_app.legacy_user')),
                ('model_maintain_user_id', models.ManyToManyField(db_table='model_user_join', help_text='The ID of a user who maintains the model/query.', to='test_cedar_app.legacy_user')),
            ],
        ),
        migrations.CreateModel(
            name='microbe_02',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('microbe_subtype_name', models.CharField(help_text='The species or subtype of the microbe subjected to AST, i.e. "coli" for parent microbe "Escherichia"', max_length=100)),
                ('microbe_01_id', models.ManyToManyField(db_table='microbe_join', help_text='The ID of the parent microbe', to='test_cedar_app.microbe_01')),
            ],
        ),
        migrations.CreateModel(
            name='location_join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True)),
                ('location_01', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.location_01')),
                ('location_02', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.location_02')),
                ('reference', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='test_cedar_app.reference')),
            ],
        ),
        migrations.CreateModel(
            name='host_02',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_subtype_name', models.CharField(help_text='The name of a host subtype from which an assayed microbe originated, i.e. "Eggs" for a parent host "Chicken"', max_length=100)),
                ('host_01_id', models.ManyToManyField(db_table='host_join', help_text='The ID of the parent host', to='test_cedar_app.host_01')),
            ],
        ),
        migrations.CreateModel(
            name='factor_exclusion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exclude_reason', models.TextField(blank=True, help_text='A reason why the factor should be excluded from the model.', null=True)),
                ('factor', models.ForeignKey(blank=True, help_text='The ID corresponding to the factor that is to be excluded.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.factor')),
                ('model', models.ForeignKey(blank=True, help_text='The ID corresponding to the model from which the factor should be excluded.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.model')),
            ],
        ),
        migrations.AddField(
            model_name='factor',
            name='host_01',
            field=models.ForeignKey(blank=True, help_text='The ID corresponding to the host from which the microbe was isolated.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.host_01'),
        ),
        migrations.AddField(
            model_name='factor',
            name='host_02',
            field=models.ForeignKey(blank=True, help_text='The ID corresponding to the host subtype from which the microbe was isolated.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.host_02'),
        ),
        migrations.AddField(
            model_name='factor',
            name='microbe_01',
            field=models.ForeignKey(blank=True, help_text='The ID corresponding to the microbe assayed for resistance.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.microbe_01'),
        ),
        migrations.AddField(
            model_name='factor',
            name='microbe_02',
            field=models.ForeignKey(blank=True, help_text='The ID corresponding to the subtype of the microbe assayed for resistance.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.microbe_02'),
        ),
        migrations.AddField(
            model_name='factor',
            name='moa_type',
            field=models.ForeignKey(blank=True, help_text='The ID corresponding to the type of measure of association reported for the factor.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.moa_type'),
        ),
        migrations.AddField(
            model_name='factor',
            name='moa_unit',
            field=models.ForeignKey(blank=True, help_text='The ID corresponding to the experimental unit or level of analysis for which the measure of association is presented.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_cedar_app.moa_unit'),
        ),
        migrations.AddField(
            model_name='factor',
            name='prod_stage_group_allocate',
            field=models.ForeignKey(blank=True, help_text='The ID corresponding to the production stage at which the groups were allocated (i.e. factor applied). ', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factors_a', to='test_cedar_app.production_stage'),
        ),
        migrations.AddField(
            model_name='factor',
            name='prod_stage_group_observe',
            field=models.ForeignKey(blank=True, help_text='The ID corresponding to the production stage at which the observations were recorded (i.e. factor observed).', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factors_o', to='test_cedar_app.production_stage'),
        ),
        migrations.AddField(
            model_name='factor',
            name='reference',
            field=models.ForeignKey(help_text='The ID corresponding to the reference that describes the factor.', on_delete=django.db.models.deletion.CASCADE, to='test_cedar_app.reference', to_field='other_reference_id'),
        ),
        migrations.AddField(
            model_name='factor',
            name='resistance',
            field=models.ForeignKey(blank=True, help_text='The ID corresponding to the resistance that was assayed.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='factors_resistance', to='test_cedar_app.atc_vet'),
        ),
    ]
