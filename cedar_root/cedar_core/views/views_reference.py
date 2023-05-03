
import csv
import re
from multiprocessing import context
from webbrowser import get

import numpy as np
from cedar_core.forms import (FactorForm, QuerySelectForm, ReferenceForm,
                              RefLocForm, RefLocFormSet, RefLocFormSetHelper,
                              RefNoteForm, RefNoteFormSet,
                              RefNoteFormSetHelper, ResistanceOutcomeForm,
                              TopicTabForm)
from cedar_core.models import (factor, publisher, reference,
                               reference_join_location, reference_note,
                               res_outcome)
from crispy_forms.utils import render_crispy_form
from dal import autocomplete
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q
from django.forms.models import model_to_dict
from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from cedar_core.filters import reference_filter


#@login_required
#@permission_required('cedar_core.add_factor') # this permission check serves to verify that the logged in user is part of the "Edit" permissions group
def browse_references(request):
    
    refs_list = reference.objects.filter(is_archived = False)
    
    refs_filter = reference_filter(request.GET, queryset=refs_list)
    


    context = {'refs_list': refs_list,
               'refs_filter': refs_filter, 
               'page_title': 'CEDAR: Browse References', 
               'view_references': 'active'}

               
    return render(request, 'cedar_core/browse_references.html', context)



def detail_reference(request, pk):
# Get the details of a single reference, and list associated factors.

    thisreference = get_object_or_404(reference, pk = pk)
   
    # Reverse Related Object Lookup
    factor_list = thisreference.factor_set.all()

    location_list = thisreference.reference_join_location_set.all()

    notes_list = thisreference.reference_note_set.all()

    context = {'page_title': 'CEDAR: Reference ' + str(pk),
               'reference': thisreference,
               'reference_factors': factor_list,
               'reference_locations': location_list,
               'reference_notes': notes_list,
               }

    return render(request, 'cedar_core/detail_reference.html', context)





@login_required
@permission_required('cedar_core.add_factor')
def edit_reference_factor_list(request, pk):
    
    try:
        ref = reference.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    # Reverse Related Object Lookup
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
    return render(request, 'cedar_core/edit_reference_factor_list.html', context)















@login_required
@permission_required('cedar_core.add_factor')
def edit_reference(request, pk):

    ref = get_object_or_404(reference, pk = pk )

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
        ref_notes = ref.reference_note_set.all()
        note_formset = RefNoteFormSet(request.POST, instance=ref)
        note_helper = RefNoteFormSetHelper()
        
        # Save ref form if valid (and output checks to the console)
        if ref_form.is_valid():

            #process the data in form.cleaned_data as required (i.e. save to database, etc.)
            #...
            print(ref_form.cleaned_data) # need this line as ref_form.cleaned_data must be called before ref_form.save()
            print('CLEANED DATA')
            

            # Changes wouldn't save without swap to commit=TRUE.
            # CP's approach was defending agaisnt something...
            # https://www.django-antipatterns.com/antipattern/using-commit-false-when-altering-the-instance-in-a-modelform.html
            ref_form.save() #save changes to the database

            print('SAVED FORM')
            #print(output)
            
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
               
    return render(request, 'cedar_core/edit_reference.html', context)

