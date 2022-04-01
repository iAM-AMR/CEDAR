from django.urls import include, path, reverse

from . import views

from cedar_core.views import PublisherAutocomplete

from django.contrib.auth import views as auth_views

from django.conf.urls import url

urlpatterns = [
    ##path('accounts/', include('django.contrib.auth.urls')), #create_field='publish-id-autocomplete'
    url(r'^publish-id-autocomplete/$', PublisherAutocomplete.as_view(), name='publish-id-autocomplete',),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='cedar_core/login.html')),
    path('references/', views.view_references, name='view_references'),
    path('references/<int:ref_id>/', views.ref_detail, name='ref_detail'),
    path('references/<int:obj_id>/add/<str:form_type>/', views.add_new_obj, name='add_new_obj'),
    path('references/<int:ref_id>/factors/', views.view_factors, name='view_factors'),
    path('references/<int:ref_id>/factors/<int:fac_id>/detail/', views.factor_detail, name='factor_detail'),
    path('references/<int:ref_id>/factors/<int:fac_id>/detail/associations/', views.view_resistance_outcomes, name='view_resistance_outcomes'),
    path('references/<int:ref_id>/factors/<int:fac_id>/detail/associations/<int:prev_ro_id>/detail/', views.resistance_outcome_detail, name='resistance_outcome_detail'),
    #path('references/<int:ref_id>/factors/<int:fac_id>/expand/', views.expand_factor, name='expand_factor'),
    path('references/<int:ref_id>/factors/<int:fac_id>/delete/', views.delete_factor, name='delete_factor'),
    path('references/export/', views.query_timber, name='query_timber'),
    path('references/export/papers/topictab/', views.topic_tab_query, name='topic_tab_query'),
    # NEW URL paths here for resistance outcome pages (viewing a table & editing)
]