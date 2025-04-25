from django.urls import path
from .views import clubs_table

urlpatterns = [
    path("", clubs_table, name="clubs_table"),
    ]