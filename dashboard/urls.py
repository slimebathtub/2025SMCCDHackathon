from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('item/<int:item_id>/edit/', views.item_edit_form, name='item_edit_form'),
    path('item/create/', views.item_create_form, name='item_create_form'),
    path('item/<int:item_id>/delete/', views.item_delete_view, name='item_delete_form')
]