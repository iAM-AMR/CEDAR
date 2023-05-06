
"""
The filters.py file enables django_filters.
"""

import django_filters
from cedar_core.models import (host_01, microbe_01, reference, res_outcome)





class reference_filter(django_filters.FilterSet):
    
    """
    Filter references shown at Browse References.
    """

    # By default for a Boolean, django-filter displays a drop-down with 
    # "Unknown", "True", and 'False'. To customize these choices, we 
    # must manually define a choice mapping, and specify a ChoiceFilter. 
    # The null value is specified in the ChoiceFilter.

    THECHOICES = {
        (True, 'Excluded'),
        (False, 'Included')
    }
    
    is_excluded = django_filters.ChoiceFilter(
        label='Exclusion Status', 
        field_name='is_excluded_extract', 
        choices=THECHOICES, 
        empty_label='Show All')

    class Meta:
        model = reference
        fields = ['is_excluded']





class timber_filter(django_filters.FilterSet):
    
    """
    Filter resistance outcomes in 'get_timber'.
    """

    # Unclear if this is the best implementation. Also unlear if queryset target is appropriate.
    host    = django_filters.ModelMultipleChoiceFilter(field_name = 'factor__host_level_01__host_01_name', 
                                                       queryset=host_01.objects.all(), 
                                                       label = "Host",)
    
    # Unclear if this is the best implementation. Also unlear if queryset target is appropriate.
    microbe = django_filters.ModelMultipleChoiceFilter(field_name = 'microbe_level_01__microbe_01_name', 
                                                       queryset=microbe_01.objects.all(), 
                                                       label = "Microbe",)
    
    
    # MultipleChoiceFilter() requires a choice list structured as (value, 'label').
    # We generate a choice list based on the contents of res_outcomes, rather than 
    # the full atc_vet list, to avoid cluttering the UI with unavailable choices.
    # The simplest way to generate this list structure is to pass the same field 
    # name twice.

    resistance_class_choices = res_outcome.objects.distinct('resistance__levelname_4_coarse').values_list('resistance__levelname_4_coarse', 'resistance__levelname_4_coarse')

    resistance_class         = django_filters.MultipleChoiceFilter(field_name = 'resistance__levelname_4_coarse', 
                                                                   label      = 'Resistance Class',
                                                                   choices    = resistance_class_choices,)
    
    resistance_choices       = res_outcome.objects.distinct('resistance__levelname_5').values_list('resistance__levelname_5', 'resistance__levelname_5')
    
    resistance               = django_filters.MultipleChoiceFilter(field_name = 'resistance__levelname_5', 
                                                                   label      = 'Resistance',
                                                                   choices    = resistance_choices,)


    class Meta:
        model = res_outcome
        fields = ['host', 'microbe', 'resistance_class', 'resistance']




