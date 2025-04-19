from django.urls import path
from .views import resources_view

urlpatterns = [
    path('resources/', resources_view, name='resources'),
]