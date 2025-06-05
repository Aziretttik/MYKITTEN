from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('create_cat/', views.create_cat, name='create_cat'),
    path('catalog/', views.cat_catalog, name='cat_catalog'),
    path('cat/<int:cat_id>/', views.cat_detail, name='cat_detail'),
    path('adopt/<int:cat_id>/', views.adopt_cat, name='adopt_cat'),
    path('cat/add/', views.add_cat, name='add_cat'),
    path('cat/<int:cat_id>/edit/', views.edit_cat, name='edit_cat'),
    path('cat/<int:cat_id>/delete/', views.delete_cat, name='delete_cat'),
    path('cat/<int:cat_id>/toggle-adoption/', views.toggle_adoption, name='toggle_adoption'),
    path('adoption-requests/', views.adoption_requests, name='adoption_requests'),
    path('my-adoption-requests/', views.my_adoption_requests, name='my_adoption_requests'),


]
