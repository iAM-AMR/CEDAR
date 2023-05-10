

from cedar_core.filters import reference_filter
from cedar_core.forms import (ReferenceForm, RefLocFormSet,
                              RefLocFormSetHelper, RefNoteFormSet,
                              RefNoteFormSetHelper)
from cedar_core.models import factor, reference
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, F
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render





def browse_references(request): # =================================================================
    #                             ----------------------------------------------- BROWSE_REFERENCES
    # =============================================================================================

    """
    Browse CEDAR by reference.
    """
    
    refs_list   = reference.objects.filter(is_archived = False)
    refs_filter = reference_filter(request.GET, queryset=refs_list)
    
    context = {
        'page_title': 'Browse CEDAR by Reference', 
        'refs_list': refs_list,
        'refs_filter': refs_filter, 
        'view_references': 'active',
    }
           
    return render(request, 'cedar_core/browse_references.html', context)





def list_child_factors(request, pk): # ============================================================
    #                                  ----------------------------------------- LIST_CHILD_FACTORS
    # =============================================================================================
    
    """
    Get factors associated with a reference whose ID is passed as pk.
    """

    thisreference = get_object_or_404(reference, pk = pk)
    
    # Get related factors, annotating each factor with the number of associated
    # resistance outcomes. Access via res_outcome__count in template.
    child_factors = thisreference.factor_set.all().annotate(Count('res_outcome'))

    context = {
        'page_title': 'List of Factors',
        'reference':  thisreference,
        'children':   child_factors,
    }

    return render(request, 'cedar_core/list_child_factors.html', context)





def detail_reference(request, pk): # ==============================================================
    #                                --------------------------------------------- DETAIL_REFERENCE
    # =============================================================================================\

    """
    Get the details of a single reference, and list associated factors.
    """

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

