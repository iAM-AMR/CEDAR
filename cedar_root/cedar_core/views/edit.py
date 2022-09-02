

from multiprocessing import context
from webbrowser import get
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404



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