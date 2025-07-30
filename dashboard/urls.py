from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='resources_page'),
    path('resources/', views.dashboard_view, name='resources_page'),
    path('item/<int:item_id>/edit/', views.item_edit_form, name='item_edit_form'),
    path('item/create/', views.item_create_form, name='item_create_form'),

    path('delete/<str:model>/<int:id>/', views.generic_delete_view, name='generic_delete'),

    path('room/', views.dashboard_room_view, name='room_page'),
    path('room/<int:room_id>/edit/', views.room_edit_form, name='room_edit_form'),
    path('room/create/', views.room_create_form, name='room_create_form'),

    path('setting/', views.dashboard_setting_view, name='setting_page'),
    path('setting/tag_management/', views.Tag_management_setting, name='tag_management_page'),
    path('tags/bulk_delete/', views.bulk_delete_tags, name='bulk_delete_tags')
]