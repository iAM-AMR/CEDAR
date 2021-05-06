from django.forms import ModelForm
from django import forms
from cedar_core.models import factor, reference, location_join, reference_note, location_01, location_02, host_01, microbe_01, atc_vet
from django.utils.translation import gettext_lazy as _

from crispy_forms.bootstrap import Tab, TabHolder, FormActions, PrependedText, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, ButtonHolder, Row, Column, HTML, Field
from crispy_forms.utils import render_crispy_form

from django.forms.models import modelformset_factory, inlineformset_factory

from dal import autocomplete

class ReferenceForm(ModelForm):
    class Meta:
        model = reference
        fields = ['study_title','study_authors', 'publish_year', 'publish_id', 'publish_doi', 'publish_pmid', 
                  'exclude_extraction','exclude_extraction_reason', 'study_design_id', 'study_design_detail',
                  'study_sample_method', 'ast_method_id', 'ref_has_explicit_break', 'ref_has_mic_table']
        widgets = {
            'publish_id': autocomplete.ModelSelect2(url='publish-id-autocomplete')
        }
        
        # Replaced by prepended text below
        #labels = {
            #'study_title': 'Title',
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
        
        # Hides help text
        #help_texts = {}
        #for fieldname in fields:
            #help_texts[fieldname] = None
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #Create FormHelper from crispy forms for layout
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        #self.helper.form_class = 'form-horizontal'
        #can have class='sr-only' to hide labels
        #but how to add w/in Layout?
        self.helper.layout = Layout(
            #Main tab
            Div(
                Column(
                    Div(
                        HTML(
                            """<h6>Bibliographic Information:</h6> <hr>"""
                        ),
                        PrependedText('study_title', 'Title', placeholder="Study Title Here"), 
                        PrependedText('study_authors', 'Author Name(s)', placeholder="Author Name(s) Here"),
                    ),            
                    Div(
                        Row(
                            Column(
                                PrependedText('publish_year', 'Publication Year', placeholder="Publication Year Here"),
                                css_class='col-md-6'
                            ),
                            Column(
                                PrependedText('publish_id', 'Publisher', placeholder="Publisher Here"), #form-text styles oddly
                                css_class='col-md-6'
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
                        HTML(
                            """<br> <h6>Study Identifiers:</h6> <hr>"""
                        ),
                        Row(
                            Column(
                                PrependedText('publish_doi', 'DOI:', placeholder="DOI Here"),
                                css_class='col-md-6'
                            ),
                            Column(
                                PrependedText('publish_pmid', 'PMID:', placeholder="PUBMED ID Here"),
                                css_class='col-md-6'
                            ),
                        ),
                    ),
                    Div(
                        HTML(
                            """<br> <h6>Exclusion Status:</h6> <hr>"""
                        ),
                        PrependedText('exclude_extraction', 'Exclude?', css_class='ml-2 mt-2'),
                        PrependedText('exclude_extraction_reason', 'Is Excluded Because:', placeholder="Reason Here", css_class='form-group'),
                    ),
                    FormActions(
                        Submit('save', 'Save changes')
                    ),
                ),
                css_id='main-md',
                css_class='tab-pane fade show active',
            ),
            #Study Design tab
            Div(
                Column(
                    HTML(
                        """<br> <h6>Study Design:</h6> <hr>"""
                    ),          
                    PrependedText('study_design_id', 'Study Design:'),
                    PrependedText('study_design_detail', 'Design Detail:'), 
                    PrependedText('study_sample_method', 'Sampling Method:'), 
                    HTML(
                        """<h6>AST:</h6> <hr>"""
                    ),
                    Row(  
                        Column(PrependedText('ast_method_id', 'AST Method'), css_class='form-group col-md-4 mx-0'),
                        Column(PrependedText('ref_has_explicit_break', 'Has Explicit Breakpoints?'), css_class='form-group col-md-4 mb-0'),
                        Column(PrependedText('ref_has_mic_table', 'Has MIC Table?'), css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'
                    ),
                ),    
                FormActions(
                    Submit('save', 'Save changes')
                ),
                css_id='study-md',
                css_class='tab-pane fade',
            ),
        )
        
class RefLocForm(ModelForm):
    class Meta:
        model = location_join
        fields = ['location_01_id', 'location_02_id', 'ref_loc_note']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        #self.businessprofile_id = kwargs.pop('businessprofile_id')
        #super(RefLocForm, self).__init__(*args, **kwargs)
        #self.fields['location_01'].queryset = location_01.objects.filter(business_profile_id = self.businessprofile_id)

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
                    PrependedText('location_01_id', 'Country'),
                    HTML("""<br>"""),
                    Column(
                        Column(
                            Row(
                                Column(
                                    PrependedText('location_02_id', 'Region:'),
                                    'ref_loc_note',
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
RefLocFormSet = inlineformset_factory(reference, location_join, form=RefLocForm, extra=0, can_delete=True)

#BaseRefLocFormSet = modelformset_factory(location_join, form=RefLocForm, extra=0, can_delete=True)

#class RefLocFormSet(BaseRefLocFormSet):
    
    #def __init__(self, *args, **kwargs):
        #  create a location_01 attribute and take it out from kwargs
        # so it doesn't messes up with the other formset kwargs
        #self.businessprofile_id = kwargs.pop('businessprofile_id')
        #super(RefLocFormSet, self).__init__(*args, **kwargs)
        #for form in self.forms:
            #form.empty_permitted = False

    #def _construct_form(self, *args, **kwargs):
        # inject location_01 in each form on the formset
        #kwargs['businessprofile_id'] = self.businessprofile_id
        #return super(RefLocFormSet, self)._construct_form(*args, **kwargs)
           
class RefNoteForm(ModelForm):
    class Meta:
        model = reference_note
        fields = ['note', 'user_id', 'resolved']
        #labels = {
            #'resolved': 'Resolved?',
        #}
        help_texts = {}
        for fieldname in fields:
            if fieldname != 'note':
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
                        Column(PrependedText('user_id', 'User'), css_class='form-group col-md-8 mx-0'),
                        Column(PrependedText('resolved', 'Resolved?', css_class='ml-2 mt-2'), css_class='form-group col-md-4 mx-0'),
                        css_class='form-row'
                    ),
                    Field('note', css_class='col-md-9'),
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
    
    am_classes = forms.MultipleChoiceField(choices=AM_CLASS_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
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
        #No amu_id for now -- add in later
        fields = ['resistance_id', 'factor_title', 'factor_description', 'place_in_text', 'host_01_id', 'host_02_id',
                  'microbe_01_id', 'microbe_02_id', 'prod_stage_group_allocate_id', 'prod_stage_group_observe_id', 'group_exposed',
                  'group_referent', 'moa_type_id', 'moa_unit_id', 'contable_a', 'contable_b', 'contable_c', 'contable_d',
                  'prevtable_a', 'prevtable_b', 'prevtable_c', 'prevtable_d', 'table_n_exp', 'table_n_ref',
                  'odds_ratio', 'odds_ratio_lo', 'odds_ratio_up', 'odds_ratio_sig']
        help_texts = {}
        #help_texts['prod_stage_group_allocate'] = 'When the factor was applied'
        for fieldname in ['contable_a', 'contable_b', 'contable_c', 'contable_d', 'resistance_id',
                          'prevtable_a', 'prevtable_b', 'prevtable_c', 'prevtable_d',
                          'table_n_exp', 'table_n_ref', 'microbe_02_id', 'host_02_id', 'host_01_id', 'group_exposed', 'group_referent',
                          'odds_ratio', 'odds_ratio_lo', 'odds_ratio_up', 'microbe_01', 'odds_ratio_sig']:
            if fieldname == 'odds_ratio_sig':
                help_texts[fieldname] = 'The p-value associated with the odds ratio. If an odds ratio is provided, without a significance level, please report "NR" for "not reported".'
            else:
                help_texts[fieldname] = None
        labels = {
            'factor_title': None,
            'factor_description': None,
            'host_01_id': None,
            'host_02_id': None,
            'microbe_01_id': None,
            'microbe_02_id': None,
            'place_in_text': None,
            'moa_type_id': None,
            'prod_stage_group_allocate_id': 'Allocated',
            'prod_stage_group_observe_id': 'Observed',
            'resistance_id': None,
            'contable_a': None,
            'contable_b': None,
            'table_n_exp': None,
            'table_n_ref': None,
            'group_exposed': None,
            'group_referent': None,
            'prevtable_a': None,
            'prevtable_b': None,
            'contable_c': None,
            'prevtable_c': None,
            'contable_d': None,
            'prevtable_d': None,
            'odds_ratio': 'OR',
            'odds_ratio_lo': 'Lower CI',
            'odds_ratio_up': 'Upper CI',
            'odds_ratio_sig': 'Sig.',
            'moa_unit_id': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        #self.helper.form_class = 'form_horizontal'
        #to_exclude = ['odds_ratio_sig', 'odds_ratio', 'odds_ratio_lo', 'odds_ratio_up',
                      #'contable_a', 'contable_b', 'table_n_exp']
        to_exclude = ['resistance_id', 'factor_title', 'factor_description', 'place_in_text', 'host_01_id', 'host_02_id',
                  'microbe_01_id', 'microbe_02_id', 'group_exposed', 'contable_a', 'contable_b',
                  'group_referent', 'moa_type_id', 'moa_unit_id', 'contable_c', 'contable_d', 'table_n_exp',
                  'prevtable_a', 'prevtable_b', 'prevtable_c', 'prevtable_d', 'table_n_ref', 'group_exposed', 'group_referent']
        for i in range(0,len(to_exclude)-1):
            self.fields[to_exclude[i]].label = False
        #self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Div(
                    PrependedText('factor_title', 'Title'),
                    PrependedText('factor_description', 'Description'), 
                    css_class='form-horizontal'
                    #css_class='col-md-12'
                ),
                #HTML('''<hr>'''),
                HTML(''' <br> '''),
                Row(
                    Column(
                        Row(
                            PrependedText('host_01_id', 'Host'),
                            'host_02_id',
                        ),
                        css_class='col-md-5 ml-1',
                    ),
                    #Column(
                        #HTML('''<div style="border-left: 2px solid white; height: 100px; margin-left: 80px;"></div>'''), #margin-left to offset automatic spacing of border style
                        #css_class='col-md-2',
                    #),
                    Column(
                        Row(
                            PrependedText('microbe_01_id', 'Microbe'), 
                            'microbe_02_id',
                        ),
                        css_class='col-md-6',
                    ),
                    #Column(
                        #Row(
                            #PrependedText('resistance', 'AMR'), 
                            #css_class='col-md-3',
                            #css_class='form-label-md-2'
                        #),
                    #),
                    #css_class='form-group',
                    #css_class='justify-content-center',
                ),
                Row(
                    Column(
                        PrependedText('resistance_id', 'AMR'), 
                        css_class='col-md-10',
                        #css_class='form-label-md-2'
                    ),
                ),
                HTML('''<hr style="border-width:5px;">'''),
                HTML('''<br>'''),
                Row(
                    HTML(''' <h5 class="col-2">Stage</h5> '''),
                    Column(
                        'prod_stage_group_allocate_id',
                        css_class='col-md-4',
                    ), 
                    Column(
                        'prod_stage_group_observe_id',
                        css_class='col-md-4',
                    ),
                ),
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
                        'moa_unit_id',
                        css_class='col-md-8',
                    ), 
                ),
                HTML('''<br>'''),
                Row(
                    HTML(''' <h5 class="col-2">Grain/Type</h5> '''),
                    Column(
                        Field('moa_type_id', css_id='moa_type_id'),
                        css_class='col-md-8',
                    ), 
                ),
                HTML('''<hr style="border-width:5px;">'''),
                #HTML('''<br> <h5 class="col-2">Factor Data</h5> '''),
                HTML('''
                        <br>
                        <table id="fullFacData" class="table table-borderless">
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
                                <td rowspan="2"><h5>Exposed <br> Group</h5></td>
                                <td rowspan="2">'''),
                Field('group_exposed', style="height: 125px"),
                HTML('''        </td>
                                <td>'''),
                Field('contable_a', css_id='ct_a'),
                HTML('''        </td>
                                <td>'''),
                Field('contable_b', css_id='ct_b'),
                HTML('''        </td>
                                <td rowspan="2">'''),
                Field('table_n_exp', css_id='total_exp', style="height: 125px"),
                HTML('''        </td>
                            </tr>
                            <tr>
                                <td>'''),
                Field('prevtable_a', css_id='pt_a'),
                HTML('''        </td>
                                <td>'''),
                Field('prevtable_b', css_id='pt_b'),
                HTML('''        </td>
                            </tr>
                            <tr>
                                <td rowspan="2"><h5>Referent <br> Group</h5></td>
                                <td rowspan="2">'''),
                Field('group_referent', style="height: 125px"),
                HTML('''        </td>
                                <td>'''),
                Field('contable_c', css_id='ct_c'),
                HTML('''        </td>
                                <td>'''),
                Field('contable_d', css_id='ct_d'),
                HTML('''        </td>
                                <td rowspan="2">'''),
                Field('table_n_ref', css_id='total_ref', style="height: 125px"),
                HTML('''        </td>
                            </tr>
                            <tr>
                                <td>'''),
                Field('prevtable_c', css_id='pt_c'),
                HTML('''        </td>
                                <td>'''),
                Field('prevtable_d', css_id='pt_d'),
                HTML('''        </td>
                            </tr>
                        </table>
                '''),
                HTML('''<br>'''),
                Row(
                    Column(
                        HTML(''' <h6 style="margin-left: 10px;">Odds Ratio</h6> '''),
                        #css_class='col-md-2 ml-1',
                    ),
                    #HTML(''' <h6 class="col-2">Test</h6> '''),
                    Column(Field('odds_ratio', css_id='or'), css_class='col-2'), 
                    Column(Field('odds_ratio_lo', css_id='or_lo'), css_class='col-2'),
                    Column(Field('odds_ratio_up', css_id='or_up'), css_class='col-2'),
                    Column(Field('odds_ratio_sig', css_id='or_sig'), css_class='col-4'),
                ),
                # JavaScript experimenting with changing attributes of numerical fields (show/hide etc.) depending on dropdown selection of Contingency Table, Prevalence Table, etc.
                HTML('''
                    <script>
                        $('#moa_type_id').change(function () {
                            var end = this.value;
                            //if (end == 2){ //Prevalence Table
                            $('#ct_a').css( "border", "3px solid red" );
                            //}
                            //else {
                                //$('[name="otherInstitute"]').hide();
                            //}
                        })
                    </script>
                '''),
                # css_class='col no-gutters',
                FormActions(
                    Submit('save', 'Save changes')
                ),
            ),
        )
        
class ConTableForm(ModelForm):
    class Meta:
        model = factor
        fields = ['resistance_id','group_exposed', 'group_referent', 'moa_type_id', 'contable_a', 'contable_b',
                  'contable_c', 'contable_d', 'table_n_exp', 'table_n_ref']
        help_texts = {}
        for fieldname in fields:
            help_texts[fieldname] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['moa_type_id'].disabled = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            HTML('''
                    <!-- <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/mdbootstrap@4.19.2/css/addons/datatables.min.css"> -->
                    <table id="facTable" class="table">
                        <thead>
                            <tr style="background-color: white;">
                                <th>AMR</th>
                                <th>Factor Data</th>
                            </tr>
                        </thead>
                        <tbody>
                            <td>
                                <table id="amrData" class="table table-sm style="width: 100%;">
                                    <thead>
                                        <tr style="background-color: rgb(242, 247, 255);">
                                            <th style="border: none;">'''),
            Field('resistance_id'),
            HTML('''                        </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                            <td>
                                <table id="facData" class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>'''),
            Field('moa_type_id', style="width: auto; height: auto;"),
            HTML('''                        </th>
                                            <th># AMR+</th>
                                            <th># AMR-</th>
                                            <th># Total</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Exposed</td>
                                            <td>'''),
            Field('contable_a', style="width: 80px;"),
            HTML('''                        </td>
                                            <td>'''),
            Field('contable_b', style="width: 80px;"), 
            HTML('''                        </td>
                                            <td>'''),
            Field('table_n_exp', style="width: 80px;"),
            HTML('''                        </td>
                                        </tr>
                                        <tr>
                                            <td>Referent</td>
                                            <td>'''),
            Field('contable_c', style="width: 80px;"),
            HTML('''                        </td>
                                            <td>'''),
            Field('contable_d', style="width: 80px;"),
            HTML('''                        </td>
                                            <td>'''),
            Field('table_n_ref', style="width: 80px;"),
            HTML('''                        </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tbody>
                        <tfoot>
                            <tr style="border: none;">
                                <td style="border: none;"></td>
                                <td style="text-align: right; border: none;">'''),
            FormActions(
                Submit('save', 'Save changes')
            ),
            HTML('''            </td>
                            </tr>
                        </tfoot>
                    </table>
            '''),
        )
        
        
class PrevTableForm(ModelForm):
    class Meta:
        model = factor
        fields = ['resistance_id', 'moa_type_id', 'prevtable_a', 'prevtable_b',
                  'prevtable_c', 'prevtable_d', 'table_n_exp', 'table_n_ref']
        help_texts = {}
        for fieldname in fields:
            help_texts[fieldname] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['moa_type_id'].disabled = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            HTML('''
                    <table id="facTable" class="table">
                        <thead>
                            <tr style="background-color: white;">
                                <th>AMR</th>
                                <th>Factor Data</th>
                            </tr>
                        </thead>
                        <tbody>
                            <td>
                                <table id="amrData" class="table table-sm style="width: 100%;">
                                    <thead>
                                        <tr>
                                            <th style="border: none;">'''),
            Field('resistance_id'),
            HTML('''                        </th>
                                        </tr>
                                    </thead>
                                </table>
                            </td>
                            <td>
                                <table id="facData" class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>'''),
            Field('moa_type_id', style="width: auto; height: auto;"),
            HTML('''                        </th>
                                            <th>% AMR+</th>
                                            <th>% AMR-</th>
                                            <th># Total</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Exposed</td>
                                            <td>'''),
            Field('prevtable_a', style="width: 80px;"),
            HTML('''                        </td>
                                            <td>'''),
            Field('prevtable_b', style="width: 80px;"), 
            HTML('''                        </td>
                                            <td>'''),
            Field('table_n_exp', style="width: 80px;"),
            HTML('''                        </td>
                                        </tr>
                                        <tr>
                                            <td>Referent</td>
                                            <td>'''),
            Field('prevtable_c', style="width: 80px;"),
            HTML('''                        </td>
                                            <td>'''),
            Field('prevtable_d', style="width: 80px;"),
            HTML('''                        </td>
                                            <td>'''),
            Field('table_n_ref', style="width: 80px;"),
            HTML('''                        </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </td>
                        </tbody>
                        <tfoot>
                            <tr style="border: none;">
                                <td style="border: none;"></td>
                                <td style="text-align: right; border: none;">'''),
            FormActions(
                Submit('save', 'Save changes')
            ),
            HTML('''            </td>
                            </tr>
                        </tfoot>
                    </table>
                    
                    <script>
                        $(document).ready(function () {
                            $('#facTable').DataTable({
                                "paging": false,
                                "searching": false,
                                "info": false,
                            });
                        });
                    </script>

                    <script>
                        $(document).ready(function () {
                            $('#facData').DataTable({
                                "paging": false,
                                "searching": false,
                                "info": false,
                            });
                        });
                    </script>
                    
                    <script>
                        $(document).ready(function () {
                            $('#amrData').DataTable({
                                "paging": false,
                                "searching": false,
                                "info": false,
                            });
                        });
                    </script>
            '''),
        )

class OddsTableForm(ModelForm):
    class Meta:
        model = factor
        fields = ['resistance_id', 'moa_type_id',
                  'odds_ratio', 'odds_ratio_lo', 'odds_ratio_up', 'odds_ratio_sig']
        help_texts = {}
        for fieldname in fields:
            help_texts[fieldname] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['moa_type_id'].disabled = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            HTML('''
                    <table id="facTable" class="table">
                        <thead>
                            <tr style="background-color: white;">
                                <th>AMR</th>
                                <th>Factor Data</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>
                                    <table id="amrData" class="table table-sm style="width: 100%;">
                                        <thead>
                                            <tr>
                                                <th style="border: none;">'''),
            Field('resistance_id'),
            HTML('''        
                                                </th>
                                            </tr>
                                        </thead>
                                    </table>
                                </td>
                                <td>
                                    <table id="facData" class="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>'''),
            Field('moa_type_id', style="width: auto; height: auto;"),
            HTML('''                            </th>
                                                <th>Odds Ratio</th>
                                                <th>Lower CI</th>
                                                <th>Upper CI</th>
                                                <th>Sig</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td></td>
                                                <td>'''),
            Field('odds_ratio', style="width: 80px;"),
            HTML('''                            </td>
                                                <td>'''),
            Field('odds_ratio_lo', style="width: 80px;"),
            HTML('''                            </td>
                                                <td>'''),
            Field('odds_ratio_up', style="width: 80px;"),
            HTML('''                            </td>
                                                <td>'''),
            Field('odds_ratio_sig', style="width: 80px;"),
            HTML('''                            </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </td>
                            </tr>
                        </tbody>
                        <tfoot>
                            <tr style="border: none;">
                                <td style="border: none;"></td>
                                <td style="text-align: right; border: none;">'''),
            FormActions(
                Submit('save', 'Save changes')
            ),
            HTML('''            </td>
                            </tr>
                        </tfoot>
                    </table>
                    
                    <script>
                        $(document).ready(function () {
                            $('#facTable').DataTable({
                                "paging": false,
                                "searching": false,
                                "info": false,
                            });
                        });
                    </script>

                    <script>
                        $(document).ready(function () {
                            $('#facData').DataTable({
                                "paging": false,
                                "searching": false,
                                "info": false,
                            });
                        });
                    </script>
                    
                    <script>
                        $(document).ready(function () {
                            $('#amrData').DataTable({
                                "paging": false,
                                "searching": false,
                                "info": false,
                            });
                        });
                    </script>
            '''),
        )