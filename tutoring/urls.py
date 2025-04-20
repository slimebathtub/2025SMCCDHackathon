from django.urls import path
from .views import tutoring_table

urlpatterns = [
    path("", tutoring_table, name="tutoring"),
]