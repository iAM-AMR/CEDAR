
from urllib import request
from django.urls import reverse
from multiprocessing import context
from webbrowser import get
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import DetailView
from django.views import View

from cedar_core.models import reference, reference_join_location, reference_note, factor, publisher, res_outcome
from cedar_core.forms  import ReferenceForm, RefLocForm, RefLocFormSet, RefLocFormSetHelper, RefNoteForm, RefNoteFormSet, RefNoteFormSetHelper, QuerySelectForm, TopicTabForm, FactorForm, ResistanceOutcomeForm, EditResistanceOutcomeForm, TestResistanceOutcomeForm

from django.forms.models import model_to_dict
from django.db.models import F, Q

from cedar_core.forms import TestResistanceOutcomeForm

from django.utils import timezone

import csv
import numpy as np





from crispy_forms.utils import render_crispy_form


from dal import autocomplete

import re



def edit_resistance_outcome(request, reference_id, factor_id, res_outcome_id):

    resout = get_object_or_404(res_outcome, pk = res_outcome_id)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        
        print('Error: REQ is POST')
        # https://docs.djangoproject.com/en/4.1/topics/forms/

    else:
        res_out_form = EditResistanceOutcomeForm()

    context = {
        'page_title': 'Edit RO: ' + str(res_outcome_id),
        'resistance_outcome': resout,
        'EditResistanceOutcomeForm': res_out_form

    }

    return render(request, 'cedar_core/edit_resistance_outcome.html', context)


""" 
If you wish to have separate templates for CreateView and UpdateView, you can 
set either template_name or template_name_suffix on your view class.


https://docs.djangoproject.com/en/4.1/topics/class-based-views/generic-editing/#model-forms
"""






class resoutCreateView(LoginRequiredMixin, CreateView):
    model = res_outcome
    template_name = "cedar_core/res_outcome_detail.html"
    #fields = ['factor', 'resistance', 'moa_type', 'microbe_level_01']

    form_class = TestResistanceOutcomeForm

# initial = {'key', 'value'}
    
    # An attempt to use the same form.
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = TestResistanceOutcomeForm()
    #     return context

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['factor'] = self.kwargs['factor_id']
        return initial




class resoutDetailView(DetailView):
    model = res_outcome

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TestResistanceOutcomeForm(initial=model_to_dict(self.object)) # Missing instance?
        context['resout'] = self.object
        return context

   

    


class resoutUpdateView(UpdateView):
    model = res_outcome
    form_class = TestResistanceOutcomeForm
    
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)



class resoutDeleteView(DeleteView):
    model = res_outcome
    success_url = reverse_lazy('index')


class resoutView(View):

    def get(self, request, *args, **kwargs):
        view = resoutDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = resoutUpdateView.as_view()
        return view(request, *args, **kwargs)