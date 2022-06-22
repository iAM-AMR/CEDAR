
# Generate Timber

import csv, datetime

from django.db.models import F
from cedar_core.make_query_fun import write_timber_csv

from cedar_core.models import reference, reference_join_location, reference_join_reference_note, factor, publisher, res_outcome


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
    'factor__reference__reference_join_location__location_main_id__country',   # Will result in return of multiple records per resistance outcome.
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

# Order the QuerySet by the ID and the ID of the reference_join_location. This 
# should ensure the first location entry (by order of entry) is selected, as the ID
# is an ascending integer -- a proxy for order (or date-time order).

timber_qs = timber_qs.order_by('factor__id', 
                               'id', 
                               'factor__reference__reference_join_location__id')

# Select only one record for each resistance outcome.
# At present, the join with location results in duplicates.
# Note, if more fields are added to the Timber, care should be taken to ensure 
# deduplication considers these fields.

timber_qs_distinct = timber_qs.distinct('factor__id','id')

# Check that the number of records is reduced by distinct().

timber_qs.count()
timber_qs_distinct.count()



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

write_timber_csv(timber_qs_distinct, "timber_all_%s.csv" % (appendnow))



""" ----- Write Timber == lridge ----------------------------------------- """
# Host: Chicken
# Microbe: Any
# Resistance: Any
# Project: //unknown//

timber_lridge = timber_qs_distinct.filter(factor__host_level_01__host_name = "Chicken")

write_timber_csv(timber_lridge, "timber_lridge_%s.csv" % (appendnow))






""" ----- Write Timber == bchapman --------------------------------------- """
# Host: Chicken
# Microbe: Salmonella
# Resistance: Third-Generation Cephalosporins
# Project: CH-SAL-3GC

timber_CH_SAL_3GC = timber_qs_distinct.filter(factor__fk_factor_host_01_id__host_name = "Chicken",
                                     fk_microbe_01_id__microbe_name = "Salmonella",
                                     fk_resistance_atc_vet_id__levelname_4 = "Third-generation cephalosporins")

timber_CH_SAL_3GC.count()

write_timber_csv(timber_CH_SAL_3GC, "timber_CH_SAL_3GC_%s.csv" % (appendnow))






