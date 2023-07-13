from django.forms import ModelForm
from django import forms
from cedar_core.models import factor, reference, reference_join_location, reference_note, res_outcome, location_01, location_02, host_01, microbe_01, atc_vet, dict_help, dict_capt
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
                                PrependedText('ref_title', dict_capt['ref_title'], placeholder="Study Title"),
                                ccs_class='col-md-6',
                            ),
                            Column(
                                PrependedText('ref_author', dict_capt['ref_author'], placeholder="Author Name(s) Here"),
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

class QuerySelectForm(forms.Form):
    
    AM_CLASS_CHOICES = [
        ('Fluoroquinolones', 'Fluoroquinolones'),
        ('Macrolides', 'Macrolides'),
        ('Third-generation cephalosporins', 'Third-generation cephalosporins'),
        ('Tetracyclines', 'Tetracyclines'),
    ]
    
    AM_CHOICES = [
        ('ciprofloxacin', 'ciprofloxacin'),
        ('ceftiofur', 'ceftiofur'),
        ('gentamicin', 'gentamicin'),
        ('oxytetracycline', 'oxytetracycline')
    ]
    
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
    
    am_classes = forms.MultipleChoiceField(choices=AM_CLASS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False) # can change these to be querysets instead of manually defining options
    ams = forms.MultipleChoiceField(choices=AM_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    microbes = forms.MultipleChoiceField(choices=MICROBE_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    hosts = forms.MultipleChoiceField(choices=HOST_CHOICES)

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
            HTML(''' <h5>Host</h5> '''),
            'hosts',
            HTML(''' <h5>Microbes</h5> '''),
            'microbes',
            HTML(''' <h5>Antimicrobial Classes</h5> '''),
            'am_classes',
            HTML(''' <h5>Specific Antimicrobial(s)</h5> '''),
            'ams',
            FormActions(
                Submit('save', 'Export query')
            ),
        )

class FactorForm(ModelForm):
    class Meta:
        model = factor

        fields = ['factor_title', 'factor_description', 'host_level_01', 'host_level_02', 'group_allocate_production_stage',
                    'group_factor', 'group_comparator']
        help_texts = {}

        labels = {
            'factor_title': '',
            'factor_description': '',
            'host_level_01': '',
            'host_level_02': '',
            'group_allocate_production_stage': 'Stage of Factor Application or Presence',
            'group_factor': '',
            'group_comparator': '',
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
        #self.helper.form_show_labels = False

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
                    Submit('save', 'Save changes')
                ),
            ),
        )










class EditResistanceOutcomeForm(ModelForm):
    
    class Meta:
        model = res_outcome
        exclude = ['']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = ''
        self.helper.form_class = 'res-out-detail'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.form_show_labels = False
        self.helper.add_input(Submit('submit', 'Submit'))

        self.helper.layout = Layout(
            Div(
                Row(
                    Column(
                        PrependedText('microbe_level_01', 'Microbe'),
                        css_class='col-md-6',
                    ),
                    Column(
                        PrependedText('microbe_level_02', 'Microbe'),
                        css_class='col-md-6',
                    ), 
                ),
                Row(
                    Column(
                        PrependedText('resistance', 'Resistance (Phenotypic)'), 
                        css_class='col-md-6',
                    ),

                    Column(
                        PrependedText('resistance_gene', 'Resistance (Genomic)'), 
                        css_class='col-md-6',
                    ),
                ),
                Row(
                    Column(
                        HTML(''' <p>Group Allocation Production Stage:  {{factor.group_allocate_production_stage}} </p> ''')
                    ),
                    Column(
                        PrependedText('group_observe_production_stage', 'Observed Production Stage'), 
                        css_class='col-md-6',
                    ),
                ),

                HTML('''<hr class="mb-4" style="border-width:5px;">'''),

                
                HTML('''<br>'''),
                Row(
                    HTML(''' <h5 class="col-2">Location</h5> '''),
                    Column(
                        'place_in_text',
                        css_class='col-md-8',
                    ), 
                ),
                HTML('''<br>'''),
                Row(
                    HTML(''' <h5 class="col-2">Result Unit</h5> '''),
                    Column(
                        'moa_unit',
                        css_class='col-md-8',
                    ), 
                ),
                HTML('''<br>'''),
                Row(
                    HTML(''' <h5 class="col-2">Grain/Type</h5> '''),
                    Column(
                        Field('moa_type', css_id='moa_type_id'),
                        css_class='col-md-8',
                    ), 
                ),
                
                # Quantitative Data -------------------------------------------

                HTML('''<br> <h3>Quantitative Data</h3> '''),

                HTML('''<hr style="border-width:5px;">'''),

                HTML('''<p> This section combines a count table and a prevalence table. <br>
                            You do not need to extract all fields. <br>
                            See the data extraction guide for more details. 
                        </p> '''),


                HTML('''
                        <br>
                        <table id="fullFacData" class="table table-bordered">
                            <tr>
                                <td></td>
                                <td></td>
                                <td>
                                    <h6>AMR+</h6>
                                </td>
                                <td>
                                    <h6>AMR-</h6>
                                </td>
                                <td>
                                    <h6>Total</h6>
                                </td>
                            </tr>
                            <tr>
                                <td rowspan="2" class="rotate align-middle "><h5>Factor</h5></td>
                                <td rowspan="2">'''),

                HTML(''' <h5>{{ factor.group_factor }}</h5> '''),
                HTML('''        </td>
                                <td>'''),
                AppendedText('contable_a', '(n)'),
                HTML('''        </td>
                                <td>'''),
                AppendedText('contable_b', '(n)', css_id='ct_b'),
                HTML('''        </td>
                                <td rowspan="2">'''),
                AppendedText('table_n_ab', '(n)', css_id='total_exp', style="height: 110px"),
                HTML('''        </td>
                            </tr>
                            <tr>
                                <td>'''),
                AppendedText('prevtable_a', '(%)',css_id='pt_a', wrapper_class="prevalence"),
                HTML('''        </td>
                                <td>'''),
                AppendedText('prevtable_b', '(%)', css_id='pt_b', wrapper_class="prevalence"),
                HTML('''        </td>
                            </tr>
                            <tr>
                                <td class="rotate" rowspan="2"><h5>Comparator</h5></td>
                                <td rowspan="2">'''),
                
                # Comparator Row
                HTML(''' <h5> {{ factor.group_comparator }}</h5> '''),
                HTML('''        </td>
                                <td>'''),
                AppendedText('contable_c', '(n)', css_id='ct_c'),
                HTML('''        </td>
                                <td>'''),
                AppendedText('contable_d', '(n)', css_id='ct_d'),
                HTML('''        </td>
                                <td rowspan="2">'''),
                AppendedText('table_n_cd', '(n)', css_id='total_ref', style="height: 110px"),
                HTML('''        </td>
                            </tr>
                            <tr>
                                <td>'''),
                AppendedText('prevtable_c', '(%)', css_id='pt_c', wrapper_class="prevalence"),
                HTML('''        </td>
                                <td>'''),
                AppendedText('prevtable_d', '(%)', css_id='pt_d', wrapper_class="prevalence"),
                HTML('''        </td>
                            </tr>
                        </table>
                '''),
                HTML('''<br>'''),
                Row(
                    Column(PrependedText('odds_ratio', "Odds Ratio"), css_class='col-2'), 
                    Column(PrependedText('odds_ratio_lo', "OR (Lower Bounds)"), css_class='col-2'),
                    Column(PrependedText('odds_ratio_up', "OR (Upper Bounds)"), css_class='col-2'),
                    Column(PrependedText('odds_ratio_sig', "OR Significance Level"), css_class='col-2'),
                ),
                
                FormActions(
                    Submit('save', 'Save changes')
                ),
            ),
        )




