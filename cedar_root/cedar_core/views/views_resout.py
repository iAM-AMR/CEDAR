

from cedar_core.forms import editResistanceOutcomeForm
from cedar_core.models import factor, reference, res_outcome
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView





@login_required
def createResistanceOutcome(request, reference_id, pk): # =========================================
    #                                                     --------------- CREATE RESISTANCE OUTCOME
    # =============================================================================================

    thisfactor       = get_object_or_404(factor, pk = pk)
    parent_reference = reference.objects.all().get(pk = thisfactor.reference_id)

    context = {
        'pk'        : pk, 
        'factor'    : thisfactor, 
        'reference' : parent_reference,
        'is_create' : True,
        }


    if request.method == 'GET':

        form = editResistanceOutcomeForm()
        context['form'] = form

        return render(request, 
                      'cedar_core/edit_resistance_outcome.html', 
                      context = context)
    

    elif request.method == 'POST':

        form = editResistanceOutcomeForm(request.POST)

        context['form'] = form

        if form.is_valid():
            form.instance.factor = thisfactor
            form.save()
            messages.success(request, 'The resistance outcome has been saved successfully.')
            return render(request, 'cedar_core/edit_resistance_outcome.html', context = context)
        
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'cedar_core/edit_resistance_outcome.html', context = context)





@login_required
def EditReferenceOutcome(request, reference_id, factor_id, pk): # =================================
    #                                                             --------- EDIT RESISTANCE OUTCOME
    # =============================================================================================

    ro = get_object_or_404(res_outcome, pk = pk)

    parent_factor    = factor.objects.all().get(pk = ro.factor_id)
    parent_reference = reference.objects.all().get(pk = parent_factor.reference_id)

    if request.method == 'GET':
        context = {'form': editResistanceOutcomeForm(instance=ro), 
                   'pk': pk, 
                   'resistance_outcome': ro,
                   'factor' : parent_factor, 
                   'reference' : parent_reference,
                   
                   }


        return render(request, 'cedar_core/edit_resistance_outcome.html', context)
    
    elif request.method == 'POST':
        form = editResistanceOutcomeForm(request.POST, instance=ro)

        post_context = {'pk': pk, 
                        'form': form,
                        'factor' : parent_factor,
                        'reference' : parent_reference,}

        if form.is_valid():
            form.save()
            messages.success(request, 'The resistance outcome has been saved successfully.')
            return render(request, 'cedar_core/edit_resistance_outcome.html', context=post_context)
        
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'cedar_core/edit_resistance_outcome.html', post_context)





class resoutDeleteView(LoginRequiredMixin, DeleteView): # =========================================
    #                                                     --------------- DELETE RESISTANCE OUTCOME
    # =============================================================================================

    # This is a class-based delete view.
    # https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/#deleteview
    # Where request = GET, display a confirmation page at <model>_confirm_delete.html.
    # Where request = POST, delete object without confirmation.

    # Here, we do not use the confirmation page. Rather, we use a bootstrap 
    # confirmation modal with jQuery that POSTs. We override get_success_url()
    # rather than specifying success_url to access object (inherited from 
    # SingleObjectMixin). Alternatively, we could use get_context_data() to 
    # get kwargs. 

    # Alternatively, we could use a function-based delete view, as implemented
    # for factor deletion.

    model = res_outcome

    def get_success_url(self):
        thisfactor = self.object.factor
        return reverse_lazy('list_child_resistance_outcomes', 
                            kwargs={'reference_id': thisfactor.reference.id, 'pk': thisfactor.id})

