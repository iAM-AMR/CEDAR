from django.urls import path

from . import views

urlpatterns = [
    path('references/<str:view_type>/', views.view_references, name='view_references'),
    path('references/<int:ref_id>/<str:view_type>/', views.ref_detail, name='ref_detail'),
    path('references/<int:ref_id>/add/<str:form_type>/<str:view_type>/', views.add_ref_info, name='add_ref_info'),
    path('references/<int:ref_id>/factors/<str:view_type>/', views.view_factors, name='view_factors'),
    path('references/<int:ref_id>/factors/<int:fac_id>/detail/<str:view_type>/', views.factor_detail, name='factor_detail'),
    path('references/<int:ref_id>/factors/<int:fac_id>/expand/<str:view_type>/', views.expand_factor, name='expand_factor'),
    path('references/<int:ref_id>/factors/<int:fac_id>/delete/<str:view_type>/', views.delete_factor, name='delete_factor'),
    path('thanks/', views.add_ref_success, name='add_ref_success'),
    path('references/export/', views.export_query, name='export_query'),
]