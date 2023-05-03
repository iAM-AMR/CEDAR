from cedar_core.models import reference

import django_filters


class reference_filter(django_filters.FilterSet):
    
    
    MYCHOICE = {

       
        (True, 'Excluded'),
        (False, 'Included')
    }
    
    is_excluded = django_filters.ChoiceFilter(label='Exclusion Status', field_name='is_excluded_extract', choices=MYCHOICE, empty_label='Show All')



    
    class Meta:
        model = reference
        fields = ['is_excluded']