"""A collection of functions related to querying CEDAR_forest.

"""


import csv


"""----- write_timber_csv ------------------------------------------------ """

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
    ] 

tmbr_default_col_names = [
    # See write_timber_csv() for description.
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
    'study_design'
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
    'meta_analysis_group',
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