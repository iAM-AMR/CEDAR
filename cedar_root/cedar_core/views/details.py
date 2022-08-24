
from multiprocessing import context
from webbrowser import get
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404



from cedar_core.models import reference, reference_join_location, reference_join_reference_note, factor, publisher, res_outcome
from cedar_core.forms  import ReferenceForm, RefLocForm, RefLocFormSet, RefLocFormSetHelper, RefNoteForm, RefNoteFormSet, RefNoteFormSetHelper, QuerySelectForm, TopicTabForm, FactorForm, ResistanceOutcomeForm

from django.forms.models import model_to_dict
from django.db.models import F, Q


from django.utils import timezone

import csv
import numpy as np





from crispy_forms.utils import render_crispy_form


from dal import autocomplete

import re



# =============================================================================
# -------------------------------------------------------------- VIEW REFERENCE
# =============================================================================

@login_required
@permission_required('cedar_core.add_factor')
def edit_reference(request, ref_id):

    # try:
    #     ref = reference.objects.get(pk=ref_id)
    # except ObjectDoesNotExist:
    #     return HttpResponseNotFound('<h1>Page not found</h1>')
    
    # Shortcut
    ref = get_object_or_404(reference, pk=ref_id )

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
               
    return render(request, 'cedar_core/edit_reference.html', context)









def detail_reference(request, ref_id):

    thisreference = get_object_or_404(reference, pk = ref_id)


    context = {'page_title': 'CEDAR: Reference Details',
               'reference': thisreference,
               }

    return render(request, 'cedar_core/detail_reference.html', context)