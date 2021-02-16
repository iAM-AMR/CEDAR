from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('references/<int:ref_id>/', views.ref_detail, name='ref_detail'),
    path('references/<int:ref_id>/add/<str:form_type>', views.add_ref_info, name='add_ref_info'),
    path('references/<int:ref_id>/factors/', views.view_factors, name='view_factors'),
    path('references/<int:ref_id>/factors/<int:fac_id>/edit', views.factor_detail, name='factor_detail'),
    path('references/<int:ref_id>/factors/<int:fac_id>/expand', views.expand_factor, name='expand_factor'),
    path('references/<int:ref_id>/factors/<int:fac_id>/delete', views.delete_factor, name='delete_factor'),
    path('thanks/', views.add_ref_success, name='add_ref_success'),
    path('references/', views.view_references, name='view_references'),
    path('references/export/', views.export_query, name='export_query'),
]