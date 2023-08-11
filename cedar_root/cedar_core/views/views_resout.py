

from cedar_core.forms import FactorForm, EditResistanceOutcomeForm, ExtractResistanceOutcomeForm
from cedar_core.models import factor, reference, res_outcome
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.views import View
from django.core.exceptions import PermissionDenied
from django.contrib import messages





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

        form = ExtractResistanceOutcomeForm()
        context['form'] = form

        return render(request, 
                      'cedar_core/edit_resistance_outcome.html', 
                      context = context)
    

    elif request.method == 'POST':

        form = ExtractResistanceOutcomeForm(request.POST)

        context['form'] = form

        if form.is_valid():
            form.instance.factor = thisfactor
            form.save()
            messages.success(request, 'The resistance outcome has been saved successfully.')
            return render(request, 'cedar_core/edit_resistance_outcome.html', context = context)
        
        else:
            messages.error(request, 'Please correct the following errors:')
            return render(request, 'cedar_core/edit_resistance_outcome.html', context = context)





def EditReferenceOutcome(request, reference_id, factor_id, pk): # =================================
    #                                                             --------- EDIT RESISTANCE OUTCOME
    # =============================================================================================

    ro = get_object_or_404(res_outcome, pk = pk)

    parent_factor    = factor.objects.all().get(pk = ro.factor_id)
    parent_reference = reference.objects.all().get(pk = parent_factor.reference_id)

    if request.method == 'GET':
        context = {'form': ExtractResistanceOutcomeForm(instance=ro), 
                   'pk': pk, 
                   'resistance_outcome': ro,
                   'factor' : parent_factor, 
                   'reference' : parent_reference,
                   
                   }


        return render(request, 'cedar_core/edit_resistance_outcome.html', context)
    
    elif request.method == 'POST':
        form = ExtractResistanceOutcomeForm(request.POST, instance=ro)

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





class resoutCreateView(LoginRequiredMixin, CreateView):
    
    # Create a ModelForm
    model = res_outcome

    # Set template. CreateView defaults to *_form. 
    template_name = "cedar_core/res_outcome_detail.html"

    # Set template alternate approach: 
    # template_name_suffix = '_detail'

    # Do not specify fields and create a form; select existing (crispy) form. 
    form_class = EditResistanceOutcomeForm

# initial = {'key', 'value'}
    
    # An attempt to use the same form.
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = TestResistanceOutcomeForm()
    #     return context

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['factor'] = self.kwargs['pk']
        return initial






class resoutDetailView(LoginRequiredMixin, DetailView):
    
    model = res_outcome
    template_name = "cedar_core/edit_resistance_outcome.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)
    
    
    # Set the context for the view.
    def get_context_data(self, **kwargs):

        # ?
        context = super().get_context_data(**kwargs)

        # Get parent factor, then parent reference. This cascaded retrieval from 
        # self avoids reliance on reading from context via self.kwargs['URL param'].
        parent_factor    = factor.objects.all().get(pk=self.object.factor_id)
        parent_reference = reference.objects.all().get(pk = parent_factor.reference_id)

        # Set additional context.
        context['form'] = EditResistanceOutcomeForm(initial=model_to_dict(self.object))
        context['resistance_outcome'] = self.object
        context['factor'] = parent_factor
        context['reference'] = parent_reference
        context['page_title'] = "Edit Resistance Outcome"
        return context

   

class resoutUpdateView(LoginRequiredMixin, UpdateView):
    model = res_outcome
    form_class = EditResistanceOutcomeForm
    
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)



class resoutView(View):

    def get(self, request, *args, **kwargs):
        view = resoutDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = resoutUpdateView.as_view()
        return view(request, *args, **kwargs)
    


