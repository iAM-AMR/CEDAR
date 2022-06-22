from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from crispy_forms.utils import render_crispy_form

from .models import reference, reference_join_location, reference_join_reference_note, factor, publisher, res_outcome

from .forms import ReferenceForm, RefLocForm, RefLocFormSet, RefLocFormSetHelper, RefNoteForm, RefNoteFormSet, RefNoteFormSetHelper, QuerySelectForm, TopicTabForm, FactorForm, ResistanceOutcomeForm

from django.forms.models import model_to_dict, formset_factory, modelformset_factory
from django.urls import reverse
from django.db.models import F, Q

from django.utils import timezone

import csv
import numpy as np

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from dal import autocomplete

import re

class PublisherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return publisher.objects.none()

        qs = publisher.objects.all()

        if self.q:
            qs = qs.filter(pub_title__istartswith=self.q)

        return qs


@login_required
@permission_required('cedar_core.add_factor') # this permission check serves to verify that the logged in user is part of the "Edit" permissions group
def view_references(request):
    
    refs_list = reference.objects.order_by('key_bibtex')
    
    #************************ COMMENTED OUT: CHECKBOX CODE**********************************************
    # If data is incoming from the server, filtering can happen based on the checkboxes that have been checked
    """if request.method == 'POST':
        
        # Get checked checkboxes from webpage. If none are chcked, request_getdata is None
        print('POST')
        request_getdata = request.POST.get('getdata', None)
        print(request_getdata)
        
        # Parse out a list of all the checked host names
        filter_hosts = re.split("&",request_getdata)[1:]
        
        # Filtering is not necessary if none, or if all of the checkboxes are checked
        if 0 < len(filter_hosts) < 4:
            total_refs = {}
            #curr_refs_list = []
            
            # Filter the list by each checked checkbox and store each filtered list in a total_refs dictionary
            for host in filter_hosts:
                host_field = "topic_tab_" + re.search("(?<=\=)(.*)",host).group()
                print(host_field)
                total_refs[host_field] = exec("reference.objects.filter(%s=1)" % (host_field))
            
            # In progress: Combine the filtered lists and remove duplicates, saving a new refs_list 
            combine_exp = "refs_list = "
            count = 0
            for key in total_refs:
                count += 1
                if count == len(total_refs):
                    combine_exp += "total_refs['%s']" % (key)
                else:
                    combine_exp += "total_refs['%s'] | " % (key)
            exec(combine_exp)
        context = {'refs_list': refs_list}
        return render(request, 'cedar_core/view_refs_new.html', context)
    """
    
    context = {'refs_list': refs_list, 'page_title': 'References'}
    return render(request, 'cedar_core/view_refs_new.html', context)

@login_required
@permission_required('cedar_core.add_factor')
def view_factors(request, ref_id):
    
    try:
        ref = reference.objects.get(pk=ref_id)
    except ref.DoesNotExist:
        raise Http404("Reference does not exist")
    
    ref_factors = ref.factor_set.all()
    
    # **********Legacy code (depreciated): Retrieve 2x2 table info (contingency or prevalence) (back when resistance outcomes & factors were in the same table)*********************
    
    #fac_data = {} # stores 2x2 info in order of A, B, C, D (or P, R, Q, S)
    #for f in ref_factors:
        #if f.moa_type == 'Contingency Table':
            #fac_data = [f.contable_a, f.contable_b, f.contable_c, f.contable_d]
        #else if f.moa_type == 'Prevalence Table':
            #fac_data = [f.prevtable_a, f.prevtable_b, f.prevtable_c, f.prevtable_d]
            
    #for i in range(0,len(ref_factors)):
        #if 'Contingency Table' in ref_factors[i].moa_type:
            #print('ct')
            #fac_data[i] = [f.contable_a, f.contable_b, f.contable_c, f.contable_d]
        #elif 'Prevalence Table' in ref_factors[i].moa_type:
            #print('rt')
            #fac_data[i] = [f.prevtable_a, f.prevtable_b, f.prevtable_c, f.prevtable_d]
    #*************************************************************************************************

    rfs_serialized = []
    for rf in ref_factors:
        rfs_serialized.append(model_to_dict(rf))

    #Loop through json dumps on rfs_serialized (each dictionary in this list)
    #rfs_json = json.dumps(rfs_serialized, cls=DjangoJSONEncoder)
    
    context = {
        'ref': ref,
        'ref_factors': ref_factors,
        'page_title': 'View Factors',
    }
    return render(request, 'cedar_core/view_factors.html', context)

@login_required
@permission_required('cedar_core.add_factor')
def view_resistance_outcomes(request, ref_id, fac_id):

    ref = reference.objects.get(pk=ref_id)
    
    try:
        fac = factor.objects.get(pk=fac_id)
    except fac.DoesNotExist:
        raise Http404("Factor does not exist")
    
    fac_ros = fac.res_outcome_set.all()

    # TO DO: Pull only the most recent entry under each soid (see code under query_timber view)


    ros_serialized = []
    for ro in fac_ros:
        ros_serialized.append(model_to_dict(ro))
    
    context = {
        'fac': fac,
        'ref': ref,
        'fac_ros': fac_ros,
        'page_title': 'View Associations with Resistance',
    }
    return render(request, 'cedar_core/view_resistance_outcomes.html', context)


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
                            'prevtable_d', 'table_n_exp', 'table_n_ref', 'odds_ratio', 'odds_ratio_lo', 'odds_ratio_up',
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


### This view has been depreciated, now that factors and resistance outcomes are in separate tables
"""@login_required
@permission_required('cedar_core.add_factor')
def expand_factor(request, ref_id, fac_id):
    
    ref = reference.objects.get(pk=ref_id)
    ref_factors = ref.factor_set.all()
    main_fac = factor.objects.get(id=fac_id)
    result_type = factor._meta.get_field('moa_type_id').value_from_object(main_fac)
    
    if request.method == 'POST':
        # Create the appropriate factor data form depending on the result type.
        if result_type == 4:
            exp_form = OddsTableForm(request.POST, initial=model_to_dict(main_fac), instance=main_fac)
        elif result_type == 2:
            exp_form = PrevTableForm(request.POST, initial=model_to_dict(main_fac), instance=main_fac)
        else:
            exp_form = ConTableForm(request.POST, initial=model_to_dict(main_fac), instance=main_fac)
        
        if exp_form.is_valid():
            
            print('CLEANED DATA')
            print(exp_form.cleaned_data)
            
            output = exp_form.save()

    else:
        # Create the appropriate factor data form depending on the result type.
        if result_type == 4:
            exp_form = OddsTableForm(initial=model_to_dict(main_fac), instance=main_fac)
        elif result_type == 2:
            exp_form = PrevTableForm(initial=model_to_dict(main_fac), instance=main_fac)
        else:
            exp_form = ConTableForm(initial=model_to_dict(main_fac), instance=main_fac)
    
    context = {
        'ref': ref,
        'ref_factors': ref_factors,
        'exp_form': exp_form,
        'page_title': 'View Factors',
    }
    return render(request, 'cedar_core/view_factors.html', context)
"""

@login_required
@permission_required('cedar_core.add_factor')
def delete_factor(request, ref_id, fac_id):
    
    # Delete the factor
    del_fac = factor.objects.get(id=fac_id)
    del_fac.delete(commit=False)
    
    # Reload the view factors page
    ref = reference.objects.get(pk=ref_id)
    ref_factors = ref.factor_set.all()
    
    context = {
        'ref': ref,
        'ref_factors': ref_factors,
    }
    
    return redirect('/cedar_core/references/' + str(ref_id) + '/factors/')

@login_required
@permission_required('cedar_core.add_factor')
def ref_detail(request, ref_id):

    try:
        ref = reference.objects.get(pk=ref_id)
    except ref.DoesNotExist:
        raise Http404("Reference does not exist")

    # If this is a POST request, process the form data
    if request.method == 'POST':
        
        # Create form instances and populate them with data from the request
        
        # Main and Study Design tabs
        ref_form = ReferenceForm(request.POST, initial=model_to_dict(ref), instance=ref)
        
        # Location tab
        ref_locs = ref.reference_join_location_set.all().order_by(F('location_main_id').asc(nulls_first=True))
        loc_formset = RefLocFormSet(request.POST, instance=ref)
        loc_helper = RefLocFormSetHelper()
        
        # Notes and Issues tab
        ref_notes = ref.reference_join_reference_note_set.all()
        note_formset = RefNoteFormSet(request.POST, instance=ref)
        note_helper = RefNoteFormSetHelper()
        
        # Save ref form if valid (and output checks to the console)
        if ref_form.is_valid():

            #process the data in form.cleaned_data as required (i.e. save to database, etc.)
            #...
            print(ref_form.cleaned_data) # need this line as ref_form.cleaned_data must be called before ref_form.save()
            print('CLEANED DATA')
            
            output = ref_form.save(commit=False) #save changes to the database

            print('SAVED FORM')
            print(output)
            
        else:
            print('REF FORM NOT VALID')

        # Save notes and issues form set if valid
        if note_formset.is_valid():
            print('NOTE FORMSET IS VALID')
            note_formset.save(commit=False)
            print(note_formset.cleaned_data)
        else:
            print('NOTE FORMSET NOT VALID')
        
        # Save location form set if valid
        if loc_formset.is_valid():
            print('LOC FORMSET IS VALID')
            for f in loc_formset:
                print(f.cleaned_data)
            loc_formset.save(commit=False)
        else:
            print('LOC FORMSET NOT VALID')
            for f in loc_formset:
                print(f.cleaned_data)
            print(loc_formset.errors)

    # If request is a GET (or any other method) we'll create a blank form for each tab (pre-populated with fields that are not empty)
    else:
        ref_form = ReferenceForm(initial=model_to_dict(ref), instance=ref)
        
        # Location
        ref_locs = ref.reference_join_location_set.all().order_by(F('location_main_id').asc(nulls_first=True))
        loc_formset = RefLocFormSet(instance=ref)
        loc_helper = RefLocFormSetHelper()
        
        # Notes
        ref_notes = ref.reference_join_reference_note_set.all()
        note_formset = RefNoteFormSet(instance=ref)
        note_helper = RefNoteFormSetHelper()
    
    context = {'ref': ref,
               'ref_form': ref_form,
               'ref_form_helper': ref_form.helper,
               'loc_formset': loc_formset,
               'loc_helper': loc_helper,
               'note_formset': note_formset,
               'note_helper': note_helper,
               'page_title': 'Update a Reference',
               }
    return render(request, 'cedar_core/ref_detail.html', context)

# Add either a new reference note, reference location, factor, or res_outcome
@login_required
@permission_required('cedar_core.add_factor')
def add_new_obj(request, obj_id, form_type):
    
    # TO DO: create a case for creating a new res_outcome (when the new res_outcome button on the view_resistance_outcomes page) -- very similar to the new factor button on the view factors page

    obj = reference.objects.get(pk=obj_id)

    if form_type == 'loc':
        new_obj = reference_join_location(fk_reference_join_location_reference_id = obj)
        redir_path = '/cedar_core/references/' + str(obj_id) + '/#loc-md'
    elif form_type == 'note':
        new_obj = reference_join_reference_note(fk_reference_join_note_reference_id = obj)
        redir_path = '/cedar_core/references/' + str(obj_id) + '/#notes-md'
    else: #form_type = 'fac'
        new_obj = factor(fk_factor_reference_id = obj)
        redir_path = '/cedar_core/references/' + str(obj_id) + '/factors'
    
    # Save new object and redirect
    new_obj.save(commit=False)
    
    return redirect(redir_path)

@login_required
@permission_required('cedar_core.add_factor')
def factor_detail(request, ref_id, fac_id):
    
    ref = reference.objects.get(pk=ref_id)
    
    #Get factor
    try:
        fac = factor.objects.get(pk=fac_id)
    except fac.DoesNotExist:
        raise Http404("Factor does not exist")
    
    # Sample code for setting fields to read only
    #for f in range(len(factor_forms)):
        #curr_factor = factor_forms[f]
        #for key in curr_factor.fields:
            #curr_factor.fields[key].disabled = True
        ##factor_forms[f].fields['factor_title'].disabled = True
        
    if request.method == 'POST':
        fac_form = FactorForm(request.POST, initial=model_to_dict(fac), instance=fac)
        
        if fac_form.is_valid():
            
            print('CLEANED DATA')
            print(fac_form.cleaned_data)
            
            output = fac_form.save(commit=False)
    else:
        fac_form = FactorForm(initial=model_to_dict(fac), instance=fac)

    context = {'fac': fac,
               'ref': ref,
               'fac_form': fac_form,
               'page_title': 'Edit Factor',
    }
    return render(request, 'cedar_core/factor_detail_new.html', context)


@login_required
@permission_required('cedar_core.add_factor')
def resistance_outcome_detail(request, ref_id, fac_id, prev_ro_id):
    
    ref = reference.objects.get(pk=ref_id)
    fac = factor.objects.get(pk=fac_id)
    
    #Get RO
    try:
        prev_ro = res_outcome.objects.get(pk=prev_ro_id)
    except fac.DoesNotExist:
        raise Http404("Resistance outcome does not exist")

    # New extraction (duplicate) under the same soid
    ro = res_outcome.objects.create(soid=prev_ro.soid, extract_date_ro=timezone.now)
    
    #Set fields to read only (example code just for reference)
    #for f in range(len(factor_forms)):
        #curr_factor = factor_forms[f]
        #for key in curr_factor.fields:
            #curr_factor.fields[key].disabled = True
        ##factor_forms[f].fields['factor_title'].disabled = True
        
    if request.method == 'POST':
        ro_form = ResistanceOutcomeForm(request.POST, initial=model_to_dict(ro), instance=ro)
        
        if ro_form.is_valid():
            
            print('CLEANED DATA')
            print(ro_form.cleaned_data)
            
            output = ro_form.save(commit=False)

    else:
        ro_form = ResistanceOutcomeForm(initial=model_to_dict(ro), instance=ro)

    context = {'ro': ro,
               'ro_form': ro_form,
               'page_title': 'Edit Association with Resistance',
               'ref': ref,
               'fac': fac,
    }
    return render(request, 'cedar_core/resistance_outcome_detail.html', context)
