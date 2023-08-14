

# CEDAR Models

from decimal import Decimal
from pathlib import Path

import pandas
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .validators import UnicodeUsernameValidator

# Read in the local CEDAR_dictionary to get captions and help-text.

BASE_DIR               = Path(__file__).resolve().parent.parent
cedar_forest_dict_path = BASE_DIR / 'CEDAR_forest_dictionary.csv'
cedar_forest_dict      = pandas.read_csv(cedar_forest_dict_path, encoding='utf-8')

# Create lists from each column.
field_names    = cedar_forest_dict.field.tolist()
field_helpt    = cedar_forest_dict.description.tolist()
field_captions = cedar_forest_dict.caption.tolist()

# Make dictionaries indexed by field names.
dict_help = dict(zip(field_names, field_helpt))
dict_capt = dict(zip(field_names, field_captions))



# Clean the data dict
for key in dict_help:
    if isinstance(dict_help[key], float):
        dict_help[key] = ''
    else:
        dict_help[key] = dict_help[key].replace('\xa0',' ')

# Clean the data dict
for key in dict_capt:
    if isinstance(dict_capt[key], float):
        dict_capt[key] = ''
    else:
        dict_capt[key] = dict_capt[key].replace('\xa0',' ')


def get_help_text(field_name, dict = dict_help):
    return(dict.get(field_name, "Missing Help Text"))



class reference(models.Model): # ====================================================================================================================
    #                            ---------------------------------------------------------------------------------------------------------- REFERENCE
    # ===============================================================================================================================================

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
    

    # ID ------------------------------------------------------------------------------------------

    pid_reference       = models.PositiveIntegerField(null       = True,
                                                      blank      = True,) 

    key_bibtex                     = models.CharField(default    = '', 
                                                      max_length = 200, 
                                                      help_text  = get_help_text('key_bibtex'))

    refwk               = models.PositiveIntegerField(null       = True, 
                                                      blank      = True, 
                                                      help_text  = get_help_text('refwk'))


    # Omissions -----------------------------------------------------------------------------------

    # Archive -----------------------------------
    is_archived                 = models.BooleanField(null       = True,
                                                      blank      = True, 
                                                      default    = False, 
                                                      help_text  = get_help_text('is_archived'))

    archived_reason                = models.CharField(null       = True, 
                                                      blank      = True, 
                                                      max_length = 200, 
                                                      help_text  = get_help_text('archived_reason'))
    
    # Exclude Extract ---------------------------

    # To support users using CEDAR for Lit Searches.
    is_excluded_extract         = models.BooleanField(default    = False, 
                                                      help_text  = get_help_text('is_excluded_extract'))

    excluded_extract_reason        = models.TextField(null       = True, 
                                                      blank      = True, 
                                                      help_text  = get_help_text('excluded_extract_reason'))

    excluded_extract_reason_type  = models.ForeignKey(to         = 'cedar_exclude', 
                                                      null       = True, 
                                                      blank      = True, 
                                                      on_delete  = models.SET_NULL, 
                                                      help_text  = get_help_text('excluded_extract_reason_type'))                                                    
    
    # Exclude Model -----------------------------
    is_excluded_model           = models.BooleanField(null       = True, 
                                                      blank      = True, 
                                                      help_text  = get_help_text('is_excluded_model'))

    excluded_model_reason          = models.CharField(null       = True, 
                                                      blank      = True, 
                                                      max_length = 500, 
                                                      help_text  = get_help_text('excluded_model_reason'))
    

    # Meta-data -----------------------------------------------------------------------------------
    publisher                     = models.ForeignKey(to         = 'publisher', 
                                                      null       = True, 
                                                      blank      = True, 
                                                      on_delete  = models.SET_NULL,                                  
                                                      help_text  = get_help_text('publisher'))

    publisher_name_alt             = models.CharField(blank      = True,
                                                      default    = '', 
                                                      max_length = 500, 
                                                      help_text  = get_help_text('publisher_name_alt'))

    publish_year                   = models.CharField(blank      = True, 
                                                      max_length = 4,  
                                                      help_text  = get_help_text('publish_year'), 
                                                      validators = [RegexValidator(r'^\d{4}$')])

    publish_doi                    = models.CharField(blank      = True, 
                                                      max_length = 500, 
                                                      help_text  = get_help_text('publish_doi'))

    publish_pmid                   = models.CharField(blank      = True, 
                                                      max_length = 8,  
                                                      help_text  = get_help_text('publish_pmid'), 
                                                      validators = [RegexValidator(r'^\d{8}$')])
    
    ref_title                      = models.TextField(default    = '', 
                                                      help_text  = get_help_text('ref_title'))

    ref_author                     = models.TextField(blank      = True, 
                                                      help_text  = get_help_text('ref_author'))

    ref_abstract                   = models.TextField(blank      = True, 
                                                      help_text  = get_help_text('ref_abstract'))
    
    ref_country                   = models.ForeignKey(to         = 'location_01', 
                                                      null       = True,
                                                      blank      = False,
                                                      on_delete  = models.SET_NULL)

    # Reference Features --------------------------------------------------------------------------

    # Study Design ------------------------------
    study_design                  = models.ForeignKey(to         = 'study_design', 
                                                      null       = True,
                                                      blank      = True,  
                                                      on_delete  = models.SET_NULL,
                                                      help_text  = get_help_text('study_design'))
    
    study_design_detail            = models.TextField(blank      = True,  
                                                      help_text  = get_help_text('study_design_detail'))

    study_sample_method            = models.TextField(blank      = True,  
                                                      help_text  = get_help_text('study_sample_method'))
    

    # AST ---------------------------------------
    ref_ast_method                = models.ForeignKey(to         = 'ast_method_old',
                                                      null       = True, 
                                                      blank      = True, 
                                                      on_delete  = models.SET_NULL)
    
    hist_ref_has_ast_explicit_break     = models.CharField(null       = True, 
                                                      blank      = True, 
                                                      max_length = 2, 
                                                      choices    = ANSWER_CHOICES, 
                                                      help_text  = get_help_text('ref_has_ast_explicit_break'))

    ref_has_ast_explicit_break                                = models.ForeignKey(
        to         = 'logic_dictionary',
        null       = True,
        blank      = True, 
        on_delete  = models.SET_NULL, 
        help_text  = get_help_text('ref_has_ast_explicit_break'),
        related_name = 'ast_explicit_break')

    

    hist_ref_has_ast_mic_table          = models.CharField(null       = True, 
                                                      blank      = True, 
                                                      max_length = 2, 
                                                      choices    = ANSWER_CHOICES, 
                                                      help_text  = get_help_text('ref_has_ast_mic_table'))

    ref_has_ast_mic_table                               = models.ForeignKey(
        to         = 'logic_dictionary', 
        null       = True,
        blank      = True, 
        on_delete  = models.SET_NULL, 
        help_text  = get_help_text('ref_has_ast_mic_table'), 
        related_name = 'ast_mic_table')




    # Topic -------------------------------------
    topic_tab_cattle        = models.BooleanField(blank=True, null=True, help_text=get_help_text('topic_tab_cattle'))
    topic_tab_chicken       = models.BooleanField(blank=True, null=True, help_text=get_help_text('topic_tab_chicken'))
    topic_tab_swine         = models.BooleanField(blank=True, null=True, help_text=get_help_text('topic_tab_swine'))
    topic_tab_turkey        = models.BooleanField(blank=True, null=True, help_text=get_help_text('topic_tab_turkey'))
    topic_tab_ecoli         = models.BooleanField(blank=True, null=True, help_text=get_help_text('topic_tab_ecoli'))
    topic_tab_enterococcus  = models.BooleanField(blank=True, null=True, help_text=get_help_text('topic_tab_enterococcus'))
    topic_tab_salmonella    = models.BooleanField(blank=True, null=True, help_text=get_help_text('topic_tab_salmonella'))
    topic_tab_campylobacter = models.BooleanField(blank=True, null=True, help_text=get_help_text('topic_tab_campylobacter'))

    capture_search_2016     = models.BooleanField(blank=True, null=True, help_text=get_help_text('capture_search_2016'))
    capture_search_2019     = models.BooleanField(blank=True, null=True, help_text=get_help_text('capture_search_2019'))
    capture_2019_reject     = models.BooleanField(blank=True, null=True, help_text=get_help_text('capture_search_2019'))
    capture_snowball        = models.BooleanField(blank=True, null=True, help_text=get_help_text('capture_snowball'))
    capture_submit          = models.BooleanField(blank=True, null=True, help_text=get_help_text('capture_submit'))

    source_project               =  models.ForeignKey(to         = 'source_project',
                                                      null       = True, 
                                                      blank      = True, 
                                                      on_delete  = models.SET_NULL)           

    cedar_extract_esr           = models.BooleanField(blank=True, null=True, help_text=get_help_text('cedar_extract_esr'))
    cedar_extract_turkey_update = models.BooleanField(blank=True, null=True, help_text=get_help_text('cedar_extract_turkey_update'))

    
    # Historical ----------------------------------------------------------------------------------
    v12_is_v1_import          = models.BooleanField(blank=True, null=True, help_text=get_help_text('v12_is_v1_import'))
    v12_v1_id         = models.PositiveIntegerField(blank=True, null=True, help_text=get_help_text('v12_v1_id'))
    v12_is_in_v1_and_v2       = models.BooleanField(blank=True, null=True, help_text=get_help_text('v12_is_in_v1_and_v2'))
    v12_migrated_from = models.PositiveIntegerField(blank=True, null=True, help_text=get_help_text('v12_migrated_from'))
    v12_migrated_to   = models.PositiveIntegerField(blank=True, null=True, help_text=get_help_text('v12_migrated_to'))
    #v12_migrated_as_replace = models.BooleanField(blank=True, null=True, help_text='Specifies whether a v2 reference was identified as previously extracted in v1 by the assigned extractor, and was NOT dual-extracted.')
    v12_solo_extraction_2016  = models.BooleanField(blank=True, null=True, help_text=get_help_text('v12_solo_extraction_2016'))
        
    v2_fk_m_reference_history_id        = models.ForeignKey('reference_join_reference_history', on_delete=models.SET_NULL, blank=True, null=True, help_text=get_help_text('v2_fk_m_reference_history_id'))
    v2_fk_reference_history_last_action = models.ForeignKey('reference_history_action', on_delete=models.SET_NULL, blank=True, null=True, help_text=get_help_text('v2_fk_reference_history_last_action'))
    v2_fk_user_reference_history_last_action = models.ForeignKey('legacy_user', on_delete=models.SET_NULL, blank=True, null=True, help_text=get_help_text('v2_fk_user_reference_history_last_action'))
    fk_reference_status_id = models.IntegerField(blank=True, null=True, help_text=get_help_text('fk_reference_status_id')) # TO DO: this will be a foreign key to a new reference status table

    def __str__(self):
        return '%s: %s' % (self.key_bibtex, self.ref_title)
    
    def get_absolute_url(self):
        return reverse("detail_reference", args=[str(self.id)])





class factor(models.Model): # =========================================================================================
    # ---------------------------------------------------------------------------------------------------------- FACTOR
    # =================================================================================================================

    """
    A factor associated with antimicrobial resistance.
    """
    
    reference                                              = models.ForeignKey(
        to        = 'reference', 
        default   = 99999, 
        on_delete = models.CASCADE, 
        help_text = get_help_text('reference'))

    pid_factor                                   = models.PositiveIntegerField(
        blank     = True, 
        null      = True, 
        help_text = get_help_text('pid_factor')) 


    # Factor Details ----------------------------------------------------------
    # -------------------------------------------------------------------------

    factor_title                                            = models.TextField(
        blank     = True, 
        null      = True, # To Change
        help_text = get_help_text('factor_title'))

    factor_description                                      = models.TextField(
        blank     = True, 
        null      = True, # To Change
        help_text = get_help_text('factor_description'))
    
    group_factor                                            = models.TextField(
        null      = True, 
        blank     = True, 
        help_text = get_help_text('group_factor'))

    group_comparator                                        = models.TextField(
        null      = True, 
        blank     = True, 
        help_text = get_help_text('group_comparator'))

    group_allocate_production_stage                        = models.ForeignKey(
        to        = 'production_stage', 
        null      = True, 
        blank     = True, 
        on_delete = models.SET_NULL,                                       
        help_text = get_help_text('group_allocate_production_stage'))
    

    # Factor Host Details -----------------------------------------------------
    # -------------------------------------------------------------------------

    host_level_01                                          = models.ForeignKey(
        to        = 'host_01', 
        blank     = True, 
        null      = True, 
        on_delete = models.SET_NULL, 
        help_text = get_help_text('host_level_01'))

    # To be depreciated; see scheme_update_new_subhost
    host_level_02                                          = models.ForeignKey(
        to        = 'host_02', 
        blank     = True, 
        null      = True, 
        on_delete = models.SET_NULL, 
        help_text = get_help_text('host_level_02'))
    
    # Not yet in use; see scheme_update_new_subhost
    host_production_stream                                 = models.ForeignKey(
        to        = 'production_stream',
        null      = True,
        on_delete = models.SET_NULL,
        help_text = get_help_text('host_production_stream'))

    # Not yet in use; see scheme_update_new_subhost
    host_life_stage                                        = models.ForeignKey(
        to        = 'host_life_stage',
        null      = True,
        on_delete = models.SET_NULL,
        help_text = get_help_text('host_life_stage'))
    
    
    exclude_cedar = models.BooleanField(blank=True, null=True) # to do: rename to depreciated

    # The host_01_id used in the ESR (Enterococcus Scoping Review), which differentiated between beef cattle and dairy cattle at the host_main level.
    # Here, host_02_id records records beef vs dairy cattle using host_sub. # The host_01_id before Beef Cattle (6) and Dairy Cattle (5) are collapsed into Cattle. 
    HIST_ESR_host_01_id = models.IntegerField(blank=True, null=True)
    
    # Eventual to do: add fk to factor history table (factor_history table: not created yet). Other table: reference_history (legacy info in the reference table, but the static tables that those fks in the reference table refer to are not loaded into the db yet)
    
    #fk_extract_factor_user_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, blank=True, null=True, help_text=get_help_text('fk_extract_factor_user_id'))
    #extract_date_factor = models.DateField(blank=True, null=True, help_text=get_help_text('extract_date_factor'))
    
    def __str__(self):
        return '%s (Reference %s)' % (self.factor_title, self.reference)

    def get_absolute_url(self):
        return reverse("detail_factor", kwargs={'reference_id': self.reference_id, 
                                                'pk': self.id})
    




class res_outcome(models.Model): # ==================================================================================================================
    # ----------------------------------------------------------------------------------------------------------------------------------- RES_OUTCOME
    # ===============================================================================================================================================

    """
    An measured association with a resistance outcome.
    """

    factor                             = models.ForeignKey(to        = 'factor', 
                                                           on_delete = models.CASCADE, 
                                                           blank     = True, 
                                                           null      = True,                           # SHOULD BOTH BE FALSE
                                                           help_text = get_help_text('factor'))
    
    pid_ro                   = models.PositiveIntegerField(blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('pid_ro'))
    
    resistance                         = models.ForeignKey(to        = 'atc_vet', 
                                                           on_delete = models.SET_NULL, 
                                                           blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('resistance'))

    resistance_gene                    = models.ForeignKey(to        = 'genetic_element', 
                                                           on_delete = models.SET_NULL, 
                                                           blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('resistance_gene'))
    
    microbe_level_01                   = models.ForeignKey(to        = 'microbe_01', 
                                                           on_delete = models.SET_NULL, 
                                                           blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('microbe_level_01'))

    microbe_level_02                   = models.ForeignKey(to        = 'microbe_02', 
                                                           on_delete = models.SET_NULL, 
                                                           blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('microbe_level_02'))
    
    group_observe_production_stage     = models.ForeignKey(to        = 'production_stage', 
                                                           null      = True, 
                                                           blank     = True, 
                                                           on_delete = models.SET_NULL, 
                                                           help_text = get_help_text('group_observe_production_stage'))
        

    # Quantitative Data ---------------------------------------------------------------------------

    moa_type                           = models.ForeignKey(to        = 'moa_type', 
                                                           on_delete = models.SET_NULL, 
                                                           blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('moa_type'))

    moa_unit                           = models.ForeignKey(to        = 'moa_unit', 
                                                           on_delete = models.SET_NULL, 
                                                           blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('moa_unit'))
    
    place_in_text                       = models.TextField(blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('place_in_text'))

    # Contingency Table
    contable_a = models.PositiveIntegerField(blank=True, null=True, help_text=get_help_text('contable_a'))
    contable_b = models.PositiveIntegerField(blank=True, null=True, help_text=get_help_text('contable_b'))
    contable_c = models.PositiveIntegerField(blank=True, null=True, help_text=get_help_text('contable_c'))
    contable_d = models.PositiveIntegerField(blank=True, null=True, help_text=get_help_text('contable_d'))

    # Prevalence Table
    # MinValueValidator at 0.01 ensures no negative numbers can be entered
    prevtable_a = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], blank=True, null=True, help_text=get_help_text('prevtable_a'))
    prevtable_b = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], blank=True, null=True, help_text=get_help_text('prevtable_b'))
    prevtable_c = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], blank=True, null=True, help_text=get_help_text('prevtable_c'))
    prevtable_d = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], blank=True, null=True, help_text=get_help_text('prevtable_d'))
    
    # Contingency / Prevalence Table Margin Totals
    table_n_ab = models.PositiveIntegerField(blank=True, null=True, help_text=dict_help.get('table_n_ab'))
    table_n_cd = models.PositiveIntegerField(blank=True, null=True, help_text=get_help_text('table_n_cd'))
    
    # Odds Ratios
    odds_ratio            = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], blank=True, null=True, help_text=get_help_text('odds_ratio')) #
    odds_ratio_lo         = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], blank=True, null=True, help_text=get_help_text('odds_ratio_lo')) #
    odds_ratio_up         = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], blank=True, null=True, help_text=get_help_text('odds_ratio_up')) #
    odds_ratio_sig        =    models.CharField(max_length=20, blank=True, null=True, help_text=get_help_text('odds_ratio_sig'))
    odds_ratio_confidence = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=3, help_text=get_help_text('odds_ratio_confidence'))
    

    # AST Method and Details ----------------------------------------------------------------------

    ast_method                                             = models.ForeignKey(
        to        = 'ast_method', 
        null      = True, 
        blank     = True, 
        on_delete = models.SET_NULL, 
        help_text = get_help_text('ast_method'))

    ast_reference_standard             = models.ForeignKey(to        = 'ast_reference_standard', 
                                                           on_delete = models.SET_NULL, 
                                                           blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('ast_reference_standard'))

    ast_breakpoint_version             = models.ForeignKey(to        = 'ast_reference_standard_version',
                                                           on_delete = models.SET_NULL, 
                                                           blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('ast_breakpoint_version'))

    ast_breakpoint_is_explicit       = models.BooleanField(blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('ast_breakpoint_is_explicit'))
    

    # Figure Extraction Method and Details --------------------------------------------------------

    is_figure_extract                = models.BooleanField(blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('is_figure_extract'))

    figure_extract_method              = models.ForeignKey(to        = 'figure_extract_method',
                                                           on_delete = models.SET_NULL, 
                                                           blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('figure_extract_method'))

    figure_extract_reproducible      = models.BooleanField(blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('figure_extract_reproducible'))
    

    # User, Project, and Date of Extraction -------------------------------------------------------

    extract_user_legacy                = models.ForeignKey(to        = 'legacy_user', 
                                                           on_delete = models.SET_NULL, 
                                                           blank     = True, 
                                                           null      = True, 
                                                           help_text = get_help_text('extract_user_legacy'))
                                                           
    extract_project                     = models.ForeignKey(to        = 'source_project', 
                                                            on_delete = models.SET_NULL, 
                                                            blank     = True, 
                                                            null      = True, 
                                                            help_text = get_help_text('extract_project'))

    extract_date                         = models.DateField(default   = timezone.now, 
                                                            help_text = get_help_text('extract_date'))
    

    # Historical Fields ---------------------------------------------------------------------------

    # ADD status field (name = "fk_status_id") when resistance outcome status field is made
    factor_v0_id = models.IntegerField(blank=True, null=True, help_text=get_help_text('factor_v0_id'))
    v12_is_v1_import = models.BooleanField(blank=True, null=True, help_text=get_help_text('v12_is_v1_import'))
    v12_ID_factor_v1 = models.IntegerField(blank=True, null=True, help_text=get_help_text('v12_ID_factor_v1'))
    v12_ID_reference_v1 = models.IntegerField(blank=True, null=True, help_text=get_help_text('v12_ID_reference_v1'))
    v12_ID_reference_v2_initial = models.IntegerField(blank=True, null=True, help_text=get_help_text('v12_ID_reference_v2_initial'))
    v12_solo_extraction_2016 = models.BooleanField(blank=True, null=True, help_text=get_help_text('v12_solo_extraction_2016'))
    
    def get_absolute_url(self):
        x = factor.objects.get(pk=self.factor_id)
        return reverse('resout-details', kwargs={'pk': self.pk, 'factor_id': self.factor_id, 'reference_id': x.reference_id})


    def __str__(self):
        return '%s_%s' % (self.factor, self.resistance)

    
    
    # The clean method is called automatically when model is used in a form. These are commented out for now, as extracted data may have errors that mean these conditions are rarely met
    #def clean(self):
        # Prevalence table values must sum to approx. 100. Currently not used, as prevtable_b and prevtable_d (AMR- %s) are rarely provided
        #if all(v is not None for v in [self.prevtable_a, self.prevtable_b]) and ((self.prevtable_a + self.prevtable_b >= Decimal(99)) and (self.prevtable_a + self.prevtable_b <= Decimal(101))):
            #raise ValidationError(_('Prevalences of AMR+ and AMR- within the exposed group do not sum to 100%'))
        
        #if all(v is not None for v in [self.prevtable_c, self.prevtable_d]) and ((self.prevtable_c + self.prevtable_d >= Decimal(99)) and (self.prevtable_c + self.prevtable_d <= Decimal(101))):
            #raise ValidationError(_('Prevalences of AMR+ and AMR- within the referent group do not sum to 100%'))
        
        # Error if # positive > total
        #if all(v is not None for v in [self.contable_a, self.table_n_exp]) and (self.contable_a > self.table_n_exp):
            #raise ValidationError(_('Count of AMR+ within the exposed group is greater than the total number in the exposed group'))
        
        #if all(v is not None for v in [self.contable_c, self.table_n_ref]) and (self.contable_c > self.table_n_ref):
            #raise ValidationError(_('Count of AMR+ within the referent group is greater than the total number in the referent group'))



# SECONDARY TABLES (Alphabetical Order) ===============================================================================
# =====================================================================================================================


class ast_reference_standard(models.Model): # =========================================================================
    #                                        --------------------------------------------------- AST_REFERENCE_STANDARD
    # =================================================================================================================

    """
    The reference standard for interpreting the Minimum Inhibitory Concentration (MIC).
    """
    
    ast_reference_std_name    = models.CharField(max_length=200, help_text=get_help_text('ast_reference_std_name'))
    ast_reference_std_acronym = models.CharField(max_length=200, blank=True, help_text=get_help_text('ast_reference_std_acronym'))
    ast_reference_std_accno   = models.CharField(max_length=200, blank=True, help_text=get_help_text('ast_reference_std_accno'))
    ast_reference_std_desc    = models.CharField(max_length=200, blank=True, help_text=get_help_text('ast_reference_std_desc'))
    
    def __str__(self):
        return self.ast_reference_std_name



class ast_reference_standard_version(models.Model): # =========================================================================
    #                                        --------------------------------------------------- AST_BREAKPOINT_VERSION
    # =================================================================================================================

    """
    Version of the source of breakpoint information
    """
    
    ast_reference_std_version     = models.CharField(max_length=200, blank=True, help_text=get_help_text('ast_breakpoint_version'))
    
    ast_reference_std             = models.ForeignKey(to        = ast_reference_standard, 
                                                      on_delete = models.CASCADE, 
                                                      help_text = get_help_text('ast_reference_std'))
    
    ast_reference_std_pub_year    = models.PositiveSmallIntegerField(blank      = True, 
                                                                     help_text  = get_help_text('ast_reference_std_pub_year'))
    
    clsi_std_doc_name              = models.CharField(max_length=200, blank=True, help_text=get_help_text('clsi_std_doc_name'))
    
    def __str__(self):
        return '%s: %s' % (self.ast_reference_std, self.ast_reference_std_version)



class ast_method_old(models.Model): # =================================================================================
    #                             -------------------------------------------------------------------------- AST_METHOD
    # =================================================================================================================

    """
    Microbial susceptibility testing methods, and 
    """
    
    ast_method_name            = models.CharField(max_length=50, help_text=get_help_text('method'))
    
    def __str__(self):
        return self.ast_method_name


class ast_method(models.Model): # =====================================================================================
    #                                 ---------------------------------------------------------------------- AST_METHOD
    # =================================================================================================================
    
    """
    Microbial susceptibility testing methods. 
    """

    ast_method_name                                         = models.CharField(
        max_length = 100, 
        help_text  = get_help_text('ast_method_name'))

    ast_method_accno                                        = models.CharField(
        max_length = 100, 
        help_text  = get_help_text('ast_method_accno'))

    ast_method_type_name                                    = models.CharField(
        max_length = 100, 
        help_text  = get_help_text('ast_method_type_name'))

    ast_method_type_accno                                   = models.CharField(
        max_length = 100, 
        help_text  = get_help_text('ast_method_type_accno'))

    ast_method_is_ast_type                               = models.BooleanField(
        help_text = get_help_text('ast_method_is_ast_type'))

    hist_ast_method_id                                   = models.IntegerField(
        null      = True, 
        blank     = True, 
        help_text = get_help_text('hist_ast_method_id'))
    
    def __str__(self):
        return self.ast_method_name


class atc_vet(models.Model): # ========================================================================================
    #                          -------------------------------------------------------------------------------- ATC_VET
    # =================================================================================================================

    """
    Antimicrobials, from the ATC and ATCvet indices.
    """

    levelname_1 = models.CharField(max_length=100,                        help_text=get_help_text('levelname_1'))
    levelname_2 = models.CharField(max_length=100, blank=True, null=True, help_text=get_help_text('levelname_2'))
    levelname_3 = models.CharField(max_length=100, blank=True, null=True, help_text=get_help_text('levelname_3'))
    levelname_4 = models.CharField(max_length=200, blank=True, null=True, help_text=get_help_text('levelname_4'))
    levelname_4_coarse       = models.CharField(max_length=100, blank=True, null=True, help_text=get_help_text('levelname_4_coarse'))
    levelname_5 = models.CharField(max_length=100, blank=True, null=True, help_text=get_help_text('levelname_5'))
    levelname_5_alt          = models.CharField(max_length=100, blank=True, null=True, help_text=get_help_text('levelname_5_alt'))
    levelname_5_comb_example = models.CharField(max_length=100, blank=True, null=True, help_text=get_help_text('levelname_5_comb_example'))
    levelcode_1 = models.CharField(max_length=4,   blank=True, null=True, help_text=get_help_text('levelcode_1'))
    levelcode_2 = models.CharField(max_length=8,   blank=True, null=True, help_text=get_help_text('levelcode_2'))
    levelcode_3 = models.CharField(max_length=10,  blank=True, null=True, help_text=get_help_text('levelcode_3'))
    levelcode_4 = models.CharField(max_length=12,  blank=True, null=True, help_text=get_help_text('levelcode_4'))
    levelcode_5 = models.CharField(max_length=16,  blank=True, null=True, help_text=get_help_text('levelcode_5'))
    is_added    = models.BooleanField(                                    help_text=get_help_text('is_added'))
    is_gene     = models.BooleanField(                                    help_text=get_help_text('is_gene'))
    aro_number  = models.IntegerField(             blank=True, null=True, help_text=get_help_text('aro_number'))
    is_duplicate = models.BooleanField(                                   help_text=get_help_text('is_duplicate'))
    
    def __str__(self):
        if self.levelname_5 is not None:
            ident = self.levelname_5
        else:
            ident = self.levelname_1
        return ident



class cedar_exclude(models.Model): # ==================================================================================
    #                                -------------------------------------------------------------------- CEDAR_EXCLUDE
    # =================================================================================================================

    """
    A broad reason for exclusion from extraction.
    """
    
    exclusion = models.CharField(max_length=500, blank=True, null=True, help_text=get_help_text('exclusion'))
    exclusion_type = models.CharField(max_length=500, blank=True, null=True, help_text=get_help_text('exclusion_type'))
    
    def __str__(self):
        return self.exclusion



class evidence_type_quality(models.Model): # ==========================================================================
    #                                        ---------------------------------------------------- EVIDENCE_TYPE_QUALITY
    # =================================================================================================================

    """
    A tier of evidence quality
    """
    
    evidence_type = models.CharField(max_length=500, blank=True, null=True, help_text=get_help_text('evidence_type'))
    evidence_type_accno = models.CharField(max_length=500, blank=True, null=True, help_text=get_help_text('evidence_type_accno'))
    evidence_type_description = models.TextField(blank=True, null=True, help_text=get_help_text('evidence_type_description'))
    
    def __str__(self):
        return self.evidence_type



class figure_extract_method(models.Model): # ==========================================================================
    #                                        ---------------------------------------------------- FIGURE_EXTRACT_METHOD
    # =================================================================================================================
    """
    A method for extracting data from figures.
    """
    
    method_name = models.TextField(blank=True, null=True, unique=True, help_text=get_help_text('method_name'))
    method_description = models.TextField(blank=True, null=True, help_text=get_help_text('method_description'))
    method_wpd = models.BooleanField(blank=True, null=True, help_text=get_help_text('method_wpd'))
    method_convert_to_count = models.BooleanField(blank=True, null=True, help_text=get_help_text('method_convert_to_count'))
    
    def __str__(self):
        return self.method_name



class genetic_element(models.Model): # ================================================================================
    #                                  ---------------------------------------------------------------- GENETIC_ELEMENT
    # =================================================================================================================
    
    """
    Genetic elements (genes, gene families) expected to encode resistance determinants.
    """
    
    genetic_element_name                                    = models.CharField(
        max_length = 200, 
        help_text  = get_help_text('element_name'))

    genetic_element_alias                                   = models.CharField(
        blank      = True, 
        max_length = 200, 
        help_text  = get_help_text('element_alias'))

    genetic_element_type                                    = models.CharField(
        max_length = 200, 
        help_text  = get_help_text('element_type'))

    genetic_element_accno                                   = models.CharField(
        blank      = True, 
        max_length = 200, 
        help_text  = get_help_text('element_accno'))

    genetic_element_family_accno                            = models.CharField(
        blank      = True, 
        max_length = 200, 
        help_text  = get_help_text('element_family_accno'))
    
    def __str__(self):
        return '%s (%s)' % (self.genetic_element_name, self.genetic_element_accno)



class host_01(models.Model): # ========================================================================================
#                              -------------------------------------------------------------------------------- HOST_01
# =====================================================================================================================

    """
    Hosts, differentiated at level (01) of typing (species).
    """

    host_01_name                    = models.CharField(unique     = True, 
                                                       max_length = 20, 
                                                       help_text  = get_help_text('host_01_name')) # Change to host_level_01_name
    
    def __str__(self):
        return self.host_01_name



class host_02(models.Model): # ========================================================================================
#                              -------------------------------------------------------------------------------- HOST_02
# =====================================================================================================================

    """
    Hosts, differentiated at level (02) of typing. 
    The concept of a level 02 of host typing is being depreciated; see NEWHOST02
    """
    
    host_subtype_name               = models.CharField(max_length = 100,
                                                       help_text  = get_help_text('host_subtype_name')) #TODO: Change to host_level_02_name

    host_level_01                        = models.ForeignKey(to         = host_01, 
                                                       null       = True, 
                                                       on_delete  = models.SET_NULL,
                                                       help_text  = get_help_text('host_level_01')) # TODO: Change to host_level_01

    # These fields will be removed when the host_production_stream and host_life_stage are linked 
    # directly to the factor table.

    host_production_stream     = models.ForeignKey(to        = 'production_stream',
                                                   null      = True,
                                                   on_delete = models.SET_NULL)
    
    host_life_stage            = models.ForeignKey(to        = 'host_life_stage', 
                                                   null      = True,
                                                   on_delete = models.SET_NULL)
    
    DEP_sel_beef = models.BooleanField(blank=True, null=True, help_text=get_help_text('DEP_sel_beef'))
    DEP_sel_broil = models.BooleanField(blank=True, null=True, help_text=get_help_text('DEP_sel_broil'))

    # The host_01_id before Beef Cattle (6) and Dairy Cattle (5) are collapsed into Cattle. 
    HIST_host_01_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.host_subtype_name
    


class host_life_stage(models.Model): # ================================================================================
#                                      ---------------------------------------------------------------- HOST_LIFE_STAGE
# =====================================================================================================================

    """
    The host animal life stage (e.g., "Egg", "Chick", "Adult"; "Calf", "Heifer", "Backgrounder").
    """
    
    host_life_stage_name =       models.CharField(max_length = 100)
    applies_to_hosts     = models.ManyToManyField(to         = host_01,
                                                  db_table   = 'host_life_stage_join_host_level_01')
    
    def __str__(self):
        return self.host_life_stage_name



class legacy_user(models.Model): # ====================================================================================
#                                  ------------------------------------------------------------------------ LEGACY_USER
# =====================================================================================================================

    """
    A CEDAR user from the legacy database (Microsoft Access).
    """
    name_user = models.CharField(max_length=50, unique=True, help_text=get_help_text('name_user'))
    cedar_esr_user_id = models.PositiveIntegerField(unique=True, blank=True, null=True, help_text=get_help_text('cedar_esr_user_id'))
    
    def __str__(self):
        return self.name_user



class location_01(models.Model): # ====================================================================================
#                              ---------------------------------------------------------------------------- LOCATION_01
# =====================================================================================================================

    """
    A location (country-level).
    """
    
    country                                = models.CharField(max_length=100,  blank=False, null=False, unique=True,  help_text=get_help_text('country_area'), default="N/A")
    iso_3166_1_alpha3                      = models.CharField(max_length=10,   blank=True,  null=True,  unique=True,  help_text=get_help_text('iso_country_code_3'))
    iso_3166_1_alpha2                      = models.CharField(max_length=10,   blank=True,  null=True,  unique=True,  help_text=get_help_text('iso_country_code_2'))
    iso_3166_1_numeric                     = models.IntegerField(              blank=True,  null=True,  unique=True,  help_text=get_help_text('iso_country_code_1'))
    m49                                    = models.IntegerField(              blank=True,  null=True,  unique=True,  help_text=get_help_text('m49_code'))
    loc_subregion_name                     = models.CharField(max_length=100,  blank=True,  null=True,  help_text=get_help_text('name_subregion'))
    loc_subregion_code                     = models.IntegerField(              blank=True,  null=True,  help_text=get_help_text('code_subregion'))
    loc_intermediate_subregion_name        = models.CharField(max_length=100,  blank=True,  null=True,  help_text=get_help_text('name_intermediate_subregion'))
    loc_intermediate_subregion_code        = models.IntegerField(              blank=True,  null=True,  help_text=get_help_text('code_intermediate_subregion'))
    loc_region_name                        = models.CharField(max_length=100,  blank=True,  null=True,  help_text=get_help_text('name_region'))
    loc_region_code                        = models.IntegerField(              blank=True,  null=True,  help_text=get_help_text('code_region'))
    is_least_developed_countries           = models.BooleanField(              blank=True,  null=True,  help_text=get_help_text('bin_least_developed_countries'))
    is_land_lock_least_developed_countries = models.BooleanField(              blank=True,  null=True,  help_text=get_help_text('bin_land_lock_least_developed_countries'))
    is_small_island_developing_states      = models.BooleanField(              blank=True,  null=True,  help_text=get_help_text('bin_small_island_developing_states'))
    is_developing                          = models.BooleanField(              blank=True,  null=True,  help_text=get_help_text('bin_developing'))
    
    def __str__(self):
        return self.country



class location_02(models.Model): # ====================================================================================
#                                  ------------------------------------------------------------------------ LOCATION_02
# =====================================================================================================================

    """
    A location (a subdivision below country-level).
    """
    
    fk_location_02_location_01_id = models.ForeignKey(location_01, on_delete=models.DO_NOTHING, blank=True, null=True, to_field='iso_3166_1_alpha2')
    subdivision_code = models.CharField(max_length=3)
    subdivision = models.CharField(max_length=100, help_text=get_help_text('subdivision'))
    subdivision_type = models.CharField(max_length=200, blank=True, null=True, help_text=get_help_text('subdivision_type'))
    cipars_region_national = models.BooleanField(help_text=get_help_text('cipars_region_national'))
    cipars_region_atlantic = models.BooleanField(help_text=get_help_text('cipars_region_atlantic'))
    cipars_region_maritimes = models.BooleanField(help_text=get_help_text('cipars_region_maritimes'))
    cipars_region_prairies = models.BooleanField(help_text=get_help_text('cipars_region_prairies'))
    
    def __str__(self):
        return '%s (%s)' % (self.subdivision, self.subdivision_type)



class location_sub(models.Model): # ===================================================================================
#                                  ----------------------------------------------------------------------- LOCATION_SUB
# =====================================================================================================================

    """
    A location (sub-country level), such as a state, province, or parish.
    """
    
    iso_3166_1_alpha2       = models.ForeignKey(to=location_01, 
                                                on_delete=models.DO_NOTHING, 
                                                blank=False, 
                                                null=False, 
                                                to_field='iso_3166_1_alpha2', 
                                                db_column='iso_3166_1_alpha2',
                                                help_text=get_help_text('iso_3166_1_alpha2'))

    subdivision_type        = models.CharField(max_length=100, 
                                               blank=True, 
                                               null=True, 
                                               help_text=get_help_text('subdivision_type'))

    subdivision             = models.CharField(max_length=100, 
                                               help_text=get_help_text('subdivision'))

    iso_3166_2              = models.CharField(max_length=3, 
                                               help_text=get_help_text('iso_3166_2'))

    is_cipars_region_national  = models.BooleanField(help_text=get_help_text('cipars_region_national'))
    is_cipars_region_atlantic  = models.BooleanField(help_text=get_help_text('cipars_region_atlantic'))
    is_cipars_region_maritimes = models.BooleanField(help_text=get_help_text('cipars_region_maritimes'))
    is_cipars_region_prairies  = models.BooleanField(help_text=get_help_text('cipars_region_prairies'))
    
    def __str__(self):
        return '%s (%s)' % (self.subdivision, self.subdivision_type)



class logic_dictionary(models.Model): # ===============================================================================
    #                                   -------------------------------------------------------------- LOGIC_DICTIONARY
    # =================================================================================================================
    
    """
    A controlled vocabulary of logic states. 
    """

    logic_state                                             = models.CharField(
        unique     = True, 
        max_length = 50, 
        help_text  = get_help_text('logic_state'))

    logic_state_desc                                        = models.TextField(
        help_text  = get_help_text('logic_state_desc'))

    logic_state_accurl                                      =  models.URLField(
        help_text  = get_help_text('logic_state_accurl'))

    hist_ref_logic_state                                    = models.CharField(
        max_length = 100,
        help_text  = get_help_text('hist_ref_logic_state'))

    def __str__(self):
        return self.logic_state



class microbe_01(models.Model): # =====================================================================================
    #                             -------------------------------------------------------------------------- MICROBE_01
    # =================================================================================================================
    
    """
    Microbes, differentiated at the first level (01) of typing (generally, genus).
    """

    microbe_01_name  =  models.CharField(unique     = True, 
                                         max_length = 50, 
                                         help_text  = get_help_text('microbe_01_name'))
    
    def __str__(self):
        return self.microbe_01_name



class microbe_02(models.Model): # =====================================================================================
    #                             -------------------------------------------------------------------------- MICROBE_02
    # =================================================================================================================
    
    """
    Microbes, differentiated at the second level (02) of typing (generally: species, subtype, serovar).
    """
    
    microbe_02_name  =  models.CharField(max_length = 100, 
                                         help_text  = get_help_text('microbe_02_name'))
    
    microbe_level_01 = models.ForeignKey(to         = microbe_01, 
                                         null       = True, 
                                         blank      = True, 
                                         on_delete  = models.SET_NULL, 
                                         help_text  = get_help_text('microbe_level_01'))
    
    # Historical --------------------------------
    HIST_cedar_esr_microbe_02 = models.PositiveIntegerField(null      = True, 
                                                            blank     = True, 
                                                            unique    = True, 
                                                            help_text = get_help_text('HIST_cedar_esr_microbe_02'))
    
    def __str__(self):
        return self.microbe_02_name
    


class moa_type(models.Model): # =======================================================================================
    #                           ------------------------------------------------------------------------------ MOA_TYPE
    # =================================================================================================================

    """
    Measures of association. Refered to as "grain" elsewhere in CEDAR.
    """

    moa_type_name        = models.CharField(unique     = True, 
                                            max_length = 50, 
                                            help_text  = get_help_text('moa_type_name'))
    
    def __str__(self):
        return self.moa_type_name



class moa_unit(models.Model): # =======================================================================================
    #                           ------------------------------------------------------------------------------ MOA_UNIT
    # =================================================================================================================

    """
    Units of analyses (e.g., isolate, sample, animal, person, flock, herd, farm).
    """

    outcome_unit_name     = models.CharField(unique     = True, 
                                            max_length = 50, 
                                            help_text  = get_help_text('outcome_unit_name'))

    def __str__(self):
        return self.outcome_unit_name



class model(models.Model): # ==========================================================================================
#                                  ------------------------------------------------------------------------------ MODEL
# =====================================================================================================================

    """
    An iAM.AMR model for which a query may be generated.
    """
    model_name = models.CharField(max_length=20, unique=True, help_text=get_help_text('model_name'))
    model_description = models.CharField(max_length=100, blank=True, null=True, help_text=get_help_text('model_description'))
    fk_model_create_user_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, blank=True, null=True, related_name='users_c', help_text=get_help_text('fk_model_create_user_id'))
    model_create_date = models.DateField(blank=True, null=True, help_text=get_help_text('model_create_date'))
    fk_model_maintain_user_id = models.ManyToManyField(legacy_user, db_table='model_user_join', help_text=get_help_text('fk_model_maintain_user_id')) # TO DO: create a join table for this (instead of many to many)
    model_maintain_date = models.DateField(blank=True, null=True, help_text=get_help_text('model_maintain_date'))
    
    def __str__(self):
        return self.model_name



class production_stage(models.Model): # ===============================================================================
    #                                   -------------------------------------------------------------- PRODUCTION_STAGE
    # =================================================================================================================

    """
    Production stages along the farm-to-fork continuum.
    """

    production_stage_name = models.CharField(unique     = True, 
                                             max_length = 20, 
                                             help_text  = get_help_text('production_stage_name'))

    # Historical --------------------------------
    HIST_cedar_esr_production_stage = models.PositiveIntegerField(null      = True, 
                                                                  blank     = True, 
                                                                  unique    = True, 
                                                                  help_text = get_help_text('HIST_cedar_esr_production_stage'))
    
    def __str__(self):
        return self.production_stage_name



class production_stream(models.Model): # ==============================================================================
    #                                    ------------------------------------------------------------ PRODUCTION_STREAM
    # =================================================================================================================

    """
    The host animal production stream (e.g., "Beef Cattle", "Dairy Cattle").                               
    """

    production_stream_name =  models.CharField(max_length = 100)
    host_level_01          = models.ForeignKey(to         = host_01, 
                                               on_delete  = models.CASCADE)
    # Cascade delete; a production stream does not exist without a host.

    def __str__(self):
        return self.production_stream_name



class publisher(models.Model): # ======================================================================================
    #                            ---------------------------------------------------------------------------- PUBLISHER
    # =================================================================================================================

    """
    Scientific publications.
    """

    pub_type  =    models.CharField(null       = True, 
                                    blank      = True, 
                                    max_length = 50, 
                                    help_text  = get_help_text('pub_type'))
                                    
    pub_title =    models.TextField(help_text  = get_help_text('pub_title'))

    pub_rank  = models.IntegerField(null       = True, 
                                    blank      = True, 
                                    help_text  = get_help_text('pub_rank'))

    pub_issn  =    models.TextField(null       = True, 
                                    blank      = True, 
                                    help_text  = get_help_text('pub_issn'))
    
    def __str__(self):
        return self.pub_title



class study_design(models.Model): # ===================================================================================
    #                               ---------------------------------------------------------------------- STUDY_DESIGN
    # =================================================================================================================

    """
    Types of study design.
    """

    study_design_name = models.CharField(unique     = True, 
                                         max_length = 50, 
                                         help_text  = get_help_text('study_design_name'))
    
    def __str__(self):
        return self.study_design_name



class source_project(models.Model): # =================================================================================
#                                  --------------------------------------------------------------------- SOURCE_PROJECT
# =====================================================================================================================
    """
    A source project, which has submitted data to CEDAR.
    """

    source_project_name       = models.CharField( max_length=100)
    source_project_user_owner = models.ForeignKey(to=legacy_user,
                                                  related_name='project_user_owner',
                                                  on_delete=models.SET_NULL, 
                                                  blank=True,
                                                  null=True)

    source_project_user_entry = models.ForeignKey(to=legacy_user,
                                                  related_name='project_user_entry',
                                                  on_delete=models.SET_NULL, 
                                                  blank=True,
                                                  null=True)
    source_project_entry_date = models.DateField()

    project_references        = models.ManyToManyField(to='reference',
                                                       db_table='source_project_join_reference',
                                                       related_name='project_references')

    project_factors           = models.ManyToManyField(to='factor', 
                                                       db_table='source_project_join_factor',
                                                       related_name='project_factors')

    project_res_outcomes      = models.ManyToManyField(to='res_outcome',
                                                       db_table='source_project_join_res_outcome',
                                                       related_name='project_res_outcomes')



class factor_family(models.Model):
    """
    A factor family
    """
    
    factor_family_name = models.CharField(max_length=500, blank=True, null=True, help_text=get_help_text('factor_family_name'))
    
    def __str__(self):
        return self.factor_family_name



class factor_family_join_parent_factor(models.Model):
    fk_family_join_parent_factor_parent_id = models.ForeignKey('factor_parent', on_delete=models.CASCADE, blank=True, null=True, help_text=get_help_text('fk_family_join_parent_factor_parent_id'))
    fk_family_join_parent_factor_family_id = models.ForeignKey('factor_family', on_delete=models.CASCADE, blank=True, null=True, help_text=get_help_text('fk_family_join_parent_factor_family_id'))



class factor_parent(models.Model):
    """
    A parent factor
    """
    
    factor_parent_name = models.CharField(max_length=500, blank=True, null=True, help_text=get_help_text('factor_parent_name'))
    
    def __str__(self):
        return self.factor_parent_name



class factor_parent_join_atc_vet(models.Model): # formerly m_factor_amu
    """
    AMU at the parent factor level
    """
    
    fk_amu_factor_parent_id = models.ForeignKey('factor_parent', on_delete=models.CASCADE, blank=True, null=True, help_text=get_help_text('fk_amu_factor_parent_id'))
    fk_amu_atc_vet_id = models.ForeignKey(atc_vet, on_delete=models.SET_NULL, blank=True, null=True, help_text=get_help_text('fk_amu_atc_vet_id'))
    


class factor_parent_join_factor(models.Model):
    fk_parent_join_factor_factor_parent_id = models.ForeignKey('factor_parent', on_delete=models.CASCADE, blank=True, null=True, help_text=get_help_text('fk_parent_join_factor_factor_parent_id'))
    fk_parent_join_factor_factor_id = models.ForeignKey(factor, on_delete=models.CASCADE, blank=True, null=True, help_text=get_help_text('fk_parent_join_factor_factor_id'))



class factor_parent_metadata(models.Model):
    """
    An entry of metadata pertaining to the applicability or frequency of a parent factor
    """
    
    fk_metadata_factor_parent_id     = models.ForeignKey(factor_parent, on_delete=models.SET_NULL, blank=True, null=True, help_text=get_help_text('fk_metadata_factor_parent_id'))
    fk_metadata_location_02_id = models.ForeignKey(location_02, on_delete=models.SET_NULL, blank=True, null=True, help_text=get_help_text('fk_metadata_location_02_id'))
    fk_entry_user_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, related_name='user_entry', blank=True, null=True, help_text=get_help_text('fk_entry_user_id'))
    fk_review_user_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, related_name='user_review', blank=True, null=True, help_text=get_help_text('fk_review_user_id'))
    frequency = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text=get_help_text('frequency'))
    frequency_distribution = models.CharField(max_length=200, blank=True, null=True, help_text=get_help_text('frequency_distribution'))
    frequency_param_a = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text=get_help_text('frequency_param_a'))
    frequency_param_b = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text=get_help_text('frequency_param_b'))
    frequency_param_c = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text=get_help_text('frequency_param_c'))
    frequency_data_apply_start_year = models.IntegerField(blank=True, null=True, help_text=get_help_text('frequency_data_apply_start_year'))
    frequency_data_apply_end_year = models.IntegerField(blank=True, null=True, help_text=get_help_text('frequency_data_apply_end_year'))
    frequency_data_source = models.CharField(max_length=500, blank=True, null=True, help_text=get_help_text('frequency_data_source'))

    frequency_data_source_added_year                     = models.IntegerField(
        null       = True, 
        blank      = True, 
        help_text  = get_help_text('frequency_data_source_added_year'))

    fk_frequency_evidence_type_quality_id                  = models.ForeignKey(      
        to           = evidence_type_quality, 
        null         = True, 
        blank        = True, 
        on_delete    = models.SET_NULL, 
        help_text    = get_help_text('fk_frequency_evidence_type_quality_id'), 
        related_name = 'evidence_quality_frequency')


    note = models.TextField(blank=True, null=True, help_text=get_help_text('note'))
    is_applicable_past = models.BooleanField(blank=True, null=True, help_text=get_help_text('is_applicable_past'))
    is_applicable_present = models.BooleanField(blank=True, null=True, help_text=get_help_text('is_applicable_present'))
    is_applicable_future = models.BooleanField(blank=True, null=True, help_text=get_help_text('is_applicable_future'))
    applicable_data_source = models.CharField(max_length=200, blank=True, null=True, help_text=get_help_text('applicable_data_source'))
    applicable_data_source_added_year = models.IntegerField(blank=True, null=True, help_text=get_help_text('applicable_data_source_added_year'))
    fk_applicable_evidence_type_quality_id = models.ForeignKey(evidence_type_quality, on_delete=models.SET_NULL, blank=True, null=True, related_name='evidence_quality_applicability', help_text=get_help_text('fk_applicable_evidence_type_quality_id'))
    
    def __str__(self):
        return 'Metadata entry for parent factor %s (entered by %s)' % (self.fk_metadata_factor_parent_id, self.fk_entry_user_id)



class factor_join_res_outcome(models.Model):
    
    # TO DO: see if I can add ufid and urid here for context(?)
    fk_factor_join_res_outcome_factor_id = models.ForeignKey(factor, on_delete=models.CASCADE, blank=True, null=True, help_text=get_help_text('fk_factor_join_res_outcome_factor_id'))
    fk_res_outcome_id = models.ForeignKey(res_outcome, on_delete=models.CASCADE, blank=True, null=True, help_text=get_help_text('fk_res_outcome_id'))

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



class reference_history_action(models.Model): # TO DO: reference_history
    action = models.CharField(max_length=200, help_text='')
    action_level_coarse = models.CharField(max_length=200, blank=True, null=True, help_text='')
    action_level_coarse_num = models.IntegerField(blank=True, null=True, help_text='')
    action_description = models.TextField(blank=True, null=True, help_text='')
    action_level_fine = models.CharField(max_length=100, blank=True, null=True, help_text=get_help_text('action_level_fine'))
    
    def __str__(self):
        return self.action



class reference_join_reference_history(models.Model): # formerly m_reference_history in Microsoft Access
    reference_join_history_reference_id = models.IntegerField(blank=True, null=True, help_text=get_help_text('reference_join_history_reference_id'))
    fk_reference_history_action_id = models.ForeignKey(reference_history_action, on_delete=models.SET_NULL, blank=True, null=True, help_text='')
    fk_user_r_join_rh_id = models.ForeignKey(legacy_user, on_delete=models.SET_NULL, blank=True, null=True, help_text='')
    action_date = models.DateTimeField(blank=True, null=True, help_text='') #TO DO: timestamp i.e. yyyy-mm-dd 0:00
    is_cedar_esr = models.BooleanField(default=False, help_text='')



class reference_join_location(models.Model): # ====================================================
    #                                          ---------------------------- reference_join_location
    # =============================================================================================
    """
    The location(s) of reference creation.
    """

    #  ManyToManyField.through¶
    
    reference_id         = models.ForeignKey(to=reference,
                                             db_column='reference_id', 
                                             on_delete=models.CASCADE, 
                                             blank=True, 
                                             null=True, 
                                             help_text=get_help_text('fk_reference_join_location_reference_id'))
    
    location_main_id     = models.ForeignKey(to=location_01, 
                                             db_column='location_main_id', 
                                             on_delete=models.SET_NULL, 
                                             blank=True, 
                                             null=True, 
                                             help_text=get_help_text('fk_location_01_id'))

    location_sub_id      = models.ForeignKey(to=location_sub, 
                                             db_column='location_sub_id', 
                                             on_delete=models.SET_NULL, 
                                             blank=True, 
                                             null=True, 
                                             help_text=get_help_text('fk_reference_join_location_location_02_id'))

    hist_join_id         = models.IntegerField(blank=True, null=True)
    

    location_detail      = models.TextField(blank=True, null=True, help_text=get_help_text('ref_loc_note'))
    
    location_alpha3_dep  = models.TextField(blank=True, null=True)


    #def __str__(self):
        #return '%s:%s (%s)' % (self.location_01, self.location_02, self.reference)



class reference_note(models.Model): #former matrix table m_reference_note
    """
    A note written for a particular reference.
    """
    reference                                              = models.ForeignKey(
        to         = reference, 
        null       = True,
        blank      = True,
        on_delete  = models.CASCADE,   
        help_text  = get_help_text('reference'))

    reference_note                                          = models.TextField(
        null       = True, 
        blank      = True, 
        help_text  = get_help_text('reference_note'))

    user                                                   = models.ForeignKey(
        to         = legacy_user,                                                # To Update
        null       = True,
        blank      = True,  
        on_delete  = models.SET_NULL, 
        help_text  = get_help_text('user'))

    is_resolved                                          = models.BooleanField(
        default    = False, 
        help_text  = get_help_text('is_resolved'))
    
    def __str__(self):
        return self.reference_note



#class status_reference(models.Model):
    #"""
    #A reference's status with respect to data extraction.
    #"""
    #status = models.CharField(max_length=50, unique=True, help_text='The stage of data extraction, i.e. "Validation (Phase 1)"')
    #status_description = models.TextField(help_text='A description of the status')
    
    #def __str__(self):
        #return self.status




class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        # abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
