

from multiprocessing import context
from webbrowser import get
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from cedar_core.models import reference, reference_join_location, reference_note, factor, publisher, res_outcome
from cedar_core.forms  import ReferenceForm, RefLocForm, RefLocFormSet, RefLocFormSetHelper, RefNoteForm, RefNoteFormSet, RefNoteFormSetHelper, QuerySelectForm, TopicTabForm, FactorForm, ResistanceOutcomeForm, EditResistanceOutcomeForm

from django.forms.models import model_to_dict
from django.db.models import F, Q


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


class resoutCreateView(CreateView):
    model = res_outcome
    fields = ['factor', 'resistance']

class resoutUpdateView(UpdateView):
    model = res_outcome
    fields = ['factor', 'resistance', 'resistance_gene', 'place_in_text', 
                  'microbe_level_01', 'microbe_level_02', 'group_observe_production_stage',
                  'moa_type', 'moa_unit', 'contable_a', 'contable_b', 'contable_c', 'contable_d',
                  'prevtable_a', 'prevtable_b', 'prevtable_c', 'prevtable_d', 'table_n_ab', 'table_n_cd',
                  'odds_ratio', 'odds_ratio_lo', 'odds_ratio_up', 'odds_ratio_sig', 'is_figure_extract',
                  'figure_extract_method', 'extract_user_legacy']



class resoutDeleteView(DeleteView):
    model = res_outcome
    success_url = reverse_lazy('index')