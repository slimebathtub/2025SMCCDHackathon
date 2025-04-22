from django.urls import path
from .views import room_list_view

urlpatterns = [
    path('', room_list_view, name='rooms-list'),
]