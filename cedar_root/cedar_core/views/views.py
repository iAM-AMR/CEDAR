

import csv
from cedar_core.filters import timber_filter
from cedar_core.models import factor, publisher, reference, res_outcome, host_02, microbe_02
from dal import autocomplete
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render





def about(request): # =============================================================================
    #                 ----------------------------------------------------------------------- ABOUT
    # =============================================================================================

    """
    Return the 'About' page.
    """
    context = {
        'page_title': 'About CEDAR'    
    }

    return render(request, 'cedar_core/about.html', context)





class PublisherAutocomplete(autocomplete.Select2QuerySetView): # ==================================
    #                                                            ------------ PUBLISHERAUTOCOMPLETE
    # =============================================================================================

    """
    The purpose of this function is unclear, but is evidently related to 
    auto-completing the publisher (journal) name in the reference model.
    """
    
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return publisher.objects.none()

        qs = publisher.objects.all()

        if self.q:
            qs = qs.filter(pub_title__istartswith=self.q)

        return qs




class MicrobeTwoAutocomplete(autocomplete.Select2QuerySetView): # =================================
    #                                                             -------- MICROBE TWO AUTOCOMPLETE
    # =============================================================================================

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return microbe_02.objects.none()

        qs = microbe_02.objects.all()

        subset = self.forwarded.get('microbe_level_01', None)

        # If subset != None, filter where foreign key = subset.
        if subset:
            qs = qs.filter(microbe_level_01=subset)

        # Note, 'name' may only work here where __str__ is defined in the model.
        # Replace with field name on failure.
        if self.q:
            qs = qs.filter(microbe_02_name__istartswith=self.q)

        return qs



class HostTwoAutocomplete(autocomplete.Select2QuerySetView): # ====================================
    #                                                          -------------- HOST TWO AUTOCOMPLETE
    # =============================================================================================

    """
    Use DAL for autocompletion of host_02, and cascading selection.
    """

    def get_queryset(self):

        # Guard against unauthenticated enumeration of table.
        if not self.request.user.is_authenticated:
            return host_02.objects.none()

        qs = host_02.objects.all()

        subset = self.forwarded.get('host_level_01', None)

        # If subset != None, filter where foreign key = subset.
        if subset:
            qs = qs.filter(host_level_01=subset)

        # Note, 'name' may only work here where __str__ is defined in the model.
        # Replace with field name on failure.
        if self.q:
            qs = qs.filter(host_subtype_name__istartswith=self.q)

        return qs



@login_required
@permission_required('cedar_core.add_factor')
def new_blank_factor(request, reference_id): # ====================================================
    #                                          ----------------------------------- NEW_BLANK_FACTOR
    # =============================================================================================

    """
    This function creates a new blank factor associated with the reference 
    indicated by "reference_id". 
    """

    # Get parent reference
    parent_reference = reference.objects.get(pk=reference_id)

    # Create new blank factor with reference field complete. ID 
    # is assigned by auto-increment. 
    new_factor = factor(reference = parent_reference)

    # Save new factor
    new_factor.save()

    # Return to referer. Where no referer, home.
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))




def get_timber(request): # ========================================================================
    #                      ------------------------------------------------------------- GET_TIMBER
    # =============================================================================================

    """
    This function informs the "Get Timber" page, which allows users to filter 
    resistance outcomes, presented in the 'timber' format. It also allows users
    to export the filtered resistance outcomes as a timber-formatted CSV.
    """

    # The timber query.
    # Note, earlier error corrected in 503f38aaffd5fad4cf2c30f8ecbbf550460417aa 
    # may have been a result of the use of values_list() here (prev. values()). 

    timber_qs_all = res_outcome.objects.all().values_list(
    'id',
    'pid_ro',
    'factor__reference__id',
    'factor__reference__pid_reference',
    'factor__reference__refwk',
    'factor__reference__publish_doi',
    'factor__reference__publish_pmid',
    'factor__reference__key_bibtex',
    'factor__reference__ref_title',
    'factor__reference__ref_country__country',
    'factor__reference__study_design__study_design_name',
    'factor__id',
    'factor__pid_factor',
    'factor__factor_title',
    'factor__factor_description',
    'factor__group_factor',
    'factor__group_comparator',
    'factor__host_level_01__host_01_name',
    'factor__host_level_02__host_subtype_name',
    'factor__host_production_stream',
    'factor__host_life_stage',
    'factor__group_allocate_production_stage__production_stage_name',
    'group_observe_production_stage__production_stage_name',
    'moa_type__moa_type_name',
    'moa_unit__outcome_unit_name',
    'resistance__levelname_4_coarse',
    'resistance__levelname_5',
    'resistance_gene__genetic_element_name',
    'microbe_level_01__microbe_01_name',
    'microbe_level_02__microbe_02_name',
    'is_figure_extract',
    'figure_extract_method__method_name',
    'figure_extract_reproducible',
    'contable_a',
    'contable_b',
    'contable_c', 
    'contable_d',
    'prevtable_a',
    'prevtable_b',
    'prevtable_c',
    'prevtable_d',
    'table_n_ab',
    'table_n_cd',
    'odds_ratio',
    'odds_ratio_lo',
    'odds_ratio_up',
    'odds_ratio_sig',
    'odds_ratio_confidence',
    )

    # Timber column names.
    tmbr_default_col_names = [
    'id_res_out',
    'pid_res_out',
    'id_reference',
    'pid_reference',
    'ref_rwid',
    'ref_doi',
    'ref_pmid',
    'ref_bibtex_key',
    'ref_title',
    'country',
    'study_design',
    'id_factor',
    'pid_factor',
    'factor_title',
    'factor_description',
    'factor_group',
    'comparator_group',
    'host_level_01',
    'host_level_02',
    'host_production_stream',
    'host_life_stage',
    'stage_allocate',
    'stage_observe',
    'moa_type',
    'moa_unit',
    'resistance_class',
    'resistance',
    'resistance_gene',
    'microbe_level_01',
    'microbe_level_02',
    'is_figure_extract',
    'figure_extract_method',
    'figure_extract_reproducible',
    'contable_a',
    'contable_b',
    'contable_c', 
    'contable_d',
    'prevtable_a',
    'prevtable_b',
    'prevtable_c',
    'prevtable_d',
    'table_n_exp',
    'table_n_ref',
    'odds_ratio',
    'odds_ratio_lo',
    'odds_ratio_up',
    'odds_ratio_sig',
    'odds_ratio_confidence',
    ] 

    # Apply filter on GET from any form.
    filtered_timber = timber_filter(request.GET, queryset=timber_qs_all)

    
    # Export as CSV button includes HTML button 'name' = 'csv' parameter.
    # Generate CSV when pressed.
    if request.GET and ('csv' in request.GET):
            
            # See: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="timber.csv"'},
            )

            # See: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
            writer = csv.writer(response)

            # Write timber column names as a header.
            writer.writerow(tmbr_default_col_names)

            # Loop, writing each line of the QuerySet to the .CSV.
            for eachline in filtered_timber.qs:
                writer.writerow(eachline)

            # See: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
            return(response)


    context = {'filtered_timber': filtered_timber, 
               'col_list'       : tmbr_default_col_names, 
               'page_title'     : 'Get Timber'
               }
    
    return render(request, 'cedar_core/get_timber.html', context)








# Add either a new reference note, reference location, factor, or res_outcome
# @login_required
# @permission_required('cedar_core.add_factor')
# def add_new_obj(request, obj_id, form_type):
    
#     # This function is being depreciated; too much complexity for too little DRY improvement.

#     # obj_id would be better as "parent object ID"

#     obj = reference.objects.get(pk=obj_id)

#     if form_type == 'loc':
#         new_obj = reference_join_location(reference_id = obj)
#         redir_path = '/cedar_core/references/' + str(obj_id) + '/#loc-md'
    
#     elif form_type == 'note':
#         new_obj = reference_join_reference_note(fk_reference_join_note_reference_id = obj)
#         redir_path = '/cedar_core/references/' + str(obj_id) + '/#notes-md'
    
#     else: #form_type = 'fac'
#         new_obj = factor(reference = obj)
#         redir_path = '/reference/' + str(obj_id) + '/factors'
    
#     # Save new object and redirect
#     new_obj.save()
    
#     return redirect(redir_path)
