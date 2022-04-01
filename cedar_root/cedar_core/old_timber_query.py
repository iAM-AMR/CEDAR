# TO DO: re-work the if POST statement to accommodate factor/res_outcome separation of models
def query_timber(request):
    if request.method == 'POST':
        
        print('ENTERED POST')
        query_form = QuerySelectForm(request.POST)
        
        #Example query
        #factor.objects.filter(host_01=4).filter(Q(microbe_01=4) | Q(microbe_01=2)).filter()
        #factor.objects.filter(reference_id=10004).filter(Q(resistance__levelname_4='Macrolides') | Q(resistance__levelname_4='Penicillins with extended spectrum'))
        
        if query_form.is_valid():
            print('CLEANED DATA')
            print(query_form.cleaned_data)
            
            microbes = [int(item) for item in query_form.cleaned_data['microbes']]
            am_classes = query_form.cleaned_data['am_classes']
            ams = query_form.cleaned_data['ams']
            host_name = int(query_form.cleaned_data['hosts'][0])
            
            print(microbes)
            print(am_classes)
            print(ams)
            print(host_name)
            
            # Set drugs list based on whether user is filtering by specific antimicrobial or by antimicrobial class
            if len(ams) == 0:
                drugs = am_classes
                drug_level = '4'
            else:
                drugs = ams
                drug_level = '5'
            
            # Export all associations with resistance if all checkboxes are checked, or if no checkboxes are checked
            if ((not microbes) and (not drugs) and (not host_name)) or (len(microbes) == 4 and len(drugs) == 4):
                query_string = 'res_outcome.objects.all()'
                
            # Otherwise, filter the associations with resistance selected for export based on checked checkboxes
            else:
                # Filter by host only
                
                # If cattle, need to select multiple hosts (cattle, dairy cattle, and beef cattle)
                if host_name == '4':
                    query_string = 'res_outcome.objects.filter(fk_factor_id__fk_factor_host_01_id__host_name__contains="Cattle")'
                else:
                    query_string = 'res_outcome.objects.filter(fk_factor_id__fk_factor_host_01_id=host_name)'

                # Filter by host and microbe (all drugs)
                
                if len(drugs) == 0 or len(drugs) == 4:
                    query_string += '.filter('
                    for mic_count in range(len(microbes)):
                        microbe_id = microbes[mic_count]
                        query_string += 'Q(fk_microbe_01_id=%d)' % (microbe_id)
                        if len(microbes) > 1 and (mic_count < len(microbes)-1):
                            query_string += ' | '
                    query_string += ')'
                
                # Filter by host and drug (all microbes)
                
                elif len(microbes) == 0 or len(microbes) == 4:
                    query_string += '.filter('
                    for drug_count in range(len(drugs)):
                        drug_id = drugs[drug_count]
                        query_string += 'Q(fk_resistance_atc_vet_id__levelname_%s="%s")' % (drug_level, drug_id)
                        if len(drugs) > 1 and (drug_count < len(drugs)-1):
                            query_string += ' | '
                    query_string += ')'
                
                # Filter by host, microbe, and drug
                
                else:
                    
                    # Append microbe filtering
                    query_string += '.filter('
                    for mic_count in range(len(microbes)):
                        microbe_id = microbes[mic_count]
                        query_string += 'Q(fk_microbe_01_id=%d)' % (microbe_id)
                        if len(microbes) > 1 and (mic_count < len(microbes)-1):
                            query_string += ' | '
                    query_string += ')'
                    
                    # Append drug filtering
                    query_string += '.filter('
                    for drug_count in range(len(drugs)):
                        drug_id = drugs[drug_count]
                        query_string += 'Q(fk_resistance_atc_vet_id__levelname_%s="%s")' % (drug_level, drug_id)
                        if len(drugs) > 1 and (drug_count < len(drugs)-1):
                            query_string += ' | '
                    query_string += ')'
            
            print(query_string)
            
            # Perform the filtering to get the desired factors   
            export_ros = eval(query_string)
            
            # Return a pop-up if no factors exist meeting the query criteria
            if len(export_ros) == 0:
                # return popup
                #messages.info(request, 'No factors exist that meet the chosen criteria. Please try broadening your query')
                return render(request, 'cedar_core/query_timber.html', {'query_form': QuerySelectForm(), 'page_title': 'Export Timber', 'message_text': 'No factors exist that meet the chosen criteria. Please try broadening your query'})
            
            # Return a list of all the ufids
            ##for each ro in export_ros:
                #
            
            # Prepare all required fields for a .csv file export (raw timber)
            
            #timber_header = ['RWID', 'ident_doi', 'ident_pmid', 'name_bibtex', 'ID_factor', 'AMR', 'factor_title','factor_description', 'host_01', 'host_02', 'microbe_01', 'microbe_02', 'stage_allocate', 'stage_observe', 'group_exposed', 'group_referent', 'res_format', 'res_unit', 'contable_a', 'contable_b', 'contable_c', 'contable_d', 'prevtable_a', 'prevtable_b', 'prevtable_c', 'prevtable_d', 'table_n_exp', 'table_n_ref', 'odds_ratio', 'odds_ratio_lo', 'odds_ratio_up', 'odds_ratio_sig', 'odds_ratio_confidence', 'ID_meta', 'meta_amr', 'meta_type']
            
            timber_header = ['refwk', 'publish_doi', 'publish_pmid', 'key_bibtex', 'ID_factor', 'AMR', 'factor_title',
                            'factor_description', 'host_01', 'host_02', 'microbe_01', 'microbe_02', 'stage_allocate',
                            'stage_observe', 'group_exposed', 'group_referent', 'res_format', 'res_unit', 'contable_a',
                            'contable_b', 'contable_c', 'contable_d', 'prevtable_a', 'prevtable_b', 'prevtable_c',
                            'prevtable_d', 'table_n_exp', 'table_n_ref', 'odds_ratio', 'odds_ratio_lo', 'odds_ratio_up',
                            'odds_ratio_sig', 'odds_ratio_confidence', 'ID_meta', 'meta_amr', 'meta_type']
            
            # Fields that will be filled with values from the attached reference's fields
            ref_fields = timber_header[0:4]
            print(ref_fields)
            
            # Fields from raw factor data to delete
            del_fields = ['factor_ref_id', 'place_in_text', 'factor_v0_id', 'v12_is_v1_import', 'v12_ID_factor_v1', 
                          'v12_ID_reference_v1', 'v12_ID_reference_v2_initial', 'v12_solo_extraction_2016', 'amu_id',
                          'DEP_total_obs', 'DEP_exclude_iam', 'DEP_exclude_iam_reason', 'OLD_short_name', 'OLD_resistance_id',
                          'OLD_use_id', 'microbe_02_old_id', 'TEMP_use_id', 'exclude_cedar', 'exclude_cedar_reason']
            
            # Fields that will have null values, to be filled in by sawmill and users
            null_fields = ['ID_meta', 'meta_amr', 'meta_type']
            
            # Make a template dictionary of the raw data, excluding fields that won't be in the raw timber (i.e. that won't have a matching field in the new data)
            new_raw_dict = model_to_dict(export_ros[0])
            for del_field in del_fields:
                del new_raw_dict[del_field]
            raw_names = list(new_raw_dict.keys())
            
            # Dictionary to map new field names to their corresponding names in the raw data
            field_match_dict = dict.fromkeys(timber_header[4:])
            # Populate field_match_dict dictionary
            for i in range(len(raw_names)):
                field_name = list(field_match_dict.keys())[i]
                field_match_dict[field_name] = raw_names[i]
            
            # Create dictionary to hold final data for csv file
            query_dict = dict.fromkeys(timber_header)
            
            # Create the HttpResponse object with the appropriate CSV header.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="CEDAR_query.csv"'
            writer = csv.writer(response)
            writer.writerow(timber_header)
    
            # Write a new row in the CSV file for each factor that needs exporting
            for ro in export_ros:
                
                # Get the raw data for the current factor
                raw_ro_dict = model_to_dict(ro)
                
                # Replace ids with values for foreign key fields in the raw data
                raw_ro_dict['resistance_id'] = ro.resistance_id.levelname_5
                raw_ro_dict['host_01_id'] = ro.host_01_id.host_name
                raw_ro_dict['host_02_id'] = ro.host_02_id.host_subtype_name
                raw_ro_dict['microbe_01_id'] = ro.microbe_01_id.microbe_name
                raw_ro_dict['microbe_02_id'] = ro.microbe_02_id.microbe_subtype_name
                raw_ro_dict['prod_stage_group_allocate_id'] = ro.prod_stage_group_allocate_id.stage
                raw_ro_dict['prod_stage_group_observe_id'] = ro.prod_stage_group_observe_id.stage
                raw_ro_dict['moa_type_id'] = ro.moa_type_id.res_format
                raw_ro_dict['moa_unit_id'] = ro.moa_unit_id.res_unit
                
                #print('RAW FACTOR DICTIONARY')
                #print(raw_fac_dict)
                
                # Populate the query_dict with raw data
                for field in timber_header:
                    
                    # Reference-level fields: retrieve the values
                    if field in ref_fields:
                        query_dict[field] = eval("ro.factor_ref_id.%s" % (field))
                    # Factor-level fields: retrieve the values from raw data
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