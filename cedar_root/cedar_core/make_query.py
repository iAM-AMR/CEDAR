
# Generate Timber

import csv
from cedar_core.models import reference, reference_join_location, reference_join_reference_note, factor, publisher, res_outcome


# This example generates a Timber with all resistance outcomes in the database, 
# and writes them to a .CSV.

# Define the QuerySet (the collection of objects to retrieve). The QuerySet
# uses .all() (can later be replaced with a filter), and .values() to select
# the attributes. Note the syntax for FKs: fk_col__attribute or fk_col__next_fk_col__attribute

# Using values "Returns a QuerySet that returns dictionaries, rather than model instances, when used as an iterable."
timberQS = res_outcome.objects.all().values(

    'fk_factor_id__fk_factor_reference_id__refwk',
    'fk_factor_id__fk_factor_reference_id__publish_doi',
    'fk_factor_id__fk_factor_reference_id__publish_pmid',
    'fk_factor_id__fk_factor_reference_id__key_bibtex',
    'fk_factor_id__fk_factor_reference_id__ref_title',
    'fk_factor_id__id',
    'fk_factor_id__factor_title',
    'fk_factor_id__factor_description',
    'fk_factor_id__group_exposed',
    'fk_factor_id__group_referent',
    'fk_factor_id__fk_factor_host_01_id__host_name',
    'fk_factor_id__fk_host_02_id__host_subtype_name',
    'fk_factor_id__fk_group_allocate_production_stage_id__stage',
    'fk_group_observe_production_stage_id__stage',
    'fk_moa_type_id__res_format',
    'fk_moa_unit_id__res_unit',
    'fk_resistance_atc_vet_id__levelname_5',
    'fk_microbe_01_id__microbe_name',
    'fk_res_outcome_microbe_02_id__microbe_subtype_name',
    'fk_figure_extract_method_id__method_name',
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

# Now, we must define a key, using the same column names.
timberQS_names = [
    'fk_factor_id__fk_factor_reference_id__refwk',
    'fk_factor_id__fk_factor_reference_id__publish_doi',
    'fk_factor_id__fk_factor_reference_id__publish_pmid',
    'fk_factor_id__fk_factor_reference_id__key_bibtex',
    'fk_factor_id__fk_factor_reference_id__ref_title',
    'fk_factor_id__id',
    'fk_factor_id__factor_title',
    'fk_factor_id__factor_description',
    'fk_factor_id__group_exposed',
    'fk_factor_id__group_referent',
    'fk_factor_id__fk_factor_host_01_id__host_name',
    'fk_factor_id__fk_host_02_id__host_subtype_name',
    'fk_factor_id__fk_group_allocate_production_stage_id__stage',
    'fk_group_observe_production_stage_id__stage',
    'fk_moa_type_id__res_format',
    'fk_moa_unit_id__res_unit',
    'fk_resistance_atc_vet_id__levelname_5',
    'fk_microbe_01_id__microbe_name',
    'fk_res_outcome_microbe_02_id__microbe_subtype_name',
    'fk_figure_extract_method_id__method_name',
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

# Now define Column Names
timberQS_col_names = [
    'REFWK',
    'ref_doi',
    'ref_pmid',
    'ref_bibtex_key',
    'ref_title',
    'factor_id',
    'factor_title',
    'fk_factor_id__factor_description',
    'fk_factor_id__group_exposed',
    'fk_factor_id__group_referent',
    'fk_factor_id__fk_factor_host_01_id__host_name',
    'fk_factor_id__fk_host_02_id__host_subtype_name',
    'fk_factor_id__fk_group_allocate_production_stage_id__stage',
    'fk_group_observe_production_stage_id__stage',
    'fk_moa_type_id__res_format',
    'fk_moa_unit_id__res_unit',
    'fk_resistance_atc_vet_id__levelname_5',
    'fk_microbe_01_id__microbe_name',
    'fk_res_outcome_microbe_02_id__microbe_subtype_name',
    'fk_figure_extract_method_id__method_name',
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
    'odds_ratio_confidence'
    ] 

# Check a Record
timberQS.all().get(pk=10002)

# Write CSV --------------------

# Open the Connection
fobj = open(file='path_to_csv.csv',    # PATH
            mode='w',                  # Write mode
            encoding='UTF8',           # UTF8 encoding to match database
            newline='')                # Replace default carriage return

# Setup the .CSV header writer.
# Use csv.writer because the column names are a list.
head_writer = csv.writer(csvfile=fobj)

# Setup the .CSV body writer.
# Use csv.DictWriter because evaluating the QuerySet gives us dictionaries.
writer = csv.DictWriter(f=fobj,                     
                        fieldnames=timberQS_names,  # Field names (matching QuerySet)
                        extrasaction='ignore')      # Ignore errors where cols exist and are not used (will depreciate use).

# Write the header.
head_writer.writerow(timberQS_col_names)

# Loop, writing each line of the QuerySet to the .CSV.
for eachline in timberQS:
    writer.writerow(eachline)

# Close the connection.
fobj.close()



# Now, we explore filters.

from django.db.models import F
