

from cedar_core.forms import FactorForm
from cedar_core.models import factor, reference, res_outcome
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect

# --------------------------------------------------------------- detail_factor





def browse_factors(request):

    factor_list = factor.objects.all().values(
        'id',
        'factor_title',
        'reference__id',
    )

    context = {'page_title': 'CEDAR: Browse Factors',
               'navbar_status': 'active', 
               'factor_list': factor_list,
               }

    return render(request, 'cedar_core/browse_factors.html', context)



@login_required
@permission_required('cedar_core.add_factor')
def delete_factor(request, reference_id, pk):
    
    # Delete the factor
    del_fac = factor.objects.get(id=pk)
    del_fac.delete(commit=False)
    
    # Reload the view factors page
    ref = reference.objects.get(pk=reference_id)
    ref_factors = ref.factor_set.all()
    
    context = {
        'ref': ref,
        'ref_factors': ref_factors,
    }
    
    return redirect('/cedar_core/references/' + str(reference_id) + '/factors/')





def detail_factor(request, reference_id, pk):

    thisfactor = get_object_or_404(factor, pk = pk)

    thisreference = get_object_or_404(reference, pk = reference_id)

    resistance_outcome_list = thisfactor.res_outcome_set.all()

    context = {'page_title': 'CEDAR: Factor ' + str(pk),
               'navstatus_factors': 'active', 
               'factor': thisfactor,
               'reference': thisreference,
               'resistance_outcomes': resistance_outcome_list,
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





#@login_required
#@permission_required('cedar_core.add_factor')
def list_resistance_outcomes(request, reference_id, pk):

    thisfactor    = get_object_or_404(factor,    pk = pk)
    thisreference = get_object_or_404(reference, pk = reference_id)
    
    resistance_outcomes = thisfactor.res_outcome_set.all()
    
    context = {
        'factor': thisfactor,
        'reference': thisreference,
        'resistance_outcomes': resistance_outcomes,
        'page_title': 'List ROs for Factor ' + str(pk),
    }
    return render(request, 'cedar_core/list_resistance_outcomes.html', context)

