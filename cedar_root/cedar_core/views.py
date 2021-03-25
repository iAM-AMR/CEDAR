from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from crispy_forms.utils import render_crispy_form

from .models import reference, location_join, reference_note, factor, publisher
from .forms import ReferenceForm, RefLocForm, RefNoteForm, FactorForm, RefLocFormSet, RefLocFormSetHelper, RefNoteFormSet, RefNoteFormSetHelper, ConTableForm, PrevTableForm, OddsTableForm, QuerySelectForm

from django.forms.models import model_to_dict, formset_factory, modelformset_factory
from django.urls import reverse
from django.db.models import F, Q

import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from dal import autocomplete

#import json
#from django.core import serializers
#from django.core.serializers.json import DjangoJSONEncoder
#import decimal
#from decimal import Decimal

import re
#from django.views.decorators.csrf import csrf_protect

#@csrf_protect

class PublisherAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return publisher.objects.none()

        qs = publisher.objects.all()

        if self.q:
            qs = qs.filter(pub_title__istartswith=self.q)

        return qs

#def load_subregions(request):
    #country_id = request.GET.get('location_02_id')
    #subregions = location_02.objects.filter(iso_country_code_2_id=country_id)
    #return render(request, '', {'subregions': subregions})


@login_required
def view_references(request):
    
    refs_list = reference.objects.order_by('key_bibtex')
    
    #************************ COMMENTED OUT: CHECKBOX CODE**********************************************
    # If data is incoming from the server, filtering needs to happen based on the checkboxes that have been checked
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
def view_factors(request, ref_id):
    
    try:
        ref = reference.objects.get(pk=ref_id)
    except ref.DoesNotExist:
        raise Http404("Reference does not exist")
    
    ref_factors = ref.factor_set.all()
    
    # **********In progress: Retrieve 2x2 table info (contingency or prevalence)*********************
    
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

def export_query(request):
    
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
            
            # Export all factors if all checkboxes are checked, or if no checkboxes are checked
            if ((not microbes) and (not drugs) and (not host_name)) or (len(microbes) == 4 and len(drugs) == 4):
                query_string = 'factor.objects.all()'
                
            # Otherwise, filter the factors selected for export based on checked checkboxes
            else:
                query_string = 'factor.objects.filter(host_01_id=host_name)'
                if len(drugs) == 0 or len(drugs) == 4: # Filter by host and microbe (all drugs)
                    query_string += '.filter('
                    for mic_count in range(len(microbes)):
                        microbe_id = microbes[mic_count]
                        query_string += 'Q(microbe_01_id=%d)' % (microbe_id)
                        if len(microbes) > 1 and (mic_count < len(microbes)-1):
                            query_string += ' | '
                    query_string += ')'
                elif len(microbes) == 0 or len(microbes) == 4: # Filter by host and drug (all microbes)
                    query_string += '.filter('
                    for drug_count in range(len(drugs)):
                        drug_id = drugs[drug_count]
                        query_string += 'Q(resistance_id__levelname_%s="%s")' % (drug_level, drug_id)
                        if len(drugs) > 1 and (drug_count < len(drugs)-1):
                            query_string += ' | '
                    query_string += ')'
                else: # Filter by host, microbe, and drug
                    
                    # Append microbe filtering
                    query_string += '.filter('
                    for mic_count in range(len(microbes)):
                        microbe_id = microbes[mic_count]
                        query_string += 'Q(microbe_01_id=%d)' % (microbe_id)
                        if len(microbes) > 1 and (mic_count < len(microbes)-1):
                            query_string += ' | '
                    query_string += ')'
                    
                    # Append drug filtering
                    query_string += '.filter('
                    for drug_count in range(len(drugs)):
                        drug_id = drugs[drug_count]
                        query_string += 'Q(resistance_id__levelname_%s="%s")' % (drug_level, drug_id)
                        if len(drugs) > 1 and (drug_count < len(drugs)-1):
                            query_string += ' | '
                    query_string += ')'
            
            print(query_string)
            
            # Perform the filtering to get the desired factors   
            export_facs = eval(query_string)
            
            # Return a pop-up if no factors exist meeting the query criteria
            if len(export_facs) == 0:
                # return popup
                #messages.info(request, 'No factors exist that meet the chosen criteria. Please try broadening your query')
                return render(request, 'cedar_core/export_query.html', {'query_form': QuerySelectForm(), 'page_title': 'Export a Query', 'message_text': 'No factors exist that meet the chosen criteria. Please try broadening your query'})
            
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
            new_raw_dict = model_to_dict(export_facs[0])
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
            for fac in export_facs:
                
                # Get the raw data for the current factor
                raw_fac_dict = model_to_dict(fac)
                
                # Replace ids with values for foreign key fields in the raw data
                raw_fac_dict['resistance_id'] = fac.resistance_id.levelname_5
                raw_fac_dict['host_01_id'] = fac.host_01_id.host_name
                raw_fac_dict['host_02_id'] = fac.host_02_id.host_subtype_name
                raw_fac_dict['microbe_01_id'] = fac.microbe_01_id.microbe_name
                raw_fac_dict['microbe_02_id'] = fac.microbe_02_id.microbe_subtype_name
                raw_fac_dict['prod_stage_group_allocate_id'] = fac.prod_stage_group_allocate_id.stage
                raw_fac_dict['prod_stage_group_observe_id'] = fac.prod_stage_group_observe_id.stage
                raw_fac_dict['moa_type_id'] = fac.moa_type_id.res_format
                raw_fac_dict['moa_unit_id'] = fac.moa_unit_id.res_unit
                
                #print('RAW FACTOR DICTIONARY')
                #print(raw_fac_dict)
                
                # Populate the query_dict with raw data
                for field in timber_header:
                    
                    # Reference-level fields: retrieve the values
                    if field in ref_fields:
                        query_dict[field] = eval("fac.factor_ref_id.%s" % (field))
                    # Factor-level fields: retrieve the values from raw data
                    elif field not in null_fields:
                        old_field = field_match_dict[field]
                        query_dict[field] = raw_fac_dict[old_field] # raw dictionary is indexed by the old names
            
                # Write row to CSV
                writer.writerow(list(query_dict.values()))
            return response
        else:
            print('QUERY FORM NOT VALID')
    else:
        query_form = QuerySelectForm()
    
    context = {'query_form': query_form, 'page_title': 'Export a Query'}
    return render(request, 'cedar_core/export_query.html', context)

@login_required
def expand_factor(request, ref_id, fac_id):
    
    ref = reference.objects.get(pk=ref_id)
    ref_factors = ref.factor_set.all()
    main_fac = factor.objects.get(id=fac_id)
    result_type = factor._meta.get_field('moa_type_id').value_from_object(main_fac)
    
    if request.method == 'POST':
        # Create the appropriate factor data form depending on the result type. TO DO: account for Relative Risk
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
        # Create the appropriate factor data form depending on the result type. TO DO: account for Relative Risk
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

@login_required
def delete_factor(request, ref_id, fac_id):
    
    # Delete the factor
    del_fac = factor.objects.get(id=fac_id)
    del_fac.delete()
    
    # Reload the view factors page
    ref = reference.objects.get(pk=ref_id)
    ref_factors = ref.factor_set.all()
    
    context = {
        'ref': ref,
        'ref_factors': ref_factors,
    }
    
    return redirect('/cedar_core/references/' + str(ref_id) + '/factors/')
    #return render(request,'cedar_core/view_factors.html', context)

@login_required
def ref_detail(request, ref_id):

    try:
        ref = reference.objects.get(pk=ref_id)
    except ref.DoesNotExist:
        raise Http404("Reference does not exist")

    #Get dictionary of field names mapped to current values
    #state = ref.__dict__
    #exclude_key = ['_state']
    #init_vals = {k: state[k] for k in set(list(state.keys())) - set(exclude_key)}
    
    # If this is a POST request, process the form data
    if request.method == 'POST':
        print('POST ENTERED')
        
        # Create form instances and populate them with data from the request
        
        # Main and Study Design tabs
        ref_form = ReferenceForm(request.POST, initial=model_to_dict(ref), instance=ref)
        
        # Location tab
        ref_locs = ref.location_join_set.all().order_by(F('location_01_id').asc(nulls_first=True))
        loc_formset = RefLocFormSet(request.POST, instance=ref)
        loc_helper = RefLocFormSetHelper()
        #RefLocFormSet = modelformset_factory(location_join, form=RefLocForm, fields=('location_01', 'location_02', 'ref_loc_note'), extra=0)
        #loc_formset = RefLocFormSet(request.POST, queryset=ref_locs)
        
        # Notes and Issues tab
        ref_notes = ref.reference_note_set.all()
        note_formset = RefNoteFormSet(request.POST, instance=ref)
        note_helper = RefNoteFormSetHelper()
        
        # Save ref form if valid
        if ref_form.is_valid():
            #process the data in form.cleaned_data as required (i.e. save to database, etc.)
            #...
            print('ENTERED VALID')
            print(ref_form.cleaned_data)
            print('CLEANED DATA')
            
            output = ref_form.save() #save changes to the database

            print('SAVED FORM')
            print(output)
            
            #redirect to a new URL:
            #return HttpResponseRedirect(reverse('add_ref_success'))
        else:
            print('REF FORM NOT VALID')

        # Save notes and issues form set if valid
        if note_formset.is_valid():
            print('NOTE FORMSET IS VALID')
            note_formset.save()
            print(note_formset.cleaned_data)
        else:
            print('NOTE FORMSET NOT VALID')
        
        # Save location form set if valid
        if loc_formset.is_valid():
            print('LOC FORMSET IS VALID')
            for f in loc_formset:
                print(f.cleaned_data)
            loc_formset.save()
        else:
            print('LOC FORMSET NOT VALID')
            for f in loc_formset:
                print(f.cleaned_data)
            print(loc_formset.errors)
        
        # OLD: Save location form if valid
        #if all(loc.is_valid() for loc in loc_forms):
            #process the data in form.cleaned_data as required (i.e. save to database, etc.)
            #...
            
            #for loc in loc_forms:
                #loc.save(commit=False)
                #print('SAVE LOCATION')
                #print(loc.cleaned_data)

            #redirect to a new URL:
            #return HttpResponseRedirect(reverse('add_ref_success'))
        #else:
            #print('LOCATION FORM NOT VALID')

    # If request is a GET (or any other method) we'll create a blank form for each tab (pre-populated with fields that are not empty)
    else:
        ref_form = ReferenceForm(initial=model_to_dict(ref), instance=ref)
        
        # Location
        ref_locs = ref.location_join_set.all().order_by(F('location_01_id').asc(nulls_first=True))
        loc_formset = RefLocFormSet(instance=ref)
        loc_helper = RefLocFormSetHelper()
        
        # Notes
        ref_notes = ref.reference_note_set.all()
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

# Add either a new reference note, or a new location
@login_required
def add_ref_info(request, ref_id, form_type):
    
    # Get reference object
    ref = reference.objects.get(pk=ref_id)
    
    # Create a new object linked to this reference
    #new_loc = location_join.objects.create(reference = ref)
    if form_type == 'loc':
        new_obj = location_join(loc_ref_id = ref)
        redir_path = '/cedar_core/references/' + str(ref_id) + '/#loc-md'
    else:
        new_obj = reference_note(note_ref_id = ref)
        redir_path = '/cedar_core/references/' + str(ref_id) + '/#notes-md'
    
    # Save new object and redirect
    new_obj.save()
    
    return redirect(redir_path)

@login_required
def factor_detail(request, ref_id, fac_id):
    
    ref = reference.objects.get(pk=ref_id)
    
    #Get factor
    try:
        fac = factor.objects.get(pk=fac_id)
    except fac.DoesNotExist:
        raise Http404("Factor does not exist")
    
    #Set fields to read only
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
            
            output = fac_form.save()

    else:
        fac_form = FactorForm(initial=model_to_dict(fac), instance=fac)

    context = {'fac': fac,
               'fac_form': fac_form,
               'page_title': 'Edit Factor',
    }
    return render(request, 'cedar_core/factor_detail_new.html', context)
