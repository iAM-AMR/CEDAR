
from cedar_core.models import reference, res_outcome, host_01

import django_filters



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
    Filter references shown during timber query.
    """

    # By default for a Boolean, django-filter displays a drop-down with 
    # "Unknown", "True", and 'False'. To customize these choices, we 
    # must manually define a choice mapping, and specify a ChoiceFilter. 
    # The null value is specified in the ChoiceFilter.

    
    
    host = django_filters.ModelMultipleChoiceFilter(field_name = 'factor__host_level_01__host_01_name', queryset=host_01.objects.all())


    class Meta:
        model = res_outcome
        fields = ['microbe_level_01', 'host']

        