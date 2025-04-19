from django.urls import path
from .views import resources_view
from resources import views

urlpatterns = [
    path('resources/', resources_view, name='resources'),
    path('items/', views.center_item_list, name='center_item_list'),
    path('items/<int:item_id>/edit/', views.update_item, name='updateitem')
]