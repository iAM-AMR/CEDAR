
from cedar_core.models import reference, res_outcome, host_01, microbe_01

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
    Filter resistance outcomes in 'get_timber'.
    """

    # Unclear if this is the best implementation. Also unlear if queryset target is appropriate.
    host = django_filters.ModelMultipleChoiceFilter(field_name = 'factor__host_level_01__host_01_name', 
                                                    queryset=host_01.objects.all(), 
                                                    label = "Host",
                                                    )
    
    # Unclear if this is the best implementation. Also unlear if queryset target is appropriate.
    microbe = django_filters.ModelMultipleChoiceFilter(field_name = 'microbe_level_01__microbe_01_name', 
                                                       queryset=microbe_01.objects.all(), 
                                                       label = "Microbe")

    class Meta:
        model = res_outcome
        fields = ['host', 'microbe']


