"""A collection of functions related to querying CEDAR_forest.

"""


import csv


"""----- write_timber_csv ------------------------------------------------ """

tmbr_default_field_names = [
    # See write_timber_csv() for description. 
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

tmbr_default_col_names = [
    # See write_timber_csv() for description. 
    'REFWK',
    'ref_doi',
    'ref_pmid',
    'ref_bibtex_key',
    'ref_title',
    'factor_id',
    'factor_title',
    'factor_description',
    'factor_group_factor',
    'factor_group_comparator',
    'factor_host_main',
    'factor_host_sub',
    'factor_stage_allocate',
    'res_outcome_stage_observe',
    'res_outcome_moa_type',
    'res_outcome_moa_unit',
    'resistance',
    'microbe_main',
    'microbe_sub',
    'figure_extraction_method',
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
    'extra_col',
    ] 

def write_timber_csv(tmbr_qs, write_path, tmbr_field_names = tmbr_default_field_names, tmbr_col_names = tmbr_default_col_names):

    """Writes a timber queryset (as a dictionary) to a .CSV

    Writes a timber QuerySet of dictionaries (created using .values()) to a .CSV.

    Args:
        tmbr_qs: A timber QuerySet of dictionaries.
        write_path: (string) the path to save the .CSV.
        tmbr_field_names: A list of timber field names (as strings), in desired order, to write to the CSV.
                          These names must match the QuerySet.  
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