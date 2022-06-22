
# Generate Timber

import csv, datetime

from django.db.models import F
from cedar_core.make_query_fun import write_timber_csv

from cedar_core.models import reference, reference_join_location, reference_join_reference_note, factor, publisher, res_outcome


# Define the QuerySet (the collection of objects to retrieve). The QuerySet
# uses .all() (can later be replaced with a filter), and .values() to select
# the attributes. Note the syntax for FKs: fk_col__attribute or fk_col__next_fk_col__attribute

# Using values "Returns a QuerySet that returns dictionaries, rather than model instances, when used as an iterable."




# Generate timber for all resistance outcomes. At present, multiple records are returned per resistance outcome because 

timber_qs_all = res_outcome.objects.all().values(

    'id',
    'fk_factor_id__fk_factor_reference_id__refwk',
    'fk_factor_id__fk_factor_reference_id__publish_doi',
    'fk_factor_id__fk_factor_reference_id__publish_pmid',
    'fk_factor_id__fk_factor_reference_id__key_bibtex',
    'fk_factor_id__fk_factor_reference_id__ref_title',
    'fk_factor_id__fk_factor_reference_id__reference_join_location__location_main_id__country',   # Will result in return of multiple records per resistance outcome.
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






# Check a Record
timber_qs_all.all().get(pk=10002)

# https://docs.djangoproject.com/en/4.0/topics/db/queries/#the-pk-lookup-shortcut

# https://docs.djangoproject.com/en/dev/ref/models/querysets/#distinct

# https://docs.djangoproject.com/en/4.0/topics/db/aggregation/

# https://docs.djangoproject.com/en/4.0/topics/db/models/#extra-fields-on-many-to-many-relationships

# https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.ForeignKey




# Filter ----------

# Remove outcomes from references excluded from CEDAR.

timber_qs = timber_qs_all.filter(fk_factor_id__fk_factor_reference_id__exclude_extraction = False,
                                 fk_factor_id__fk_factor_reference_id__archived = False)



timber_qs_order = timber_qs.order_by('id', 'fk_factor_id__fk_factor_reference_id__reference_join_location__id')





timber_qs.distinct('fk_factor_id__fk_factor_reference_id__reference_join_location__reference_id').count()



timber_qs.all().get(id=10033).count()


# Check that the filter operation reduced the count of objects.

timber_qs_all.count()
timber_qs.count()


t2 = timber_qs_all.distinct('id')
t2.count()


now = datetime.datetime.now()

appendnow = now.strftime("%Y_%m_%d_%H_%M")




""" ----- Write all resistance outcomes. ----- """

write_timber_csv(timber_qs, "timber_all_%s.csv" % (appendnow))

write_timber_csv(timber_qs_order, "timber_order_all_%s.csv" % (appendnow))


""" ----- Write Timber == lridge ----------------------------------------- """
# Host: Chicken
# Microbe: Any
# Resistance: Any
# Project: //unknown//

timber_lridge = timber_qs.filter(fk_factor_id__fk_factor_host_01_id__host_name = "Chicken")

timber_lridge.count()

write_timber_csv(timber_lridge, "timber_lridge_%s.csv" % (appendnow))






""" ----- Write Timber == bchapman --------------------------------------- """
# Host: Chicken
# Microbe: Salmonella
# Resistance: Third-Generation Cephalosporins
# Project: CH-SAL-3GC

timber_CH_SAL_3GC = timber_qs.filter(fk_factor_id__fk_factor_host_01_id__host_name = "Chicken",
                                     fk_microbe_01_id__microbe_name = "Salmonella",
                                     fk_resistance_atc_vet_id__levelname_4 = "Third-generation cephalosporins")

timber_CH_SAL_3GC.count()

write_timber_csv(timber_CH_SAL_3GC, "timber_CH_SAL_3GC_%s.csv" % (appendnow))






