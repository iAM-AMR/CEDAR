

import csv
import numpy as np
from cedar_core.forms import (QuerySelectForm, TopicTabForm)
from cedar_core.models import (factor, publisher, reference,
                               reference_join_location, res_outcome)
from dal import autocomplete
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import F, Q
from django.forms.models import model_to_dict
from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render

from cedar_core.filters import timber_filter



# Add either a new reference note, reference location, factor, or res_outcome
@login_required
@permission_required('cedar_core.add_factor')
def add_new_obj(request, obj_id, form_type):
    
    # This function is being depreciated; too much complexity for too little DRY improvement.

    # obj_id would be better as "parent object ID"

    obj = reference.objects.get(pk=obj_id)

    if form_type == 'loc':
        new_obj = reference_join_location(reference_id = obj)
        redir_path = '/cedar_core/references/' + str(obj_id) + '/#loc-md'
    
    elif form_type == 'note':
        new_obj = reference_join_reference_note(fk_reference_join_note_reference_id = obj)
        redir_path = '/cedar_core/references/' + str(obj_id) + '/#notes-md'
    
    else: #form_type = 'fac'
        new_obj = factor(reference = obj)
        redir_path = '/reference/' + str(obj_id) + '/factors'
    
    # Save new object and redirect
    new_obj.save()
    
    return redirect(redir_path)





@login_required
@permission_required('cedar_core.add_factor')

def new_blank_factor(request, reference_id): # ======================================================================================================
    #                                          ------------------------------------------------------------------------------------- NEW_BLANK_FACTOR
    # ===============================================================================================================================================

    """
    This function creates a new blank factor associated with the reference 
    indicated by "reference_id". 
    """

    # Get parent reference
    parent_reference = reference.objects.get(pk=reference_id)

    # Create new blank factor with reference field complete. ID 
    # is assigned by auto-increment. 
    new_factor = factor(reference = parent_reference)

    # Save new factor
    new_factor.save()

    # Return to referer. Where no referer, home.
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




def get_timber(request):

    tmbr_default_field_names = [
    # See write_timber_csv() for description. 
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
    'factor__reference__study_design__study_design_name',
    'factor__id',
    'factor__pid_factor',
    'factor__factor_title',
    'factor__factor_description',
    'factor__group_factor',
    'factor__group_comparator',
    'factor__host_level_01__host_01_name',
    'factor__host_level_02__host_subtype_name',
    'factor__host_production_stream',
    'factor__host_life_stage',
    'factor__group_allocate_production_stage__production_stage_name',
    'group_observe_production_stage__production_stage_name',
    'moa_type__moa_type_name',
    'moa_unit__outcome_unit_name',
    'resistance__levelname_4_coarse',
    'resistance__levelname_5',
    'resistance_gene__genetic_element_name',
    'microbe_level_01__microbe_01_name',
    'microbe_level_02__microbe_02_name',
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
    'table_n_ab',
    'table_n_cd',
    'odds_ratio',
    'odds_ratio_lo',
    'odds_ratio_up',
    'odds_ratio_sig',
    'odds_ratio_confidence',
    ] 

    timber_qs_all = res_outcome.objects.all().values_list(
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
    'factor__reference__study_design__study_design_name',
    'factor__id',
    'factor__pid_factor',
    'factor__factor_title',
    'factor__factor_description',
    'factor__group_factor',
    'factor__group_comparator',
    'factor__host_level_01__host_01_name',
    'factor__host_level_02__host_subtype_name',
    'factor__host_production_stream',
    'factor__host_life_stage',
    'factor__group_allocate_production_stage__production_stage_name',
    'group_observe_production_stage__production_stage_name',
    'moa_type__moa_type_name',
    'moa_unit__outcome_unit_name',
    'resistance__levelname_4_coarse',
    'resistance__levelname_5',
    'resistance_gene__genetic_element_name',
    'microbe_level_01__microbe_01_name',
    'microbe_level_02__microbe_02_name',
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
    'table_n_ab',
    'table_n_cd',
    'odds_ratio',
    'odds_ratio_lo',
    'odds_ratio_up',
    'odds_ratio_sig',
    'odds_ratio_confidence',
    )

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

    filtered_timber = timber_filter(request.GET, queryset=timber_qs_all)

    if request.GET:

        if 'filternow' in request.GET:
            filtered_timber = timber_filter(request.GET, queryset=timber_qs_all)


        elif 'exportnow' in request.GET:
             
            
            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
            )

            writer_head = csv.writer(response)
            writer_head.writerow(tmbr_default_col_names)

            writer = csv.writer(response)        # Ignore non-selected fields (through omission in tmbr_field_names) in tmbr_qs. 

                # Loop, writing each line of the QuerySet to the .CSV.
            for eachline in filtered_timber.qs:
                writer.writerow(eachline)

            return(response)

    context = {'all_timber': timber_qs_all, 'filtered_timber': filtered_timber, 'col_list': tmbr_default_col_names, 'page_title': 'Query Papers Based on Host and Microbe'}
    return render(request, 'cedar_core/get_timber.html', context)












def export_timber_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    tmbr_default_field_names = [
    # See write_timber_csv() for description. 
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
    'factor__reference__study_design__study_design_name',
    'factor__id',
    'factor__pid_factor',
    'factor__factor_title',
    'factor__factor_description',
    'factor__group_factor',
    'factor__group_comparator',
    'factor__host_level_01__host_01_name',
    'factor__host_level_02__host_subtype_name',
    'factor__host_production_stream',
    'factor__host_life_stage',
    'factor__group_allocate_production_stage__production_stage_name',
    'group_observe_production_stage__production_stage_name',
    'moa_type__moa_type_name',
    'moa_unit__outcome_unit_name',
    'resistance__levelname_4_coarse',
    'resistance__levelname_5',
    'resistance_gene__genetic_element_name',
    'microbe_level_01__microbe_01_name',
    'microbe_level_02__microbe_02_name',
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
    'table_n_ab',
    'table_n_cd',
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
    'factor__reference__study_design__study_design_name',
    'factor__id',
    'factor__pid_factor',
    'factor__factor_title',
    'factor__factor_description',
    'factor__group_factor',
    'factor__group_comparator',
    'factor__host_level_01__host_01_name',
    'factor__host_level_02__host_subtype_name',
    'factor__host_production_stream',
    'factor__host_life_stage',
    'factor__group_allocate_production_stage__production_stage_name',
    'group_observe_production_stage__production_stage_name',
    'moa_type__moa_type_name',
    'moa_unit__outcome_unit_name',
    'resistance__levelname_4_coarse',
    'resistance__levelname_5',
    'resistance_gene__genetic_element_name',
    'microbe_level_01__microbe_01_name',
    'microbe_level_02__microbe_02_name',
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
    'table_n_ab',
    'table_n_cd',
    'odds_ratio',
    'odds_ratio_lo',
    'odds_ratio_up',
    'odds_ratio_sig',
    'odds_ratio_confidence',
    )


    writer_head = csv.writer(response)
    writer_head.writerow(tmbr_default_col_names)

    writer = csv.DictWriter(f=response,                     
                        fieldnames=tmbr_default_field_names,  # Field names (matching QuerySet)
                        extrasaction='ignore')        # Ignore non-selected fields (through omission in tmbr_field_names) in tmbr_qs. 

        # Loop, writing each line of the QuerySet to the .CSV.
    for eachline in timber_qs_all:
        writer.writerow(eachline)


    return response



class PublisherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return publisher.objects.none()

        qs = publisher.objects.all()

        if self.q:
            qs = qs.filter(pub_title__istartswith=self.q)

        return qs



@login_required
def query_timber(request):

    # Only allows one host to be queried at a time
    # The option to filter by antimicrobial class uses the ATCvet codes' matching of individual drugs to classes. 
        # There's some discrepancies between ATCvet codes and Health Canada's VDD classification/Colleen's classification, so I've depreciated this option. 
        # Legacy code for this is located in old_timber_query.py

    if request.method == 'POST':
        
        query_form = QuerySelectForm(request.POST)
        
        #Example query
        #factor.objects.filter(host_01=4).filter(Q(microbe_01=4) | Q(microbe_01=2)).filter()
        
        if query_form.is_valid():
            
            microbes = [int(item) for item in query_form.cleaned_data['microbes']]
            host_name = int(query_form.cleaned_data['hosts'][0])
            
            # Export all associations with resistance if all checkboxes are checked, or if no checkboxes are checked

            if ((not microbes) and (not host_name)) or (len(microbes) == 4 and (not host_name)):
                query_string = 'res_outcome.objects.filter(Q(fk_factor_id__fk_factor_reference_id__capture_search_2019=True) & Q(fk_factor_id__fk_factor_reference_id__archived=False) & Q(fk_factor_id__fk_factor_reference_id__capture_2019_reject=False))'
            
            # Otherwise, filter the associations with resistance selected for export based on checked checkboxes
            else:

                # Start the query string by only filtering to the valid 2019 search results
                query_string = 'res_outcome.objects.filter(Q(fk_factor_id__fk_factor_reference_id__capture_search_2019=True) & Q(fk_factor_id__fk_factor_reference_id__archived=False) & Q(fk_factor_id__fk_factor_reference_id__capture_2019_reject=False))'

                # Filter by host only
                
                # If cattle, need to select multiple hosts (cattle, dairy cattle, and beef cattle)
                if host_name == '4':
                    query_string += '.filter(fk_factor_id__host_level_01__host_name__contains="Cattle")'
                else:
                    query_string += '.filter(fk_factor_id__host_level_01=host_name)'

                # Filter by host and microbe
                
                if len(microbes) >= 1 and len(microbes) < 4:
                    query_string += '.filter('
                    for mic_count in range(len(microbes)):
                        microbe_id = microbes[mic_count]
                        query_string += 'Q(fk_microbe_01_id=%d)' % (microbe_id)
                        if len(microbes) > 1 and (mic_count < len(microbes)-1):
                            query_string += ' | '
                    query_string += ')'
            
            # Perform the filtering to get the desired factors   
            export_ros = eval(query_string)
            
            # Return a pop-up if no factors/associations with resistance exist meeting the query criteria

            if len(export_ros) == 0:
                # return popup
                return render(request, 'cedar_core/query_timber.html', {'query_form': QuerySelectForm(), 'page_title': 'Export Timber', 'message_text': 'No factors exist that meet the chosen criteria. Please try broadening your query'})
            
            # Return a list of all the soids
            soids = np.array([])
            for ro in export_ros:
                np.append(soids, ro.soid)
            unique, counts = np.unique(soids, return_counts=True) # unique is an array of all unique soids, and counts is an array the same size as unique, where the values are the number of times each soid occurs in the main soids array

            if all(i < 2 for i in counts) == False: # if there are any duplicate soids (i.e., if at least one soid appears more than once)
                for count_index in range(0,len(counts)):

                    # If we've reached an soid that appears twice (i.e., an association with resistance for which there are 2 different extractions)
                    if counts[count_index] > 1:
                        duplicate_soid = unique[count_index]
                        duplicate_ros = export_ros.filter(soid=duplicate_soid)
                        extract_dates = np.array([])
                        ids = np.array([])
                        for ro_dup in duplicate_ros:
                            np.append(extract_dates, ro_dup.extract_date_ro)
                            np.append(ids, ro_dup.id)
                        most_recent_date = max(extract_dates)
                        most_recent_ros = export_ros.filter(Q(soid=duplicate_soid) & Q(extract_date_ro=most_recent_date))

                        # If there are multiple extractions with the most recent date, pick the one with the largest id
                        if len(most_recent_ros) > 1:
                            most_recent_ro_ids = np.array([])
                            for ro_recent in most_recent_ros:
                                np.append(most_recent_ro_ids, ro_recent.id)
                            chosen_id = max(most_recent_ro_ids)
                        else:
                            chosen_id = most_recent_ros[0].id
                        
                        # Delete the non-up-to-date extractions for this soid from the query results

                        for current_id in ids:
                            if current_id != chosen_id:
                                export_ros = export_ros.exclude(id=current_id)

            
            # Prepare all required fields for a .csv file export (raw timber)
            
            timber_header = ['RWID', 'ident_doi', 'ident_pmid', 'name_bibtex', 'ref_title',
                            'factor_title', 'factor_description', 'host_01', 'host_02', 
                            'group_exposed', 'group_referent', 'stage_allocate',
                            'ID_factor', 'association_with_resistance_id', 'AMR', 'gene', 'microbe_01', 'microbe_02',
                            'stage_observe', 'res_format', 'res_unit', 'place_in_text',
                            'contable_a', 'contable_b', 'contable_c', 'contable_d', 'prevtable_a', 'prevtable_b', 'prevtable_c',
                            'prevtable_d', 'table_n_ab', 'table_n_cd', 'odds_ratio', 'odds_ratio_lo', 'odds_ratio_up',
                            'odds_ratio_sig', 'odds_ratio_confidence','figure_extract', 'figure_extract_method', 
                            'extract_date_ro', 'ID_meta', 'meta_amr', 'meta_type']
            
            # Fields that will be filled with values from the reference table
            ref_fields = timber_header[0:5]

            # Fields that will be filled with values from the factor table
            fac_fields = timber_header[5:12]
            
            # Fields from the res_outcome table to delete
            del_fields = ['id', 'fk_res_outcome_ast_method_id', 'fk_ast_breakpoint_source_id', 'breakpoint_explicit',
                        'figure_extract_reproducible', 'fk_extract_res_outcome_user_id', 'factor_v0_id', 'v12_is_v1_import',
                        'v12_ID_factor_v1', 'v12_ID_reference_v1', 'v12_ID_reference_v2_initial', 'v12_solo_extraction_2016']
            
            # Fields that will have null values, to be filled in by sawmill and users
            null_fields = ['ID_meta', 'meta_amr', 'meta_type']
            
            # Make a template dictionary of the raw data, excluding fields that won't be in the raw timber (i.e. that won't have a matching field in the new data)
            new_raw_dict = model_to_dict(export_ros[0])
            for del_field in del_fields:
                del new_raw_dict[del_field]
            raw_names = list(new_raw_dict.keys())
            
            # Dictionary to map new field names to their corresponding names in the raw data
            field_match_dict = dict.fromkeys(timber_header[12:]) # names from timber_header (the ones that will appear in the output file) are 
            # Populate field_match_dict dictionary
            for i in range(len(raw_names)):
                field_name = list(field_match_dict.keys())[i]
                field_match_dict[field_name] = raw_names[i]
            
            # Create dictionary to hold final data for csv file
            query_dict = dict.fromkeys(timber_header)
            
            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="timber_export.csv"'
            writer = csv.writer(response)
            writer.writerow(timber_header)
    
            # Write a new row in the CSV file for each factor that needs exporting
            for ro in export_ros:
                
                # Get the raw data for the current association with resistance
                raw_ro_dict = model_to_dict(ro)
                
                # Replace ids with values for foreign key fields in the raw data
                raw_ro_dict['fk_factor_id'] = ro.fk_factor_id
                raw_ro_dict['fk_resistance_atc_vet_id'] = ro.fk_resistance_atc_vet_id.levelname_5
                
                try:
                    raw_ro_dict['fk_genetic_element_id'] = ro.fk_genetic_element_id.element_name
                except AttributeError:
                    continue

                raw_ro_dict['fk_microbe_01_id'] = ro.fk_microbe_01_id.microbe_name
                raw_ro_dict['fk_res_outcome_microbe_02_id'] = ro.fk_res_outcome_microbe_02_id.microbe_subtype_name
                raw_ro_dict['fk_group_observe_production_stage_id'] = ro.fk_group_observe_production_stage_id.stage
                raw_ro_dict['fk_moa_type_id'] = ro.fk_moa_type_id.res_format
                raw_ro_dict['fk_moa_unit_id'] = ro.fk_moa_unit_id.res_unit
                
                try:
                    raw_ro_dict['fk_figure_extract_method_id'] = ro.fk_figure_extract_method_id.method_name
                except AttributeError:
                    continue

                # Populate the query_dict with raw data
                for field in timber_header:
                    
                    # Reference-level fields: retrieve the values
                    if field in ref_fields:
                        query_dict[field] = eval("ro.fk_factor_id.fk_factor_reference_id.%s" % (field))
                    # Factor-level fields: retrieve the values from raw data
                    elif field in fac_fields:
                        if field == 'host_01':
                            query_dict[field] = ro.fk_factor_id.host_01_id.host_name
                        elif field == 'host_02':
                            query_dict[field] = ro.fk_factor_id.host_02_id.host_subtype_name
                        elif field == 'stage_allocate':
                            query_dict[field] = ro.fk_factor_id.group_allocate_production_stage.stage
                        else:
                            query_dict[field] = eval("ro.fk_factor_id.%s" % (field))
                    elif field not in null_fields:
                        old_field = field_match_dict[field]
                        query_dict[field] = raw_ro_dict[old_field] # raw dictionary is indexed by the old names
            
                # Write row to CSV
                writer.writerow(list(query_dict.values()))
            return response
        else:
            print('QUERY FORM NOT VALID')
    else:
        query_form = QuerySelectForm()
    query_form = QuerySelectForm()
    
    context = {'query_form': query_form, 'page_title': 'Export a Query'}
    return render(request, 'cedar_core/query_timber.html', context)







@login_required
def topic_tab_query(request):

    # Returns papers from 2019 search only, no archived, capture_2019_reject = false (i.e. not including any references from the 2019 search that were erroneously included in CEDAR), for a particular host/microbe combination

    MICROBE_CHOICES = {
        1: 'campylobacter',
        2: 'ecoli',
        3: 'salmonella',
        4: 'enterococcus'
    }
    
    HOST_CHOICES = {
        1: 'chicken',
        2: 'swine',
        3: 'turkey',
        4: 'cattle'
    }

    if request.method == 'POST':
        query_form = TopicTabForm(request.POST)
        
        #Example query
        #factor.objects.filter(host_01=4).filter(Q(microbe_01=4) | Q(microbe_01=2)).filter()

        if query_form.is_valid():
            
            microbes = [int(item) for item in query_form.cleaned_data['microbes']]
            hosts = [int(item) for item in query_form.cleaned_data['hosts']]

            query_string = 'reference.objects.filter(capture_search_2019=True).filter(Q(archived=False)).filter(Q(capture_2019_reject=False))'

            # Export all references if all checkboxes are checked, or if no checkboxes are checked
            if ((not microbes) and (not hosts)) or (len(microbes) == 4 and (not hosts)):
                query_string = 'reference.objects.filter(capture_search_2019=True).filter(Q(archived=False)).filter(Q(capture_2019_reject=False))'
                
            # Otherwise, filter the references selected for export based on checked checkboxes
            else:
                # Initial string

                # Filter by topic tab (allows for multiple hosts and multiple microbes)
                if len(hosts) >= 1 and len(hosts) < 4:
                    query_string += '.filter('
                    for h_count in range(len(hosts)):
                        host_id = hosts[h_count]
                        query_string += 'Q(topic_tab_%s=True)' % (HOST_CHOICES[host_id])
                        if len(hosts) > 1 and (h_count < len(hosts)-1):
                            query_string += ' | '
                    query_string += ')'

                if len(microbes) >= 1 and len(microbes) < 4:
                    query_string += '.filter('
                    for mic_count in range(len(microbes)):
                        microbe_id = microbes[mic_count]
                        query_string += 'Q(topic_tab_%s=True)' % (MICROBE_CHOICES[microbe_id])
                        if len(microbes) > 1 and (mic_count < len(microbes)-1):
                            query_string += ' | '
                    query_string += ')'
                
            # Evaluate the query string
            export_refs = eval(query_string)
    
            # Return a pop-up if no papers exist meeting the query criteria
            if len(export_refs) == 0:
                return render(request, 'cedar_core/query_topic_tab.html', {'query_form': TopicTabForm(), 'page_title': 'Query Papers', 'message_text': 'No factors exist that meet the chosen criteria. Please try broadening your query'})

            #query_header = ['id', 'key_bibtex', 'ref_author', 'ref_title', 'exclude_extraction', 'exclude_extraction_reason', 'fk_cedar_exclude_id']
            
            ref_fields_dict = model_to_dict(export_refs[0])
            query_header = list(ref_fields_dict.keys())
            
            # Create an empty dictionary to hold final data for csv file
            query_dict = dict.fromkeys(query_header)

            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="CEDAR_papers_query.csv"'
            writer = csv.writer(response)
            writer.writerow(query_header)
    
            # Write a new row in the CSV file for each factor that needs exporting
            for ref in export_refs:
                
                # Get the raw data for the current factor
                raw_ref_dict = model_to_dict(ref)
                
                # Replace ids with values for foreign key fields in the raw data
                if not ref.fk_cedar_exclude_id: # if None, empty string, or false, won't be able to reference exclusion (the text description of the field corresponding to the foreign key id)
                    raw_ref_dict['fk_cedar_exclude_id'] = ref.fk_cedar_exclude_id
                else:
                    raw_ref_dict['fk_cedar_exclude_id'] = ref.fk_cedar_exclude_id.exclusion

                # Populate the query_dict with raw data
                for field in query_header:
                    query_dict[field] = raw_ref_dict[field]
            
                # Write row to CSV
                writer.writerow(list(query_dict.values()))
            return response
        else:
            print('QUERY FORM NOT VALID')
    else:
        query_form = TopicTabForm()
    query_form = TopicTabForm()

    context = {'query_form': query_form, 'page_title': 'Query Papers Based on Host and Microbe'}
    return render(request, 'cedar_core/query_topic_tab.html', context)
    

def about(request):


    context = {'page_title': 'Help with CEDAR'}
    return render(request, 'cedar_core/about.html', context)





def export_timber_part(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    

    tmbr_default_field_names = [
    # See write_timber_csv() for description. 
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
    'factor__reference__study_design__study_design_name',
    'factor__id',
    'factor__pid_factor',
    'factor__factor_title',
    'factor__factor_description',
    'factor__group_factor',
    'factor__group_comparator',
    'factor__host_level_01__host_01_name',
    'factor__host_level_02__host_subtype_name',
    'factor__host_production_stream',
    'factor__host_life_stage',
    'factor__group_allocate_production_stage__production_stage_name',
    'group_observe_production_stage__production_stage_name',
    'moa_type__moa_type_name',
    'moa_unit__outcome_unit_name',
    'resistance__levelname_4_coarse',
    'resistance__levelname_5',
    'resistance_gene__genetic_element_name',
    'microbe_level_01__microbe_01_name',
    'microbe_level_02__microbe_02_name',
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
    'table_n_ab',
    'table_n_cd',
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
    'factor__reference__study_design__study_design_name',
    'factor__id',
    'factor__pid_factor',
    'factor__factor_title',
    'factor__factor_description',
    'factor__group_factor',
    'factor__group_comparator',
    'factor__host_level_01__host_01_name',
    'factor__host_level_02__host_subtype_name',
    'factor__host_production_stream',
    'factor__host_life_stage',
    'factor__group_allocate_production_stage__production_stage_name',
    'group_observe_production_stage__production_stage_name',
    'moa_type__moa_type_name',
    'moa_unit__outcome_unit_name',
    'resistance__levelname_4_coarse',
    'resistance__levelname_5',
    'resistance_gene__genetic_element_name',
    'microbe_level_01__microbe_01_name',
    'microbe_level_02__microbe_02_name',
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
    'table_n_ab',
    'table_n_cd',
    'odds_ratio',
    'odds_ratio_lo',
    'odds_ratio_up',
    'odds_ratio_sig',
    'odds_ratio_confidence',
    )


    filt = timber_filter(request.GET, queryset=timber_qs_all).qs

    writer_head = csv.writer(response)
    writer_head.writerow(tmbr_default_col_names)

    writer = csv.DictWriter(f=response,                     
                        fieldnames=tmbr_default_field_names,  # Field names (matching QuerySet)
                        extrasaction='ignore')        # Ignore non-selected fields (through omission in tmbr_field_names) in tmbr_qs. 

        # Loop, writing each line of the QuerySet to the .CSV.
    for eachline in filt:
        writer.writerow(eachline)


    return response
