

# The URL Configuration for CEDAR_CORE

from cedar_core.views import *
from cedar_core.views import MicrobeTwoAutocomplete, PublisherAutocomplete
from django.urls import path, re_path



urlpatterns = [
    
    # AUTOCOMPLETE ------------------------------------------------------------

    re_path(r'^publish-id-autocomplete/$', 
            PublisherAutocomplete.as_view(), 
            name='publish-id-autocomplete',),

    re_path(r'^microbe-two-autocomplete/$', 
            MicrobeTwoAutocomplete.as_view(), 
            name='microbe-two-autocomplete',), 
    
    re_path(r'^host-two-autocomplete/$', 
            HostTwoAutocomplete.as_view(), 
            name='host-two-autocomplete',), 


    # BASE --------------------------------------------------------------------

    path('about/',  
         views.about,      
         name='about'),

    path('export/', 
         views.get_timber, 
         name='get_timber'),


    # REFERENCES --------------------------------------------------------------

    # Create
    # There is no create reference view.

    # Browse All
    path('browse/references/',          
         views_reference.browse_references, 
         name='browse_references'),
    
    # List Children
    path('reference/<int:pk>/factors/', 
         views_reference.list_child_factors, 
         name='list_child_factors'),

    # Details
    path('reference/<int:pk>/',
         views_reference.detail_reference, 
         name='detail_reference'), 

    # Details Alt
    path('reference/<int:pk>/details/', 
         views_reference.detail_reference, 
         name='detail_reference_alt'),

    # Delete
    # There is no delete reference view.
    
    # Edit
    path('reference/<int:pk>/edit/',
         views_reference.edit_reference,
         name='edit_reference'),


    # FACTORS -----------------------------------------------------------------

    # Create
    path('reference/<int:reference_id>/factor/new/',
         views.new_blank_factor,
         name='new_blank_factor'),
    
    # Browse All
    path('browse/factors/',
         views_factor.browse_factors, 
         name='browse_factors'),

    # List Children
    path('reference/<int:reference_id>/factor/<int:pk>/outcomes/',
         views_factor.list_child_resistance_outcomes, 
         name='list_child_resistance_outcomes'),

    # Details
    path('reference/<int:reference_id>/factor/<int:pk>/',
         views_factor.detail_factor,
         name='detail_factor'),
    
    # DEtails Alt
    path('reference/<int:reference_id>/factor/<int:pk>/details/',
         views_factor.detail_factor,
         name='detail_factor'),
    
    # Delete
    path('factor/<int:pk>/delete/',
         views_factor.delete_factor,
         name='delete_factor'),

    # Edit
    path('reference/<int:reference_id>/factor/<int:pk>/edit/',
         views_factor.edit_factor,
         name='edit_factor'),
    
    
    # RESITANCE OUTCOMES ------------------------------------------------------

    # Create
    path('reference/<int:reference_id>/factor/<int:pk>/outcome/create/', 
         views_resout.createResistanceOutcome, 
         name='create_ro'), 

    # Browse All
    # There is no resistance outcome browse view.

    # List Children
    # There is no resistance outcome child view.

    # Details
    # There are no details view for resistance outcomes; these are aliases to edit for now.
    
    # Delete
    path('reference/<int:reference_id>/factor/<int:factor_id>/outcome/<int:pk>/delete/',  
         resoutDeleteView.as_view(), 
         name='resout-delete'),

    # Update
    path('reference/<int:reference_id>/factor/<int:factor_id>/outcome/<int:pk>/edit/', 
         views_resout.EditReferenceOutcome, 
         name="edit_resout"),

]


