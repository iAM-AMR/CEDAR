

# python .\cedar_root\manage.py make_timber

import csv, datetime

from django.db.models import F
from cedar_core.make_query_fun import write_timber_csv

from cedar_core.models import reference, reference_join_location, reference_join_reference_note, factor, publisher, res_outcome


from django.core.management.base import BaseCommand, CommandError



tmbr_default_field_names = [
    # See write_timber_csv() for description. 
    'id',
    'pid',
    'factor__reference__id',
    'factor__reference__pid_reference',
    'factor__reference__refwk',
    'factor__reference__publish_doi',
    'factor__reference__publish_pmid',
    'factor__reference__key_bibtex',
    'factor__reference__ref_title',
    'factor__reference__ref_country__country',
    'factor__reference__study_design__design',
    'factor__id',
    'factor__pid_factor',
    'factor__factor_title',
    'factor__factor_description',
    'factor__group_factor',
    'factor__group_comparator',
    'factor__host_level_01__host_name',
    'factor__host_level_02__host_subtype_name',
    'factor__host_production_stream',
    'factor__host_life_stage',
    'factor__group_allocate_production_stage__stage',
    'group_observe_production_stage__stage',
    'moa_type__res_format',
    'moa_unit__res_unit',
    'resistance__levelname_4_coarse',
    'resistance__levelname_5',
    'resistance_gene__element_name',
    'microbe_level_01__microbe_name',
    'microbe_level_02__microbe_subtype_name',
    'is_figure_extract',
    'figure_extract_method__method_name',
    'figure_extract_reproducible',
    'contable_a',
    'contable_b',
    'contable_c', 
    'contable_d',
    'prevtable_a',
    'prevtable_b',
    'prevtable_c',
    'prevtable_d',
    'table_n_exp',
    'table_n_ref',
    'odds_ratio',
    'odds_ratio_lo',
    'odds_ratio_up',
    'odds_ratio_sig',
    'odds_ratio_confidence',
    ] 

tmbr_default_col_names = [
    # See write_timber_csv() for description.
    # Note, missing comma will silently fail.
    'id_res_out',
    'pid_res_out',
    'id_reference',
    'pid_reference',
    'ref_rwid',
    'ref_doi',
    'ref_pmid',
    'ref_bibtex_key',
    'ref_title',
    'country',
    'study_design',
    'id_factor',
    'pid_factor',
    'factor_title',
    'factor_description',
    'factor_group',
    'comparator_group',
    'host_level_01',
    'host_level_02',
    'host_production_stream',
    'host_life_stage',
    'stage_allocate',
    'stage_observe',
    'moa_type',
    'moa_unit',
    'resistance_class',
    'resistance',
    'resistance_gene',
    'microbe_level_01',
    'microbe_level_02',
    'is_figure_extract',
    'figure_extract_method',
    'figure_extract_reproducible',
    'contable_a',
    'contable_b',
    'contable_c', 
    'contable_d',
    'prevtable_a',
    'prevtable_b',
    'prevtable_c',
    'prevtable_d',
    'table_n_exp',
    'table_n_ref',
    'odds_ratio',
    'odds_ratio_lo',
    'odds_ratio_up',
    'odds_ratio_sig',
    'odds_ratio_confidence',
    ] 

def write_timber_csv(tmbr_qs, write_path, tmbr_field_names = tmbr_default_field_names, tmbr_col_names = tmbr_default_col_names):

    """Writes a timber queryset (as a dictionary) to a .CSV

    Writes a timber QuerySet of dictionaries (created using .values()) to a .CSV.

    Args:
        tmbr_qs: A timber QuerySet of dictionaries.
        write_path: (string) the path to save the .CSV.
        tmbr_field_names: A list of timber field names (as strings), in desired order, to write to the CSV.
                          These names must match the QuerySet, but inclusion/exclusion and position control
                          the final CSV.  
        tmbr_col_names  : A list of column names (as strings), with order matching field_names, to write to the CSV. 
                          These positions must match tmbr_field_names,
    
    """

    fobj = open(file=write_path,           # PATH
                mode='w',                  # Write mode
                encoding='UTF8',           # UTF8 encoding to match database
                newline='')                # Replace default carriage return

    # Setup the .CSV header writer, then write.
    # Use csv.writer because the column names are a list.
    head_writer = csv.writer(fobj)
    head_writer.writerow(tmbr_col_names)

    # Setup the .CSV body writer, then write.
    # Use csv.DictWriter because evaluating the QuerySet gives us dictionaries.
    writer = csv.DictWriter(f=fobj,                     
                        fieldnames=tmbr_field_names,  # Field names (matching QuerySet)
                        extrasaction='ignore')        # Ignore non-selected fields (through omission in tmbr_field_names) in tmbr_qs. 

        # Loop, writing each line of the QuerySet to the .CSV.
    for eachline in tmbr_qs:
        writer.writerow(eachline)

    # Close the connection.
    fobj.close()














# Generate Timber


# Define the QuerySet (the collection of objects to retrieve). The QuerySet
# uses .all() (can later be replaced with a filter), and .values() to select
# the attributes. Note the syntax for FKs: fk_col__attribute or fk_col__next_fk_col__attribute

# Using values "Returns a QuerySet that returns dictionaries, rather than model instances, when used as an iterable."



# https://docs.djangoproject.com/en/4.0/topics/db/queries/#the-pk-lookup-shortcut

# https://docs.djangoproject.com/en/dev/ref/models/querysets/#distinct

# https://docs.djangoproject.com/en/4.0/topics/db/aggregation/

# https://docs.djangoproject.com/en/4.0/topics/db/models/#extra-fields-on-many-to-many-relationships

# https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ForeignKey





# Generate All Timber ---------------------------------------------------------
# =============================================================================

# Generate timber for all resistance outcomes.
# This returns multiple records per resistance outcome due to join w. multiple locations.

timber_qs_all = res_outcome.objects.all().values(
    'id',
    'pid_ro',
    'factor__reference__id',
    'factor__reference__pid_reference',
    'factor__reference__refwk',
    'factor__reference__publish_doi',
    'factor__reference__publish_pmid',
    'factor__reference__key_bibtex',
    'factor__reference__ref_title',
    'factor__reference__ref_country__country',
    'factor__reference__study_design__design',
    'factor__id',
    'factor__pid_factor',
    'factor__factor_title',
    'factor__factor_description',
    'factor__group_factor',
    'factor__group_comparator',
    'factor__host_level_01__host_name',
    'factor__host_level_02__host_subtype_name',
    'factor__host_production_stream',
    'factor__host_life_stage',
    'factor__group_allocate_production_stage__stage',
    'group_observe_production_stage__stage',
    'moa_type__res_format',
    'moa_unit__res_unit',
    'resistance__levelname_4_coarse',
    'resistance__levelname_5',
    'resistance_gene__element_name',
    'microbe_level_01__microbe_name',
    'microbe_level_02__microbe_subtype_name',
    'is_figure_extract',
    'figure_extract_method__method_name',
    'figure_extract_reproducible',
    'contable_a',
    'contable_b',
    'contable_c', 
    'contable_d',
    'prevtable_a',
    'prevtable_b',
    'prevtable_c',
    'prevtable_d',
    'table_n_exp',
    'table_n_ref',
    'odds_ratio',
    'odds_ratio_lo',
    'odds_ratio_up',
    'odds_ratio_sig',
    'odds_ratio_confidence',
    )

# You can check that the QuerySet returns the expected values.

timber_qs_all.all().get(pk=10002)



# Filter and Deduplicate Timber Returns ---------------------------------------
# =============================================================================

# Remove resistance outcomes belonging to references that are archived, or 
# excluded from extraction in CEDAR.

timber_qs = timber_qs_all.filter(factor__reference__is_excluded_extract = False,
                                 factor__reference__is_archived         = False)

# Check that the number of records i reduced by filter().

timber_qs_all.count()
timber_qs.count()



# Write Timber ----------------------------------------------------------------
# =============================================================================

# Set Time and Date
now       = datetime.datetime.now()
appendnow = now.strftime("%Y_%m_%d_%H_%M")



# Write Complete QuerySet -------------
# =====================================

# Project: iAM.AMR.SEARCH
# Archived: NO
# Excluded: NO
# Host: Any
# Microbe: Any
# Resistance: Any

write_timber_csv(timber_qs, "timber_all_%s.csv" % (appendnow))



""" ----- Write Timber == lridge ----------------------------------------- """
# Host: Chicken
# Microbe: Any
# Resistance: Any
# Project: //unknown//

timber_lridge = timber_qs.filter(factor__host_level_01__host_name = "Chicken")

write_timber_csv(timber_lridge, "timber_lridge_%s_raw.csv" % (appendnow))






""" ----- Write Timber == bchapman --------------------------------------- """
# Host: Chicken
# Microbe: Salmonella
# Resistance: Third-Generation Cephalosporins
# Project: CH-SAL-3GC

timber_CH_SAL_3GC = timber_qs.filter(factor__host_level_01__host_name = "Chicken",
                                     microbe_level_01__microbe_name = "Salmonella",
                                     resistance__levelname_4 = "Third-generation cephalosporins")

timber_CH_SAL_3GC.count()

write_timber_csv(timber_CH_SAL_3GC, "timber_3GC_SAL_CH_%s_raw.csv" % (appendnow))


# https://docs.djangoproject.com/en/4.0/howto/custom-management-commands/

class Command(BaseCommand):

    def handle(self, *args, **options):

        write_timber_csv(timber_CH_SAL_3GC, "timber_3GC_SAL_CH_%s_raw.csv" % (appendnow))


        self.stdout.write(self.style.SUCCESS('WROTE TIMBER'))