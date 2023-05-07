

from cedar_core.forms import FactorForm, EditResistanceOutcomeForm, ResistanceOutcomeForm
from cedar_core.models import factor, reference, res_outcome
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.views import View
from django.core.exceptions import PermissionDenied

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



class resoutDeleteView(LoginRequiredMixin, DeleteView):
    model = res_outcome
    success_url = reverse_lazy('index')




class resoutView(View):

    def get(self, request, *args, **kwargs):
        view = resoutDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = resoutUpdateView.as_view()
        return view(request, *args, **kwargs)
    




""" 
def detail_res_outcome(request, reference_id, factor_id, res_outcome_id):

    thisresoutcome = get_object_or_404(res_outcome, pk = res_outcome_id)

    context = {'page_title': 'CEDAR: Outcome ' + str(res_outcome_id),
               'res_outcome': thisresoutcome,
               }

    return render(request, 'cedar_core/detail_res_outcome.html', context)

 """

""" 
@login_required
@permission_required('cedar_core.add_factor')
def resistance_outcome_detail(request, reference_id, factor_id, pk):
    
    ref = reference.objects.get(pk=reference_id)
    fac = factor.objects.get(pk=factor_id)
    
    prev_ro = get_object_or_404(res_outcome, pk = pk)


    # New extraction (duplicate) under the same soid
    #ro = res_outcome.objects.create(id=prev_ro.id)
    
    #Set fields to read only (example code just for reference)
    #for f in range(len(factor_forms)):
        #curr_factor = factor_forms[f]
        #for key in curr_factor.fields:
            #curr_factor.fields[key].disabled = True
        ##factor_forms[f].fields['factor_title'].disabled = True
        
    if request.method == 'POST':
        # ro_form = ResistanceOutcomeForm(request.POST, initial=model_to_dict(prev_ro), instance=ro)
        ro_form = ResistanceOutcomeForm(request.POST, initial=model_to_dict(prev_ro))
        
        if ro_form.is_valid():
            
            print('CLEANED DATA')
            print(ro_form.cleaned_data)
            
            output = ro_form.save(commit=False)

    else:
        ro_form = ResistanceOutcomeForm(initial=model_to_dict(prev_ro), instance=prev_ro)

    context = {'ro': prev_ro,
               'ro_form': ro_form,
               'page_title': 'Edit Association with Resistance',
               'ref': ref,
               'factor': fac,
    }
    return render(request, 'cedar_core/resistance_outcome_detail.html', context)

 """
""" 

@login_required
@permission_required('cedar_core.add_factor')
def edit_resistance_outcome(request, reference_id, factor_id, pk):

    resout = get_object_or_404(res_outcome, pk = pk)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        
        print('Error: REQ is POST')
        # https://docs.djangoproject.com/en/4.1/topics/forms/

    else:
        res_out_form = EditResistanceOutcomeForm()

    context = {
        'page_title': 'Edit RO: ' + str(pk),
        'resistance_outcome': resout,
        'EditResistanceOutcomeForm': res_out_form

    }

    return render(request, 'cedar_core/edit_resistance_outcome.html', context)


 """

""" 
If you wish to have separate templates for CreateView and UpdateView, you can 
set either template_name or template_name_suffix on your view class.


https://docs.djangoproject.com/en/4.1/topics/class-based-views/generic-editing/#model-forms
"""


