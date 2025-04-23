from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('item/<int:item_id>/edit/', views.item_edit_form, name='item_edit_form'),
]