from django.urls import include, path

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='cedar_core/login.html')),
    path('references/', views.view_references, name='view_references'),
    path('references/<int:ref_id>/', views.ref_detail, name='ref_detail'),
    path('references/<int:ref_id>/add/<str:form_type>/', views.add_ref_info, name='add_ref_info'),
    path('references/<int:ref_id>/factors/', views.view_factors, name='view_factors'),
    path('references/<int:ref_id>/factors/<int:fac_id>/detail/', views.factor_detail, name='factor_detail'),
    path('references/<int:ref_id>/factors/<int:fac_id>/expand/', views.expand_factor, name='expand_factor'),
    path('references/<int:ref_id>/factors/<int:fac_id>/delete/', views.delete_factor, name='delete_factor'),
    path('references/export/', views.export_query, name='export_query'),
]