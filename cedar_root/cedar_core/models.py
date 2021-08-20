from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

import pandas

# Read in the data dictionary
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
colnames = ['table', 'field', 'caption', 'description', 'help_text', 'analysis_notes']
file_path = BASE_DIR / 'CEDAR_Dictionary_Main_2021.08.20.csv'
data_file = pandas.read_csv(file_path, names=colnames, encoding='cp1252')
field_names = data_file.field.tolist()[1:]
field_descs = data_file.description.tolist()[1:]

# Make a dictionary, indexed by field names, of the field descriptions (to go into the help_text argument of each field declared below)
data_dict = dict(zip(field_names, field_descs))

# Clean the data dict
for key in data_dict:
    if isinstance(data_dict[key], float):
        data_dict[key] = ''
    else:
        data_dict[key] = data_dict[key].replace('\xa0',' ')

#Static tables from CEDAR

class host_01(models.Model):
    """
    A host species.
    """
    host_name = models.CharField(max_length=20, unique=True, help_text=data_dict['host_name'])
    
    def __str__(self):
        return self.host_name

class host_02(models.Model): #TO DO: self-identification for dropdown!!
    """
    A host subtype.
    """
    host_01_id = models.ManyToManyField(host_01, db_table='host_join', help_text=data_dict['host_01_id'])
    host_subtype_name = models.CharField(max_length=100, help_text=data_dict['host_subtype_name'])
    DEP_sel_beef = models.BooleanField(blank=True, null=True, help_text=data_dict['DEP_sel_beef'])
    DEP_sel_broil = models.BooleanField(blank=True, null=True, help_text=data_dict['DEP_sel_broil'])
    
    def __str__(self):
        return self.host_subtype_name
    
class location_01(models.Model): #TO DO: remaining help text
    """
    A location (a country).
    """
    country_area = models.TextField(unique=True, help_text=data_dict['country_area'])
    iso_country_code_3 = models.CharField(max_length=10, blank=True, null=True, help_text=data_dict['iso_country_code_3'])
    iso_country_code_2 = models.CharField(max_length=10, blank=True, null=True, unique=True, help_text=data_dict['iso_country_code_2'])
    iso_country_code_1 = models.IntegerField(blank=True, null=True, help_text=data_dict['iso_country_code_1'])
    m49_code = models.IntegerField(blank=True, null=True, help_text=data_dict['m49_code'])
    code_global = models.IntegerField(blank=True, null=True, help_text=data_dict['code_global'])
    name_global = models.TextField(blank=True, null=True, help_text=data_dict['name_global'])
    code_region = models.IntegerField(blank=True, null=True, help_text=data_dict['code_region'])
    name_region = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['name_region'])
    code_subregion = models.IntegerField(blank=True, null=True, help_text=data_dict['code_subregion'])
    name_subregion = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['name_subregion'])
    code_intermediate_subregion = models.IntegerField(blank=True, null=True, help_text=data_dict['code_intermediate_subregion'])
    name_intermediate_subregion = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['name_intermediate_subregion'])
    bin_least_developed_countries = models.BooleanField(blank=True, null=True, help_text=data_dict['bin_least_developed_countries'])
    bin_land_lock_least_developed_countries = models.BooleanField(blank=True, null=True, help_text=data_dict['bin_land_lock_least_developed_countries'])
    bin_small_island_developing_states = models.BooleanField(blank=True, null=True, help_text=data_dict['bin_small_island_developing_states'])
    bin_developing = models.BooleanField(blank=True, null=True, help_text=data_dict['bin_developing'])
    
    def __str__(self):
        return self.country_area

class location_02(models.Model):
    """
    A location (a subdivision below a country, i.e. a state, province, parish, etc.)
    """
    iso_country_code_2_id = models.ForeignKey(location_01, on_delete=models.SET_NULL, blank=True, null=True, to_field='iso_country_code_2', help_text=data_dict['iso_country_code_2_id'])
    subdivision_code = models.CharField(max_length=3, help_text=data_dict['subdivision_code'])
    subdivision = models.CharField(max_length=100, help_text=data_dict['subdivision'])
    subdivision_type = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['subdivision_type'])
    cipars_region_national = models.BooleanField(help_text=data_dict['cipars_region_national'])
    cipars_region_atlantic = models.BooleanField(help_text=data_dict['cipars_region_atlantic'])
    cipars_region_maritimes = models.BooleanField(help_text=data_dict['cipars_region_maritimes'])
    cipars_region_prairies = models.BooleanField(help_text=data_dict['cipars_region_prairies'])
    
    def __str__(self):
        return '%s (%s)' % (self.subdivision, self.subdivision_type)

class microbe_01(models.Model):
    """
    A microbe species.
    """
    microbe_name = models.CharField(max_length=50, unique=True, help_text=data_dict['microbe_name'])
    
    def __str__(self):
        return self.microbe_name

class microbe_02(models.Model): #TO DO: self-identification for dropdown!!
    """
    A microbe subtype, corresponding to a microbe species.
    """
    microbe_01_id = models.ManyToManyField(microbe_01, db_table='microbe_join', help_text=data_dict['microbe_01_id'])
    microbe_subtype_name = models.CharField(max_length=100, help_text=data_dict['microbe_subtype_name'])
    DEP_old_id = models.IntegerField(blank=True, null=True, help_text=data_dict['DEP_old_id'])
    
    def __str__(self):
        return self.microbe_subtype_name
    
class moa_type(models.Model):
    """
    A format of extracted measure of association data.
    """
    res_format = models.CharField(max_length=50, unique=True, help_text=data_dict['res_format'])
    
    def __str__(self):
        return self.res_format

class moa_unit(models.Model):
    """
    A unit of analysis for extracted measure of association data.
    """
    res_unit = models.CharField(max_length=50, unique=True, help_text=data_dict['res_unit'])

    def __str__(self):
        return self.res_unit

class production_stage(models.Model):
    """
    A production stage along the farm-to-fork continuum.
    """
    stage = models.CharField(max_length=20, unique=True, help_text=data_dict['stage'])
    
    def __str__(self):
        return self.stage

#class status_reference(models.Model):
    #"""
    #A reference's status with respect to data extraction.
    #"""
    #status = models.CharField(max_length=50, unique=True, help_text='The stage of data extraction, i.e. "Validation (Phase 1)"')
    #status_description = models.TextField(help_text='A description of the status')
    
    #def __str__(self):
        #return self.status

class publisher(models.Model):
    """
    A publishing organization pertaining to one or more references/studies.
    """
    pub_type = models.CharField(max_length=50, blank=True, null=True, help_text=data_dict['pub_type'])
    pub_title = models.TextField(help_text=data_dict['pub_title'])
    pub_rank = models.IntegerField(blank=True, null=True, help_text=data_dict['pub_rank'])
    pub_issn = models.TextField(blank=True, null=True, help_text=data_dict['pub_issn'])
    
    def __str__(self):
        return '%s (%s)' % (self.pub_title, self.pub_rank)

class study_design(models.Model):
    """
    An overall study design type.
    """
    design = models.CharField(max_length=50, unique=True, help_text=data_dict['design'])
    
    def __str__(self):
        return self.design

class atc_vet(models.Model): #TO DO: finish help text
    """
    A list of antimicrobials, taken from the ATCvet index.
    """
    levelname_1 = models.CharField(max_length=100, help_text=data_dict['levelname_1'])
    levelname_2 = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['levelname_2'])
    levelname_3 = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['levelname_3'])
    levelname_4 = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['levelname_4'])
    levelname_4_coarse = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['levelname_4_coarse'])
    levelname_5 = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['levelname_5'])
    levelname_5_alt = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['levelname_5_alt'])
    levelname_5_comb_example = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['levelname_5_comb_example'])
    levelcode_1 = models.CharField(max_length=4, blank=True, null=True, help_text=data_dict['levelcode_1'])
    levelcode_2 = models.CharField(max_length=8, blank=True, null=True, help_text=data_dict['levelcode_2'])
    levelcode_3 = models.CharField(max_length=10, blank=True, null=True, help_text=data_dict['levelcode_3'])
    levelcode_4 = models.CharField(max_length=12, blank=True, null=True, help_text=data_dict['levelcode_4'])
    levelcode_5 = models.CharField(max_length=16, blank=True, null=True, help_text=data_dict['levelcode_5'])
    is_added = models.BooleanField(help_text=data_dict['is_added'])
    is_gene = models.BooleanField(help_text=data_dict['is_gene'])
    aro_number = models.IntegerField(blank=True, null=True, help_text=data_dict['aro_number'])
    is_duplicate = models.BooleanField(help_text=data_dict['is_duplicate'])
    
    def __str__(self):
        if self.levelname_5 is not None:
            ident = self.levelname_5
        else:
            ident = self.levelname_1
        return ident

#Dynamic tables from CEDAR

class legacy_user(models.Model): #renamed as legacy_user
    """
    A CEDAR user from the legacy database (Microsoft Access).
    """
    name_user = models.CharField(max_length=50, unique=True, help_text=data_dict['name_user'])
    
    def __str__(self):
        return self.name_user

class model(models.Model):
    """
    An iAM.AMR model for which a query may be generated.
    """
    model_name = models.CharField(max_length=20, unique=True, help_text=data_dict['model_name'])
    model_description = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['model_description'])
    model_create_user_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, blank=True, null=True, related_name='users_c', help_text=data_dict['model_create_user_id'])
    model_create_date = models.DateField(blank=True, null=True, help_text=data_dict['model_create_date'])
    model_maintain_user_id = models.ManyToManyField(legacy_user, db_table='model_user_join', help_text=data_dict['model_maintain_user_id']) #changed: made ManyToMany
    model_maintain_date = models.DateField(blank=True, null=True, help_text=data_dict['model_maintain_date'])
    
    def __str__(self):
        return self.model_name

class ast_method(models.Model):
    method = models.CharField(max_length=50, help_text=data_dict['method'])
    
    def __str__(self):
        return self.method

class reference(models.Model):
    """
    A reference/article/study from which factors are extracted.
    """
    
    ANSWER_CHOICES = [
        ('1', 'Yes'),
        ('0', 'No'),
        ('2', 'Unclear'),
        ('3', 'Not Reported'),
        ('4', 'Needs Review'),
    ]
    
    #Potential future change: use pk rather than other_reference_id for foreign keys
    other_reference_id = models.PositiveIntegerField(unique=True, blank=True, null=True, help_text=data_dict['other_reference_id'])
    key_bibtex = models.CharField(max_length=200, default='', help_text=data_dict['key_bibtex'])
    refwk = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['refwk'])
    study_authors = models.TextField(blank=True, null=True, help_text=data_dict['study_authors'])
    publish_id = models.ForeignKey(publisher, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['publish_id'])
    publish_name_alt = models.CharField(max_length=500, blank=True, null=True, default='', help_text=data_dict['publish_name_alt']) # NEW
    publish_year = models.CharField(blank=True, null=True, max_length=4, validators=[RegexValidator(r'^\d{4}$')], help_text=data_dict['publish_year'])
    publish_doi = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['publish_doi'])
    publish_pmid = models.CharField(max_length=8, validators=[RegexValidator(r'^\d{8}$')], blank=True, null=True, help_text=data_dict['publish_pmid'])
    study_title = models.TextField(default='', help_text=data_dict['study_title'])
    study_design_id = models.ForeignKey(study_design, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['study_design_id'])
    study_design_detail = models.TextField(blank=True, null=True, help_text=data_dict['study_design_detail'])
    study_sample_method = models.TextField(blank=True, null=True, help_text=data_dict['study_sample_method'])
    ref_has_explicit_break = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text=data_dict['ref_has_explicit_break'])
    ref_has_mic_table = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text=data_dict['ref_has_mic_table'])
    capture_search_2016 = models.BooleanField(blank=True, null=True,help_text=data_dict['capture_search_2016'])
    capture_search_2019 = models.BooleanField(blank=True, null=True,help_text=data_dict['capture_search_2019'])
    capture_snowball = models.BooleanField(blank=True, null=True,help_text=data_dict['capture_snowball'])
    capture_submit = models.BooleanField(blank=True, null=True,help_text=data_dict['capture_submit'])
    
    #NEW. TO DO: make many to many
    ast_method_id = models.ForeignKey(ast_method, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['ast_method_id'])
    
    #t2_study_sample_collect = models.TextField(blank=True, null=True, help_text='') #TO DO help text
    DEP_study_objective = models.TextField(blank=True, null=True, help_text=data_dict['DEP_study_objective'])
    
    exclude_extraction = models.BooleanField(default=False, help_text=data_dict['exclude_extraction'])
    exclude_extraction_reason = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['exclude_extraction_reason'])
    
    v12_v1_id = models.BooleanField(blank=True, null=True, help_text=data_dict['v12_v1_id'])
    v12_is_in_v1_and_v2 = models.BooleanField(blank=True, null=True, help_text=data_dict['v12_is_in_v1_and_v2'])
    v12_reference_ID_in_v1 = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['v12_reference_ID_in_v1'])
    v12_migrated_from = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['v12_migrated_from'])
    v12_migrated_to = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['v12_migrated_to'])
    #v12_migrated_as_replace = models.BooleanField(blank=True, null=True, help_text='Specifies whether a v2 reference was identified as previously extracted in v1 by the assigned extractor, and was NOT dual-extracted.')
    v12_solo_extraction_2016 = models.BooleanField(blank=True, null=True, help_text=data_dict['v12_solo_extraction_2016'])
    
    ref_abstract = models.TextField(blank=True, null=True, help_text=data_dict['ref_abstract'])
    
    CEDAR_extract_east = models.BooleanField(blank=True, null=True, help_text=data_dict['CEDAR_extract_east'])
    CEDAR_extract_west = models.BooleanField(blank=True, null=True, help_text=data_dict['CEDAR_extract_west'])
    CEDAR_extract_esr = models.BooleanField(blank=True, null=True, help_text=data_dict['CEDAR_extract_esr'])
    topic_tab_cattle = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_cattle'])
    topic_tab_chicken = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_chicken'])
    topic_tab_swine = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_swine'])
    topic_tab_turkey = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_turkey'])
    topic_tab_ecoli = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_ecoli'])
    topic_tab_enterococcus = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_enterococcus'])
    topic_tab_salmonella = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_salmonella'])
    topic_tab_campylobacter = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_campylobacter'])
    topic_tab_has_topic = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_has_topic'])
    topic_tab_host_free = models.CharField(blank=True, null=True, max_length=200, help_text=data_dict['topic_tab_host_free'])
    topic_tab_microbe_free = models.CharField(blank=True, null=True, max_length=200, help_text=data_dict['topic_tab_microbe_free'])
    
    archived = models.BooleanField(blank=True, null=True, default=False, help_text=data_dict['archived'])
    archived_why = models.CharField(blank=True, null=True, max_length=200, help_text=data_dict['archived_why'])
    
    # NEW
    DEP_other_genomics = models.CharField(blank=True, null=True, max_length=500, help_text='')
    DEP_analysis_unit_id = models.IntegerField(blank=True, null=True, help_text='')
    DEP_ref_has_mdr = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text='')
    OLD_status_id = models.IntegerField(blank=True, null=True, help_text='')
    OLD_ref_has_wgs = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text='')
    OLD_pub_name = models.IntegerField(blank=True, null=True, help_text='')
    OLD_id = models.IntegerField(blank=True, null=True, help_text='')
    OLD_subdivision = models.CharField(blank=True, null=True, max_length=500, help_text='')
    OLD_country_id = models.IntegerField(blank=True, null=True, help_text='')
    OLD_has_plasmid_type = models.BooleanField(blank=True, null=True, help_text='')
    ast_free = models.CharField(blank=True, null=True, max_length=500, help_text='')
    ref_has_data_pheno_level = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text=data_dict['ref_has_data_pheno_level'])
    ref_has_data_geno_level = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text=data_dict['ref_has_data_geno_level'])
    ref_has_esbl_factor = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text=data_dict['ref_has_esbl_factor'])
    
    
    def __str__(self):
        return '%s: %s' % (self.key_bibtex, self.study_title)

class location_join(models.Model):
    loc_ref_id = models.ForeignKey(reference, on_delete=models.CASCADE, blank=True, null=True, to_field='other_reference_id', help_text=data_dict['loc_ref_id'])
    location_01_id = models.ForeignKey(location_01, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['location_01_id'])
    location_02_id = models.ForeignKey(location_02, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['location_02_id'])
    ref_loc_note = models.TextField(blank=True, null=True, help_text=data_dict['ref_loc_note'])
    
    #def __str__(self):
        #return '%s:%s (%s)' % (self.location_01, self.location_02, self.reference)

class reference_history_action(models.Model):
    action = models.CharField(max_length=200, help_text='')
    action_description = models.TextField(blank=True, null=True, help_text='')
    action_level = models.CharField(max_length=100, blank=True, null=True, help_text='')
    #action_level_numeric
    
class res_outcome(models.Model):
    """
    An measured association with a resistance outcome.
    """
    ufid = models.TextField(blank=True, null=True, help_text=data_dict['ufid']) # update this to a ForeignKey later
    urid = models.TextField(blank=True, null=True, help_text=data_dict['urid']) # update this to a ForeignKey later
    
    fk_resistance_id = models.ForeignKey(atc_vet, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_resistance_id'])
    fk_genetic_element_id = models.TextField(blank=True, null=True, help_text=data_dict['fk_genetic_element_id']) # update this to a ForeignKey later
    
    fk_microbe_01_id = models.ForeignKey(microbe_01, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_microbe_01_id'])
    fk_microbe_02_id = models.ForeignKey(microbe_02, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_microbe_02_id'])
    
    fk_group_observe_prod_stage_id = models.ForeignKey(production_stage, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_group_observe_prod_stage_id'])
    
    fk_moa_type_id = models.ForeignKey(moa_type, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_moa_type_id'])
    fk_moa_unit_id = models.ForeignKey(moa_unit, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_moa_unit_id'])
    
    place_in_text = models.CharField(max_length=50, blank=True, null=True, help_text=data_dict['place_in_text'])
    
    contable_a = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['contable_a']) #
    contable_b = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['contable_b']) #
    contable_c = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['contable_c']) #
    contable_d = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['contable_d']) #
    prevtable_a = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True, help_text=data_dict['prevtable_a'])
    prevtable_b = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True, help_text=data_dict['prevtable_b'])
    prevtable_c = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True, help_text=data_dict['prevtable_c'])
    prevtable_d = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True, help_text=data_dict['prevtable_d'])
    
    table_n_exp = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['table_n_exp']) #
    table_n_ref = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['table_n_ref']) #
    
    odds_ratio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True, help_text=data_dict['odds_ratio']) #
    odds_ratio_lo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True, help_text=data_dict['odds_ratio_lo']) #
    odds_ratio_up = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], blank=True, null=True, help_text=data_dict['odds_ratio_up']) #
    odds_ratio_sig = models.CharField(max_length=20, blank=True, null=True, help_text=data_dict['odds_ratio_sig'])
    odds_ratio_confidence = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=3, help_text=data_dict['odds_ratio_confidence'])
    
    figure_extract = models.BooleanField(blank=True, null=True, help_text=data_dict['figure_extract'])
    figure_extract_reproducible = models.BooleanField(blank=True, null=True, help_text=data_dict['figure_extract_reproducible'])
    fk_figure_extract_method_id = models.TextField(blank=True, null=True, help_text=data_dict['fk_figure_extract_method_id']) # update this to a ForeignKey later
    extraction_num = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['extraction_num'])
    
    def __str__(self):
        return '%s_%s_%s' % (self.ufid, self.factor_urid, self.fk_resistance_id)
    
    #Clean method called automatically when model is used in a form
    def clean(self):
        #Prevalence table values must sum to approx. 100
        if all(v is not None for v in [self.prevtable_a, self.prevtable_b]) and ((self.prevtable_a + self.prevtable_b >= Decimal(99)) and (self.prevtable_a + self.prevtable_b <= Decimal(101))):
            raise ValidationError(_('Prevalences of AMR+ and AMR- within the exposed group do not sum to 100%'))
        
        if all(v is not None for v in [self.prevtable_c, self.prevtable_d]) and ((self.prevtable_c + self.prevtable_d >= Decimal(99)) and (self.prevtable_c + self.prevtable_d <= Decimal(101))):
            raise ValidationError(_('Prevalences of AMR+ and AMR- within the referent group do not sum to 100%'))
        
        #Error if # positive > total
        if all(v is not None for v in [self.contable_a, self.table_n_exp]) and (self.contable_a > self.table_n_exp):
            raise ValidationError(_('Count of AMR+ within the exposed group is greater than the total number in the exposed group'))
        
        if all(v is not None for v in [self.contable_c, self.table_n_ref]) and (self.contable_c > self.table_n_ref):
            raise ValidationError(_('Count of AMR+ within the referent group is greater than the total number in the referent group'))
    
class factor(models.Model):
    """
    An individual factor associated with antimicrobial resistance.
    """
    ufid = models.TextField(blank=True, null=True, help_text=data_dict['ufid']) # update this to a ForeignKey later
    fk_reference_id = models.ForeignKey(reference, on_delete=models.CASCADE, to_field='other_reference_id', help_text=data_dict['fk_reference_id'])
    
    #amu_id = models.ManyToManyField(atc_vet, db_table='factor_amu_join', related_name='factors_amu', help_text=data_dict['amu_id'])
    
    factor_title = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['factor_title'])
    factor_description = models.TextField(blank=True, null=True, help_text=data_dict['factor_description'])
    
    fk_host_01_id = models.ForeignKey(host_01, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_host_01_id'])
    fk_host_02_id = models.ForeignKey(host_02, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_host_02_id'])
    
    fk_group_allocate_prod_stage_id = models.ForeignKey(production_stage, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_group_allocate_prod_stage_id'])
    
    group_exposed = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['group_exposed'])
    group_referent = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['group_referent'])

    DEP_total_obs = models.CharField(blank=True, null=True, max_length=500, help_text='')
    DEP_exclude_iam = models.BooleanField(blank=True, null=True, help_text='')
    DEP_exclude_iam_reason = models.CharField(blank=True, null=True, max_length=500, help_text='')
    OLD_short_name = models.CharField(blank=True, null=True, max_length=200, help_text='')
    OLD_resistance_id = models.IntegerField(blank=True, null=True, help_text='')
    OLD_use_id = models.IntegerField(blank=True, null=True, help_text='')
    microbe_02_old_id = models.IntegerField(blank=True, null=True, help_text='')
    TEMP_use_id = models.IntegerField(blank=True, null=True, help_text='')
    exclude_cedar = models.BooleanField(blank=True, null=True, help_text=data_dict['exclude_cedar'])
    exclude_cedar_reason = models.CharField(blank=True, null=True, max_length=500, help_text=data_dict['exclude_cedar_reason'])
    exclude_is_validation = models.BooleanField(blank=True, null=True, help_text=data_dict['exclude_is_validation'])
    
    factor_v0_id = models.IntegerField(blank=True, null=True, help_text=data_dict['factor_v0_id'])
    v12_is_v1_import = models.BooleanField(blank=True, null=True, help_text=data_dict['v12_is_v1_import'])
    v12_ID_factor_v1 = models.IntegerField(blank=True, null=True, help_text=data_dict['v12_ID_factor_v1'])
    v12_ID_reference_v1 = models.IntegerField(blank=True, null=True, help_text=data_dict['v12_ID_reference_v1'])
    v12_ID_reference_v2_initial = models.IntegerField(blank=True, null=True, help_text=data_dict['v12_ID_reference_v2_initial'])
    v12_solo_extraction_2016 = models.BooleanField(blank=True, null=True, help_text=data_dict['v12_solo_extraction_2016'])
    
    def __str__(self):
        return '%s_%s' % (self.factor_title, self.fk_reference_id)

class factor_exclusion(models.Model):
    """
    A factor that is to be excluded from an iAM.AMR model.
    """
    factor_id = models.ForeignKey(factor, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['factor_id'])
    model_id = models.ForeignKey(model, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['model_id'])
    exclude_reason = models.TextField(blank=True, null=True, help_text=data_dict['exclude_reason'])
    
    def __str__(self):
        return '%s_%s' % (self.factor_id, self.model_id)

#class reference_edit(models.Model): #former matrix table m_reference_edit, now m_reference_history
    #"""
    #An edit conducted for a particular reference.
    #"""
    #other_reference_edit_id = models.IntegerField(unique=True, help_text='An additional identifier for the reference edit.')
    #reference = models.ForeignKey(reference, on_delete=models.CASCADE, blank=True, null=True, to_field='other_reference_id', help_text='The ID corresponding to the reference to which the edit was performed.')
    #user = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, blank=True, null=True, help_text='The ID corresponding to the user who made the edit.')
    #edit_date = models.DateField(blank=True, null=True, help_text='The date the edit was made, in <em>YYYY-MM-DD</em> format')
    #edit_contents = models.TextField(blank=True, null=True, help_text='A brief description of the edits made.')
    
    #def __str__(self):
        #return '%s_%s_%s_%d' % (self.reference, self.user, self.edit_date, self.other_reference_edit_id)

class reference_history_join(models.Model):
    reference = models.ForeignKey(reference, on_delete=models.CASCADE, blank=True, null=True, to_field='other_reference_id', help_text='')
    action = models.ForeignKey(reference_history_action, on_delete=models.SET_NULL, blank=True, null=True, help_text='')
    user = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, blank=True, null=True, help_text='')
    action_date = models.DateField(blank=True, null=True, help_text='') #TO DO: timestamp i.e. yyyy-mm-dd 0:00
                                     
class reference_note(models.Model): #former matrix table m_reference_note
    """
    A note written for a particular reference.
    """
    note_ref_id = models.ForeignKey(reference, on_delete=models.CASCADE, blank=True, null=True, to_field='other_reference_id', help_text=data_dict['note_ref_id'])
    note = models.TextField(blank=True, null=True, help_text=data_dict['note'])
    user_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['user_id'])
    resolved = models.BooleanField(default=False, help_text=data_dict['resolved'])
    
    def __str__(self):
        return 'Reference %s: %s' % (self.note_ref_id, self.note)