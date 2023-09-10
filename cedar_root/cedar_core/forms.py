from django.forms import ModelForm, TextInput
from django import forms
from cedar_core.models import factor, reference, reference_join_location, reference_note, res_outcome, location_01, location_02, host_01, microbe_01, atc_vet
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy

from crispy_forms.bootstrap import Tab, TabHolder, FormActions, PrependedText, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, ButtonHolder, Row, Column, HTML, Field
from crispy_forms.utils import render_crispy_form

from django.forms.models import modelformset_factory, inlineformset_factory

from dal import autocomplete

#class NewFactorForm(modelForm):
    #class Meta:
        #model = factor
        #fields = ['factor_title', 'factor_description']

class ReferenceForm(ModelForm):
    class Meta:
        model = reference
        fields = ['ref_title','ref_author', 'publish_year', 'publisher', 'publish_doi', 'publish_pmid', 
                  'is_excluded_extract','excluded_extract_reason', 'study_design', 'study_design_detail',
                  'study_sample_method', 'ref_ast_method', 'ref_has_ast_explicit_break', 'ref_has_ast_mic_table']
        widgets = {
            'publisher': autocomplete.ModelSelect2(url='publish-id-autocomplete'),
            'ref_title': forms.TextInput(),
            'ref_author': forms.TextInput(),
            'is_excluded_extract': forms.CheckboxInput(),
        }


        
        # Replaced by prepended text below
        #labels = {
            #'ref_title': 'Title',
            #'name_author': 'Author Name(s)',
            #'publication_year': 'Publication Year',
            #'ident_doi': 'DOI:',
            #'ident_pmid': 'PMID:',
            #'exclude_extraction': 'Exclude from Extraction?',
            #'exclude_extraction_reason': 'Reason for Exclusion:',
            #'study_design': 'Study Design:',
            #'study_design_detail': 'Design Detail:',
            #'study_sample_method': 'Sampling Method:',
            #'ast_method': 'AST Method',
            #'has_breakpoint': 'Has Explicit Breakpoints?',
            #'has_mic_table': 'Has MIC Table?'
        #}
        
        # Hides help text: commented out for now
        #help_texts = {}
        #for fieldname in fields:
            #help_texts[fieldname] = None
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #Create FormHelper from crispy forms for layout
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False

        #can have class='sr-only' to hide labels
        #but how to add w/in Layout?

        self.helper.layout = Layout(
            #Main tab
            Div(
                Column(
                  
                    Div(
                        Row(
                            Column(
                                PrependedText('ref_title', 'ref_title', placeholder="Study Title"),
                                ccs_class='col-md-6',
                            ),
                            Column(
                                PrependedText('ref_author', 'ref_author', placeholder="Author Name(s) Here"),
                                ccs_class='col-md-6',
                            )
                        ),

                        Row(
                            Column(
                                PrependedText('publish_year', 'Pub. Year', placeholder="Publication Year Here"),
                                css_class='col-md-2'
                            ),
                            Column(
                                PrependedText('publisher', 'Publisher', placeholder="Publisher Here"), #form-text styles oddly
                                css_class='col-md-6 align-content-lg-stretch' 
                            ),
                            Column(
                                PrependedText('publish_doi', 'DOI:', placeholder="DOI Here"),
                                css_class='col-md-4'
                            ),
                        ),

                        Row(
                            Column(

                                # The checkbox will not display if "Prepend Text" is used.

                                HTML("""
                                <p>Is the reference excluded?</p>
                                """),
                                'is_excluded_extract',
                                css_class='col-md-2'
                            ), 

                            Column(
                                PrependedText('excluded_extract_reason', 'Is Excluded Because:', placeholder="Reason Here"),
                                css_class='col-md-10'
                            ),
                        ),
                            #HTML(
                                #""" <style>
                                        #.row{
                                            #overflow: hidden; 
                                        #}

                                        #[class*="col-"]{
                                            #margin-bottom: -99999px;
                                            #padding-bottom: 99999px;
                                        #}
                                    #</style> """
                            #),
                            #css_class = 'd-flex flex-row',

                    ),
                    
                    FormActions(
                        Submit('save', 'Save changes')
                    ),
                ),
                css_id='tab-1-main',
                css_class='tab-pane fade show active',
            ),
            #Study Design tab
            Div(
                Column(
                  
                    PrependedText('study_design', 'Study Design:'),
                    PrependedText('study_design_detail', 'Design Detail:'), 
                    PrependedText('study_sample_method', 'Sampling Method:'), 
                    HTML(
                        """<h6>AST:</h6> <hr>"""
                    ),
                    Row(  
                        Column(PrependedText('ref_ast_method', 'AST Method'), css_class='form-group col-md-4 mx-0'),
                        Column(PrependedText('ref_has_ast_explicit_break', 'Has Explicit Breakpoints?'), css_class='form-group col-md-4 mb-0'),
                        Column(PrependedText('ref_has_ast_mic_table', 'Has MIC Table?'), css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'
                    ),
                ),    
                FormActions(
                    Submit('save', 'Save changes')
                ),
                css_id='tab-2-study',
                css_class='tab-pane fade',
            ),
        )
   
class RefLocForm(ModelForm):
    class Meta:
        model = reference_join_location
        fields = ['location_main_id', 'location_sub_id', 'location_detail']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.form_show_descriptions = False

class RefLocFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_tag = False
        self.form_show_labels = False
        self.form_show_descriptions = False
        self.layout = Layout(
            Div(
                Column(
                    PrependedText('location_main_id', 'Country'),
                    HTML("""<br>"""),
                    Column(
                        Column(
                            Row(
                                Column(
                                    PrependedText('location_sub_id', 'Region:'),
                                    'location_detail',
                                    css_class='form-group col-md-8 mx-0'
                                ),
                                #Column('note', css_class='form-group col-md-8 mx-0'),
                                css_class='form-row'
                            ),
                        ),
                    ),
                    FormActions(
                        Submit('save', 'Save changes', style="margin-left: -10px;")
                    ),
                    HTML("""<hr style="border-width:5px;">""")
                ),
                css_id='loc-md',
                css_class='tab-pane fade show active',
            ),
        )
RefLocFormSet = inlineformset_factory(reference, reference_join_location, form=RefLocForm, extra=0, can_delete=True)

class RefNoteForm(ModelForm):
    class Meta:
        model = reference_note
        fields = ['reference_note', 'user', 'is_resolved']
        #labels = {
            #'resolved': 'is_resolved?',
        #}
        help_texts = {}
        for fieldname in fields:
            if fieldname != 'reference_note':
                help_texts[fieldname] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_descriptions = False

class RefNoteFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.form_tag = False
        self.form_show_labels = False
        self.form_show_descriptions = False
        self.layout = Layout(
            Div(
                Column(
                    Row(
                        Column(PrependedText('user', 'User'), css_class='form-group col-md-8 mx-0'),
                        Column(PrependedText('is_resolved', 'Resolved?', css_class='ml-2 mt-2'), css_class='form-group col-md-4 mx-0'),
                        css_class='form-row'
                    ),
                    Field('reference_note', css_class='col-md-9'),
                    FormActions(
                        Submit('save', 'Save changes', style="margin-left: 0px;")
                    ),
                    HTML("""<hr style="border-width:5px;">"""),
                ),
                css_id='notes-md',
                css_class='tab-pane fade show active',
            ),
        )
        
RefNoteFormSet = inlineformset_factory(reference, reference_note, form=RefNoteForm, extra=0, can_delete=True)

class TopicTabForm(forms.Form):
    
    #hosts = list(host_01.objects.values_list('host_name', flat=True))
    #microbes = list(microbe_01.objects.values_list('microbe_name', flat=True))
    
    MICROBE_CHOICES = [
        (1, 'Campylobacter'),
        (2, 'Escherichia coli'),
        (3, 'Salmonella'),
        (4, 'Enterococcus'),
    ]
    
    HOST_CHOICES = [
        (1, 'Chicken'),
        (2, 'Swine'),
        (3, 'Turkey'),
        (4, 'Cattle'),
    ]
    
    microbes = forms.MultipleChoiceField(choices=MICROBE_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    hosts = forms.MultipleChoiceField(choices=HOST_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)

    #class Meta:
        #model = factor
        #fields = ['host_01', 'microbe_01', 'resistance']
        #help_texts = {}
        #for fieldname in fields:
            #help_texts[fieldname] = None
        #labels = {
            #'hosts': 'Host',
            #'microbes': 'Microbes',
            #'am_classes': 'Antimicrobial Classes',
        #}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            HTML(''' <h5>Hosts</h5> '''),
            'hosts',
            HTML(''' <h5>Microbes</h5> '''),
            'microbes',
            FormActions(
                Submit('save', 'Export query')
            ),
        )


class FactorForm(ModelForm):
    
    class Meta:
        model = factor

        fields = ['factor_title', 'factor_description', 'host_level_01', 'host_level_02', 'group_allocate_production_stage',
                    'group_factor', 'group_comparator']

        widgets = {
             'factor_title': TextInput(),
            'host_level_02': autocomplete.ModelSelect2(url='host-two-autocomplete', 
                                                      forward=['host_level_01'])

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        # Potential code in case you would like to exclude labels from showing up on the page
        # one alternative
        #to_exclude = ['host_level_01']
        #for i in range(0,len(to_exclude)-1):
            #self.fields[to_exclude[i]].label = False
        
        # another alternative
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                Div(
                    PrependedText('factor_title', 'Title'),
                    PrependedText('factor_description', 'Description'), 
                    css_class='form-horizontal'
                ),
                HTML('''<hr style="border-width:5px;">'''),
                HTML(''' <br> '''),
                Row(
                    Column(
                        Row(
                            PrependedText('host_level_01', 'Host'),
                            'host_level_02',
                        ),
                        css_class='col-md-5 ml-1',
                    ),
                ),
                HTML('''<br>'''),
                Row(
                    Column(
                        'group_allocate_production_stage',
                        css_class='col-md-4',
                    ),
                ),
                HTML('''<hr style="border-width:5px;">'''),
                HTML(''' <br> '''),
                Div(
                    PrependedText('group_factor', 'Factor Group'),
                    PrependedText('group_comparator', 'Comparator Group'), 
                    css_class='form-horizontal'
                ),
                FormActions(
                    Submit('submit', 'Save changes')
                ),
            ),
        )





class editResistanceOutcomeForm(ModelForm): # ==================================================
    #                                            ------------------------------- RESISTANCE OUTCOME
    # =============================================================================================

    """
    Edit a resistance outcome.
    This form replaces earlier versions, where layout was specified via crispy forms helper.
    """

    # Use tooltips to display help text.
    """ 
        def __init__(self, *args, **kwargs):
        super(editResistanceOutcomeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-bs-toggle':"tooltip", 'data-placement':'top', 'data-bs-title':help_text}) 
    """


    class Meta:
        model = res_outcome
        fields = ['resistance', 'resistance_gene', 'microbe_level_01', 'microbe_level_02', 
                  'group_observe_production_stage', 'moa_type', 'moa_unit', 'place_in_text',
                  'contable_a' , 'contable_b' , 'contable_c' , 'contable_d' , 
                  'prevtable_a', 'prevtable_b', 'prevtable_c', 'prevtable_d', 
                  'table_n_ab', 'table_n_cd', 'odds_ratio', 'odds_ratio_lo', 'odds_ratio_up', 
                  'odds_ratio_sig', 'odds_ratio_confidence', 'ast_method', 
                  'ast_reference_standard', 'ast_breakpoint_version', 'ast_breakpoint_is_explicit', 
                  'is_figure_extract', 'figure_extract_method', 'figure_extract_reproducible']
        
        widgets = {
            'place_in_text': TextInput(), 

            'microbe_level_02': autocomplete.ModelSelect2(url='microbe-two-autocomplete', 
                                                          forward=['microbe_level_01'])

        }