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

class ast_breakpoint_source(models.Model):
    """
    Source of breakpoint information
    """
    
    ast_breakpoint_std = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['ast_breakpoint_std'])
    ast_breakpoint_std_acronym = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['ast_breakpoint_std_acronym'])
    ast_breakpoint_std_accno = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['ast_breakpoint_std_accno'])
    ast_breakpoint_std_desc = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['ast_breakpoint_std_desc'])
    
    def __str__(self):
        return self.ast_breakpoint_std

class ast_breakpoint_version(models.Model):
    """
    Version of the source of breakpoint information
    """
    
    date_publish = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['date_publish'])
    date_last_valid = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['date_last_valid'])
    # TO DO: change to fk???
    ast_breakpoint_std = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['ast_breakpoint_std'])
    ast_breakpoint_version = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['ast_breakpoint_version'])
    clsi_std_type = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['clsi_std_type'])
    
    def __str__(self):
        return '%s: %s' % (self.ast_breakpoint_std, self.ast_breakpoint_version)
    
class evidence_type_quality(models.Model):
    """
    A tier of evidence quality
    """
    
    evidence_type = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['evidence_type'])
    evidence_type_accno = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['evidence_type_accno'])
    evidence_type_description = models.TextField(blank=True, null=True, help_text=data_dict['evidence_type_description'])
    
    def __str__(self):
        return self.evidence_type

class host_01(models.Model):
    """
    A host species.
    """
    host_name = models.CharField(max_length=20, unique=True, help_text=data_dict['host_name'])
    cedar_esr_host_01_id = models.PositiveIntegerField(unique=True, blank=True, null=True, help_text=data_dict['cedar_esr_host_01_id'])
    
    def __str__(self):
        return self.host_name

class host_02(models.Model): #TO DO: self-identification for dropdown!!
    """
    A host subtype.
    """
    #host_01_id = models.ManyToManyField(host_01, db_table='host_join', help_text=data_dict['host_01_id'])
    fk_host_01_host_02_id = models.ForeignKey(host_01, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_host_01_host_02_id'])
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
    #microbe_01_id = models.ManyToManyField(microbe_01, db_table='microbe_join', help_text=data_dict['microbe_01_id'])
    fk_microbe_01_microbe_02_id = models.ForeignKey(microbe_01, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_microbe_01_microbe_02_id'])
    microbe_subtype_name = models.CharField(max_length=100, help_text=data_dict['microbe_subtype_name'])
    DEP_old_id = models.IntegerField(blank=True, null=True, help_text=data_dict['DEP_old_id'])
    cedar_esr_microbe_02_id = models.PositiveIntegerField(unique=True, blank=True, null=True, help_text=data_dict['cedar_esr_microbe_02_id'])
    
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
    cedar_esr_production_stage_id = models.PositiveIntegerField(unique=True, blank=True, null=True, help_text=data_dict['cedar_esr_production_stage_id'])
    
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
    cedar_esr_user_id = models.PositiveIntegerField(unique=True, blank=True, null=True, help_text=data_dict['cedar_esr_user_id'])
    
    def __str__(self):
        return self.name_user

class model(models.Model):
    """
    An iAM.AMR model for which a query may be generated.
    """
    model_name = models.CharField(max_length=20, unique=True, help_text=data_dict['model_name'])
    model_description = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['model_description'])
    fk_user_model_create_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, blank=True, null=True, related_name='users_c', help_text=data_dict['fk_user_model_create_id'])
    model_create_date = models.DateField(blank=True, null=True, help_text=data_dict['model_create_date'])
    fk_user_model_maintain_id = models.ManyToManyField(legacy_user, db_table='model_user_join', help_text=data_dict['fk_user_model_maintain_id']) # TO DO: create a join table for this (instead of many to many)
    model_maintain_date = models.DateField(blank=True, null=True, help_text=data_dict['model_maintain_date'])
    
    def __str__(self):
        return self.model_name

class ast_method(models.Model):
    method = models.CharField(max_length=50, help_text=data_dict['method'])
    
    def __str__(self):
        return self.method

class cedar_exclude(models.Model):
    """
    A broad reason for exclusion from extraction.
    """
    
    exclusion = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['exclusion'])
    exclusion_type = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['exclusion_type'])
    
    def __str__(self):
        return self.exclusion
    

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
    fk_publisher_id = models.ForeignKey(publisher, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_publisher_id'])
    publish_name_alt = models.CharField(max_length=500, blank=True, null=True, default='', help_text=data_dict['publish_name_alt']) # NEW
    publish_year = models.CharField(blank=True, null=True, max_length=4, validators=[RegexValidator(r'^\d{4}$')], help_text=data_dict['publish_year'])
    publish_doi = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['publish_doi'])
    publish_pmid = models.CharField(max_length=8, validators=[RegexValidator(r'^\d{8}$')], blank=True, null=True, help_text=data_dict['publish_pmid'])
    study_title = models.TextField(default='', help_text=data_dict['study_title'])
    fk_study_design_id = models.ForeignKey(study_design, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_study_design_id'])
    study_design_detail = models.TextField(blank=True, null=True, help_text=data_dict['study_design_detail'])
    study_sample_method = models.TextField(blank=True, null=True, help_text=data_dict['study_sample_method'])
    ref_has_ast_explicit_break = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text=data_dict['ref_has_ast_explicit_break'])
    ref_has_ast_mic_table = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text=data_dict['ref_has_ast_mic_table'])
    capture_search_2016 = models.BooleanField(blank=True, null=True,help_text=data_dict['capture_search_2016'])
    capture_search_2019 = models.BooleanField(blank=True, null=True,help_text=data_dict['capture_search_2019'])
    capture_snowball = models.BooleanField(blank=True, null=True,help_text=data_dict['capture_snowball'])
    capture_submit = models.BooleanField(blank=True, null=True,help_text=data_dict['capture_submit'])
    
    #NEW. TO DO: make many to many?
    fk_ast_method_id = models.ForeignKey(ast_method, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_ast_method_id'])
    
    #t2_study_sample_collect = models.TextField(blank=True, null=True, help_text='') #TO DO help text
    DEP_study_objective = models.TextField(blank=True, null=True, help_text=data_dict['DEP_study_objective'])
    
    exclude_extraction = models.BooleanField(default=False, help_text=data_dict['exclude_extraction'])
    exclude_extraction_reason = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['exclude_extraction_reason'])
    fk_cedar_exclude_id = models.ForeignKey(cedar_exclude, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_cedar_exclude_id'])
    
    v12_is_v1_import = models.BooleanField(blank=True, null=True, help_text=data_dict['v12_is_v1_import'])
    v12_v1_id = models.BooleanField(blank=True, null=True, help_text=data_dict['v12_v1_id'])
    v12_is_in_v1_and_v2 = models.BooleanField(blank=True, null=True, help_text=data_dict['v12_is_in_v1_and_v2'])
    v12_migrated_from = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['v12_migrated_from'])
    v12_migrated_to = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['v12_migrated_to'])
    #v12_migrated_as_replace = models.BooleanField(blank=True, null=True, help_text='Specifies whether a v2 reference was identified as previously extracted in v1 by the assigned extractor, and was NOT dual-extracted.')
    v12_solo_extraction_2016 = models.BooleanField(blank=True, null=True, help_text=data_dict['v12_solo_extraction_2016'])
    
    ref_abstract = models.TextField(blank=True, null=True, help_text=data_dict['ref_abstract'])
    
    dep_CEDAR_extract_east = models.BooleanField(blank=True, null=True, help_text=data_dict['dep_CEDAR_extract_east'])
    dep_CEDAR_extract_west = models.BooleanField(blank=True, null=True, help_text=data_dict['dep_CEDAR_extract_west'])
    cedar_extract_esr = models.BooleanField(blank=True, null=True, help_text=data_dict['cedar_extract_esr'])
    topic_tab_cattle = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_cattle'])
    topic_tab_chicken = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_chicken'])
    topic_tab_swine = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_swine'])
    topic_tab_turkey = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_turkey'])
    topic_tab_ecoli = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_ecoli'])
    topic_tab_enterococcus = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_enterococcus'])
    topic_tab_salmonella = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_salmonella'])
    topic_tab_campylobacter = models.BooleanField(blank=True, null=True, help_text=data_dict['topic_tab_campylobacter'])
    dep_topic_tab_has_topic = models.BooleanField(blank=True, null=True, help_text=data_dict['dep_topic_tab_has_topic'])
    dep_topic_tab_host_free = models.CharField(blank=True, null=True, max_length=200, help_text=data_dict['dep_topic_tab_host_free'])
    dep_topic_tab_microbe_free = models.CharField(blank=True, null=True, max_length=200, help_text=data_dict['dep_topic_tab_microbe_free'])
    
    archived = models.BooleanField(blank=True, null=True, default=False, help_text=data_dict['archived'])
    archived_why = models.CharField(blank=True, null=True, max_length=200, help_text=data_dict['archived_why'])
    
    # NEW
    DEP_other_genomics = models.CharField(blank=True, null=True, max_length=500, help_text='')
    DEP_analysis_unit_ID = models.IntegerField(blank=True, null=True, help_text='')
    DEP_ref_has_mdr = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text='')
    OLD_status_ID = models.IntegerField(blank=True, null=True, help_text='')
    OLD_ref_has_wgs = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text='')
    OLD_pub_name = models.IntegerField(blank=True, null=True, help_text='')
    dep_old_id = models.IntegerField(blank=True, null=True, help_text=data_dict['dep_old_id'])
    DEL_subdivision = models.CharField(blank=True, null=True, max_length=500, help_text=data_dict['DEL_subdivision'])
    DEL_OLD_countryID = models.IntegerField(blank=True, null=True, help_text='')
    OLD_has_plasmid_type = models.BooleanField(blank=True, null=True, help_text='')
    ast_free = models.CharField(blank=True, null=True, max_length=500, help_text='')
    ref_has_data_pheno_level = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text=data_dict['ref_has_data_pheno_level'])
    ref_has_data_geno_level = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text=data_dict['ref_has_data_geno_level'])
    ref_has_esbl_factor = models.CharField(max_length=2, blank=True, null=True, choices=ANSWER_CHOICES, help_text=data_dict['ref_has_esbl_factor'])
    
    t2_ast_breakID = models.IntegerField(blank=True, null=True, help_text=data_dict['t2_ast_breakID'])
    t2_ast_break = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['t2_ast_break'])
    ref_has_ast_explicit_break = models.BooleanField(blank=True, null=True, help_text=data_dict['ref_has_ast_explicit_break'])
    DEL_journal_title = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['DEL_journal_title'])
    DEL_ID_study_location_01 = models.CharField(max_length=500, blank=True, null=True, help_text='')
    exclude_model = models.BooleanField(blank=True, null=True, help_text=data_dict['exclude_model'])
    exclude_model_reason = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['exclude_model_reason'])
    
    def __str__(self):
        return '%s: %s' % (self.key_bibtex, self.study_title)

class reference_join_location(models.Model):
    fk_reference_r_join_loc_id = models.ForeignKey(reference, on_delete=models.CASCADE, blank=True, null=True, to_field='other_reference_id', help_text=data_dict['fk_reference_r_join_loc_id'])
    fk_location_01_id = models.ForeignKey(location_01, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_location_01_id'])
    fk_location_02_r_join_loc_id = models.ForeignKey(location_02, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_location_02_r_join_loc_id'])
    ref_loc_note = models.TextField(blank=True, null=True, help_text=data_dict['ref_loc_note'])
    
    #def __str__(self):
        #return '%s:%s (%s)' % (self.location_01, self.location_02, self.reference)

class reference_history_action(models.Model):
    action = models.CharField(max_length=200, help_text='')
    action_level_coarse = models.CharField(max_length=200, blank=True, null=True, help_text='')
    action_level_coarse_num = models.IntegerField(blank=True, null=True, help_text='')
    action_description = models.TextField(blank=True, null=True, help_text='')
    action_level_fine = models.CharField(max_length=100, blank=True, null=True, help_text=data_dict['action_level_fine'])
    
    def __str__(self):
        return self.action

class genetic_element(models.Model):
    """
    A genetic element that can encode resistance
    """
    
    element_uid = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['element_uid'])
    element_name = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['element_name'])
    element_alias = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['element_alias'])
    element_type = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['element_type'])
    element_accno = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['element_accno'])
    element_family_accno = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['element_family_accno'])
    to_review = models.BooleanField(blank=True, null=True, help_text=data_dict['to_review'])
    
    def __str__(self):
        return '%s: %s' % (self.element_accession_no, self.element_name)

class factor_family(models.Model):
    """
    A factor family
    """
    
    factor_family_name = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['factor_family_name'])
    
    def __str__(self):
        return self.factor_family_name

class factor_parent(models.Model):
    """
    A parent factor
    """
    
    factor_parent_name = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['factor_parent_name'])
    
    def __str__(self):
        return self.factor_parent_name

class factor_parent_join_atc_vet(models.Model): # formerly m_factor_amu
    """
    AMU at the parent factor level
    """
    
    fk_factor_parent_fp_join_av_id = models.ForeignKey(factor_parent, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_factor_parent_fp_join_av_id'])
    fk_atc_vet_amu_id = models.ForeignKey(atc_vet, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_atc_vet_amu_id'])
    
class factor_family_join_parent_factor(models.Model):
    fk_factor_parent_ff_join_pf_id = models.ForeignKey(factor_parent, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_factor_parent_ff_join_pf_id'])
    fk_factor_family_id = models.ForeignKey(factor_family, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_factor_family_id'])

class factor(models.Model):
    """
    An individual factor associated with antimicrobial resistance.
    """
    ufid = models.PositiveIntegerField(blank=True, null=True, unique=True, help_text=data_dict['ufid']) # repeated in duplicate for each corresponding resistance outcome
    fk_reference_factor_id = models.ForeignKey(reference, blank=True, null=True, on_delete=models.CASCADE, to_field='other_reference_id', help_text=data_dict['fk_reference_factor_id'])
    
    factor_title = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['factor_title'])
    factor_description = models.TextField(blank=True, null=True, help_text=data_dict['factor_description'])
    
    fk_host_01_factor_id = models.ForeignKey(host_01, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_host_01_factor_id'])
    fk_host_02_id = models.ForeignKey(host_02, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_host_02_id'])
    
    fk_production_stage_group_allocate_id = models.ForeignKey(production_stage, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_production_stage_group_allocate_id'])
    
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
    
    factor_v0_id = models.IntegerField(blank=True, null=True, help_text=data_dict['factor_v0_id'])
    v12_is_v1_import = models.BooleanField(blank=True, null=True, help_text=data_dict['v12_is_v1_import'])
    v12_ID_factor_v1 = models.IntegerField(blank=True, null=True, help_text=data_dict['v12_ID_factor_v1'])
    v12_ID_reference_v1 = models.IntegerField(blank=True, null=True, help_text=data_dict['v12_ID_reference_v1'])
    v12_ID_reference_v2_initial = models.IntegerField(blank=True, null=True, help_text=data_dict['v12_ID_reference_v2_initial'])
    v12_solo_extraction_2016 = models.BooleanField(blank=True, null=True, help_text=data_dict['v12_solo_extraction_2016'])
    
    fk_user_extract_factor_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_user_extract_factor_id'])
    extraction_num_factor = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['extraction_num_factor'])
    extract_date_factor = models.DateField(blank=True, null=True, help_text=data_dict['extract_date_factor'])
    extract_version_factor = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['extract_version_factor'])
    
    def __str__(self):
        return '%s (Reference %s)' % (self.factor_title, self.fk_reference_factor_id)

class factor_parent_join_factor(models.Model):
    fk_factor_parent_fp_join_f_id = models.ForeignKey(factor_parent, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_factor_parent_fp_join_f_id'])
    fk_factor_fp_join_f_id = models.ForeignKey(factor, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_factor_fp_join_f_id'])

class factor_parent_metadata(models.Model):
    """
    An entry of metadata pertaining to the applicability or frequency of a parent factor
    """
    
    fk_factor_parent_fp_metadata_id = models.ForeignKey(factor_parent, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_factor_parent_fp_metadata_id'])
    fk_location_02_fp_metadata_id = models.ForeignKey(location_02, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_location_02_fp_metadata_id'])
    fk_user_entry_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, related_name='user_entry', blank=True, null=True, help_text=data_dict['fk_user_entry_id'])
    fk_user_review_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, related_name='user_review', blank=True, null=True, help_text=data_dict['fk_user_review_id'])
    frequency = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text=data_dict['frequency'])
    frequency_distribution = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['frequency_distribution'])
    frequency_param_a = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text=data_dict['frequency_param_a'])
    frequency_param_b = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text=data_dict['frequency_param_b'])
    frequency_param_c = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text=data_dict['frequency_param_c'])
    frequency_data_apply_start_year = models.IntegerField(blank=True, null=True, help_text=data_dict['frequency_data_apply_start_year'])
    frequency_data_apply_end_year = models.IntegerField(blank=True, null=True, help_text=data_dict['frequency_data_apply_end_year'])
    frequency_data_source = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['frequency_data_source'])
    frequency_data_source_added_year = models.IntegerField(blank=True, null=True, help_text=data_dict['frequency_data_source_added_year'])
    fk_evidence_type_quality_frequency_id = models.ForeignKey(evidence_type_quality, on_delete=models.SET_NULL, blank=True, null=True, related_name='evidence_quality_frequency', help_text=data_dict['fk_evidence_type_quality_frequency_id'])
    note = models.TextField(blank=True, null=True, help_text=data_dict['note'])
    is_applicable_past = models.BooleanField(blank=True, null=True, help_text=data_dict['is_applicable_past'])
    is_applicable_present = models.BooleanField(blank=True, null=True, help_text=data_dict['is_applicable_present'])
    is_applicable_future = models.BooleanField(blank=True, null=True, help_text=data_dict['is_applicable_future'])
    applicable_data_source = models.CharField(max_length=200, blank=True, null=True, help_text=data_dict['applicable_data_source'])
    applicable_data_source_added_year = models.IntegerField(blank=True, null=True, help_text=data_dict['applicable_data_source_added_year'])
    fk_evidence_type_quality_applicable_id = models.ForeignKey(evidence_type_quality, on_delete=models.SET_NULL, blank=True, null=True, related_name='evidence_quality_applicability', help_text=data_dict['fk_evidence_type_quality_applicable_id'])
    
    def __str__(self):
        return 'Metadata entry for parent factor %s (entered by %s)' % (self.fk_factor_parent_fp_metadata_id, self.fk_user_entry_id)

    
class figure_extract_method(models.Model):
    """
    A method for extracting data from figures.
    """
    
    method_name = models.CharField(max_length=200, blank=True, null=True, unique=True, help_text=data_dict['method_name'])
    method_description = models.CharField(max_length=500, blank=True, null=True, help_text=data_dict['method_description'])
    method_wpd = models.BooleanField(blank=True, null=True, help_text=data_dict['method_wpd'])
    method_convert_to_count = models.BooleanField(blank=True, null=True, help_text=data_dict['method_convert_to_count'])
    
    def __str__(self):
        return self.method_name

class res_outcome(models.Model):
    """
    An measured association with a resistance outcome.
    """
    fk_factor_ufid = models.ForeignKey(factor, on_delete=models.SET_NULL, to_field='ufid', blank=True, null=True, help_text=data_dict['fk_factor_ufid'])
    urid = models.PositiveIntegerField(blank=True, null=True, unique=True, help_text=data_dict['urid']) # this can be repeated in duplicate if a resistance outcome is extracted multiple times
    
    fk_atc_vet_resistance_id = models.ForeignKey(atc_vet, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_atc_vet_resistance_id'])
    fk_genetic_element_id = models.ForeignKey(genetic_element, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_genetic_element_id'])
    
    fk_microbe_01_id = models.ForeignKey(microbe_01, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_microbe_01_id'])
    fk_microbe_02_res_outcome_id = models.ForeignKey(microbe_02, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_microbe_02_res_outcome_id'])
    
    fk_production_stage_group_observe_id = models.ForeignKey(production_stage, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_production_stage_group_observe_id'])
    
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
    
    fk_ast_method_id = models.ForeignKey(ast_method, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_ast_method_id'])
    #fk_ast_breakpoint_source_id = models.ForeignKey(ast_method, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_ast_breakpoint_source_id'])
    breakpoint_explicit = models.CharField(max_length=50, blank=True, null=True, help_text=data_dict['breakpoint_explicit'])
    
    figure_extract = models.BooleanField(blank=True, null=True, help_text=data_dict['figure_extract'])
    figure_extract_reproducible = models.BooleanField(blank=True, null=True, help_text=data_dict['figure_extract_reproducible'])
    fk_figure_extract_method_id = models.ForeignKey(figure_extract_method, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_figure_extract_method_id'])
    
    fk_user_extract_ro_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_user_extract_ro_id'])
    extraction_num_ro = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['extraction_num_ro'])
    extract_date_ro = models.DateField(blank=True, null=True, help_text=data_dict['extract_date_ro'])
    extract_version_ro = models.PositiveIntegerField(blank=True, null=True, help_text=data_dict['extract_version_ro'])
    
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

class factor_join_res_outcome(models.Model):
    
    # TO DO: see if I can add ufid and urid here for context(?)
    fk_factor_f_join_ro_id = models.ForeignKey(factor, on_delete=models.CASCADE, blank=True, null=True, help_text=data_dict['fk_factor_f_join_ro_id'])
    fk_res_outcome_id = models.ForeignKey(res_outcome, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_res_outcome_id'])

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

class reference_join_reference_history(models.Model):
    fk_reference_r_join_rh_id = models.ForeignKey(reference, on_delete=models.CASCADE, blank=True, null=True, to_field='other_reference_id', help_text='')
    fk_reference_history_action_id = models.ForeignKey(reference_history_action, on_delete=models.SET_NULL, blank=True, null=True, help_text='')
    fk_user_r_join_rh_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, blank=True, null=True, help_text='')
    action_date = models.DateField(blank=True, null=True, help_text='') #TO DO: timestamp i.e. yyyy-mm-dd 0:00
    is_cedar_esr = models.BooleanField(default=False, help_text='')
                                     
class reference_join_reference_note(models.Model): #former matrix table m_reference_note
    """
    A note written for a particular reference.
    """
    fk_reference_r_join_rn_id = models.ForeignKey(reference, on_delete=models.CASCADE, blank=True, null=True, to_field='other_reference_id', help_text=data_dict['fk_reference_r_join_rn_id'])
    note = models.TextField(blank=True, null=True, help_text=data_dict['note'])
    fk_user_r_join_rn_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, blank=True, null=True, help_text=data_dict['fk_user_r_join_rn_id'])
    resolved = models.BooleanField(default=False, help_text=data_dict['resolved'])
    is_apply_factor = models.BooleanField(default=False, help_text=data_dict['is_apply_factor'])
    
    def __str__(self):
        return 'Reference %s: %s' % (self.fk_note_ref_id, self.note)