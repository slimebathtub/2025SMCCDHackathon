from django.urls import path
from .views import sourcepage_view
from resources import views

urlpatterns = [
    path('resources/', sourcepage_view, name='resources-list'),
    # path('items/', views.center_item_list, name='center_item_list'),
]