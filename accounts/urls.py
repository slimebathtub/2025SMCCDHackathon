from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('login/', views.login_page, name='login'),


]




urlpatterns += staticfiles_urlpatterns()