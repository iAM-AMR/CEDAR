

# URLS

from django.urls import path, re_path

from cedar_core.views import *
from cedar_core.views import PublisherAutocomplete

# from django.urls include
# from django.contrib.auth import views as auth_views

# TODO: Namespace the app. https://docs.djangoproject.com/en/4.1/intro/tutorial03/#namespacing-url-names
# This requires updating all tags in templates.

# app_name = 'cedar'

urlpatterns = [

    ##path('accounts/', include('django.contrib.auth.urls')), #create_field='publish-id-autocomplete'
    re_path(r'^publish-id-autocomplete/$', PublisherAutocomplete.as_view(), name='publish-id-autocomplete',),
    #path('accounts/login/', auth_views.LoginView.as_view(template_name='cedar_core/login.html')),

    path('about/',  views.about,      name='about'),
    path('export/', views.get_timber, name='get_timber'),


    # REFERENCES --------------------------------------------------------------

    # Add
    # There is no add reference view.

    # Browse All
    path('browse/references/',          views_reference.browse_references, name='browse_references'),
    
    # List Children
    path('reference/<int:pk>/factors/', views_reference.list_child_factors, name='list_child_factors'),

    # Details
    path('reference/<int:pk>/',         views_reference.detail_reference, name='detail_reference'), 
    path('reference/<int:pk>/details/', views_reference.detail_reference, name='detail_reference'),

    # Delete
    #path('reference/<int:pk>/delete', views_reference.delete_reference, name='delete_reference'),
    
    # Edit
    path('reference/<int:pk>/edit/',    views_reference.edit_reference,   name='edit_reference'  ),



    # FACTORS -----------------------------------------------------------------

    # Add
    path('reference/<int:reference_id>/factor/new/',                  views.new_blank_factor,     name='new_blank_factor'),
    
    # Browse All
    path('browse/factors/',    views_factor.browse_factors, name='browse_factors'),

    # List Children
    path('reference/<int:reference_id>/factor/<int:pk>/outcomes/',    views_factor.list_child_resistance_outcomes, name='list_child_resistance_outcomes'),

    # Details
    path('reference/<int:reference_id>/factor/<int:pk>/',             views_factor.detail_factor, name='detail_factor'),
    path('reference/<int:reference_id>/factor/<int:pk>/details/',     views_factor.detail_factor, name='detail_factor'),
    
    # Delete
    path('factor/<int:pk>/delete/',                                   views_factor.delete_factor, name='delete_factor'),

    # Edit
    path('reference/<int:reference_id>/factor/<int:pk>/edit/',        views_factor.edit_factor,   name='edit_factor'),
    
    
    
    # RESITANCE OUTCOMES ------------------------------------------------------

    # Create
    path('reference/<int:reference_id>/factor/<int:pk>/outcome/create/', views_resout.createResistanceOutcome, name='create_ro'), 

    # Browse All
    # There is no resistance outcome browse view.

    # List Children
    # There is no resistance outcome child view.

    # Details
    # There are no details view for resistance outcomes; these are aliases to edit for now.
    
    # Delete
    path('reference/<int:reference_id>/factor/<int:factor_id>/outcome/<int:pk>/delete/',  resoutDeleteView.as_view(), name='resout-delete'),

    # Update
    path('reference/<int:reference_id>/factor/<int:factor_id>/outcome/<int:pk>/edit/', views_resout.EditReferenceOutcome, name="edit_resout"),


]


