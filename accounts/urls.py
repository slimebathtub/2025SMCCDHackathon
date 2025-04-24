from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from .views import login_page, home
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('home/', home, name='home'),
    path('admin/', admin.site.urls),
    path ('login/', login_page, name='login_page'),
]




urlpatterns += staticfiles_urlpatterns()