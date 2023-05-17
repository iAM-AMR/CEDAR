

from cedar_core.forms import FactorForm
from cedar_core.models import factor, reference, res_outcome
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect

from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect)

# --------------------------------------------------------------- detail_factor





def browse_factors(request): # ====================================================================
    #                          --------------------------------------------------------------------
    # =============================================================================================

    """
    Browse CEDAR by Factor.
    """

    # Use values with fields here to ensure the parent reference's ID is 
    # available; calling .reference passes the object not the value.

    factor_list = factor.objects.all().values(
        'id',
        'factor_title',
        'reference__id',
    )

    context = {
        'page_title': 'Browse CEDAR by Factor',
        'factor_list': factor_list,
    }

    return render(request, 'cedar_core/browse_factors.html', context)



@login_required
@permission_required('cedar_core.add_factor')

def delete_factor(request, pk):
    
    factor.objects.get(id=pk).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))






def detail_factor(request, reference_id, pk): # ===================================================
    #                                           ------------------------------------- DETAIL_FACTOR
    # =============================================================================================

    """ View factor details

    View factor data, parent reference, and child resistance outcome(s). 
    """
    
    # Get factor through pk variable, using shortcut pk to factor's primary key.
    thisfactor = get_object_or_404(factor, pk = pk)

    # <<  reference_id >> is not used here; parent reference is got through 
    # relationship.
    thisreference = get_object_or_404(reference, pk = thisfactor.reference_id)

    # Get resistance outcomes.
    resistance_outcomes = thisfactor.res_outcome_set.all()

    # Define page title.
    page_title = 'CDR: Factor ' + str(thisfactor.id)


    context = {
        'page_title': page_title,
        'factor': thisfactor,
        'reference': thisreference,
        'resistance_outcomes': resistance_outcomes,
        }

    return render(request, 'cedar_core/detail_factor.html', context)







@login_required
@permission_required('cedar_core.add_factor')

def edit_factor(request, reference_id, pk):
    
    ref = get_object_or_404(reference, pk = reference_id)
    fac = get_object_or_404(factor, pk = pk)
    
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
    return render(request, 'cedar_core/edit_factor.html', context)





def list_child_resistance_outcomes(request, reference_id, pk):

    thisfactor    = get_object_or_404(factor,    pk = pk)
    thisreference = get_object_or_404(reference, pk = reference_id)

    # TODO: Remove reliance on reference_id.
    
    resistance_outcomes = thisfactor.res_outcome_set.all()
    
    context = {
        'factor': thisfactor,
        'reference': thisreference,
        'resistance_outcomes': resistance_outcomes,
        'page_title': 'List ROs for Factor ' + str(pk),
    }
    return render(request, 'cedar_core/list_child_resistance_outcomes.html', context)

