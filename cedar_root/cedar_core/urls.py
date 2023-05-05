

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

    # REFERENCES ----------------------
    path('references/', views_reference.browse_references, name='browse_references'),
    #path('reference/'),
    #path('reference/add')
    path('reference/<int:pk>/',         views_reference.detail_reference, name='detail_reference_generic'),  # No Generic Template 
    path('reference/<int:pk>/details/',  views_reference.detail_reference, name='detail_reference'),
    #path('reference/<int:pk>/delete', views_reference.delete_reference, name='delete_reference'),
    path('reference/<int:pk>/edit/',    views_reference.edit_reference,   name='edit_reference'  ),
    path('reference/<int:pk>/factors/', views_reference.edit_reference_factor_list, name='edit_reference_factor_list'),
    path('reference/<int:pk>/factor/',  views_reference.edit_reference_factor_list, name='edit_reference_factor_list'),
    #path('reference/<int:pk>/factor/add', views_reference),

    # FACTORS -------------------------
    path('reference/<int:reference_id>/factor/<int:pk>/',             views_factor.detail_factor, name='detail_factor_generic'), # No Generic Template
    path('reference/<int:reference_id>/factor/new/',                  views.new_blank_factor,     name='new_blank_factor'),
    path('reference/<int:reference_id>/factor/<int:pk>/details/',     views_factor.detail_factor, name='detail_factor'),
    path('factor/<int:pk>/delete/',                                   views_factor.delete_factor, name='delete_factor'),
    path('reference/<int:reference_id>/factor/<int:pk>/edit/',        views_factor.edit_factor,   name='edit_factor'),
    path('reference/<int:reference_id>/factor/<int:pk>/outcomes/',    views_factor.list_resistance_outcomes, name='list_resistance_outcomes'),
    path('reference/<int:reference_id>/factor/<int:pk>/outcome/',     views_factor.list_resistance_outcomes, name='list_resistance_outcomes'),
    path('reference/<int:reference_id>/factor/<int:pk>/outcome/add/', resoutCreateView.as_view(), name='resout-add'), 
    # Update??

    # RESITANCE OUTCOMES --------------
    path('reference/<int:reference_id>/factor/<int:factor_id>/outcome/<int:pk>',          views_resout.detail_res_outcome, name='detail_resistance_outcome_generic'),
    path('reference/<int:reference_id>/factor/<int:factor_id>/outcome/<int:pk>/details/', resoutView.as_view(), name='detail_resistance_outcome'),
    path('reference/<int:reference_id>/factor/<int:factor_id>/outcome/<int:pk>/delete/',  resoutDeleteView.as_view(), name='resout-delete'),
    path('reference/<int:reference_id>/factor/<int:factor_id>/outcome/<int:pk>/edit/',    views_resout.edit_resistance_outcome, name='edit_resistance_outcome'),
    
    path('reference/<int:reference_id>/factor/<int:factor_id>/outcome/<int:pk>/update/',  resoutUpdateView.as_view(), name='resout-update'),
    path('reference/<int:reference_id>/factor/<int:factor_id>/outcomes/<int:pk>/cptest/', views_resout.resistance_outcome_detail, name='resout-cptest'),
    

    
    path('browse/references/', views_reference.browse_references, name='browse_references'),
    path('browse/factors/',    views_factor.browse_factors, name='browse_factors'),
    #path('reference/<int:obj_id>/add/<str:form_type>/', views.add_new_obj, name='add_new_obj'),
    #path('references/<int:ref_id>/factors/<int:fac_id>/expand/', views.expand_factor, name='expand_factor'),
    path('export/', views.get_timber, name='get_timber'),
    path('about/', views.about, name='about'),
]


