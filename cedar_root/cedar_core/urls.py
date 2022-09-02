from django.urls import include, path, reverse, re_path

from cedar_core.views import *

from cedar_core.views import PublisherAutocomplete

from django.contrib.auth import views as auth_views

urlpatterns = [
    ##path('accounts/', include('django.contrib.auth.urls')), #create_field='publish-id-autocomplete'
    re_path(r'^publish-id-autocomplete/$', PublisherAutocomplete.as_view(), name='publish-id-autocomplete',),
    #path('accounts/login/', auth_views.LoginView.as_view(template_name='cedar_core/login.html')),
    path('references/', views.browse_references, name='browse_references'),
    path('references/<int:ref_id>/', details.detail_reference, name='detail_reference'),
    path('references/<int:ref_id>/edit/', details.edit_reference, name='edit_reference'),
    path('references/<int:obj_id>/add/<str:form_type>/', views.add_new_obj, name='add_new_obj'),
    path('references/<int:ref_id>/factors/', views.edit_reference_factor_list, name='edit_reference_factor_list'),
    path('references/<int:reference_id>/factors/<int:factor_id>/', details.detail_factor, name='detail_factor'),
    path('references/<int:ref_id>/factors/<int:fac_id>/edit/', views.edit_factor, name='edit_factor'),
    path('references/<int:ref_id>/factors/<int:fac_id>/outcomes/', views.view_resistance_outcomes, name='view_resistance_outcomes'),
    path('references/<int:reference_id>/factors/<int:factor_id>/outcomes/<int:res_outcome_id>', details.detail_res_outcome, name='detail_res_outcome'),
    path('references/<int:reference_id>/factors/<int:factor_id>/outcomes/<int:res_outcome_id>/edit/', edit.edit_resistance_outcome, name='edit_resistance_outcome'),
    #path('references/<int:ref_id>/factors/<int:fac_id>/expand/', views.expand_factor, name='expand_factor'),
    path('references/<int:ref_id>/factors/<int:fac_id>/delete/', views.delete_factor, name='delete_factor'),
    path('references/export/', views.query_timber, name='query_timber'),
    path('references/export/papers/topictab/', views.topic_tab_query, name='topic_tab_query'),
    # NEW URL paths here for resistance outcome pages (viewing a table & editing)
    path('factors/', views.browse_factors, name='browse_factors'),
]