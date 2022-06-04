from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    
    path('', include('prode.urls')),
    path('admin/', admin.site.urls),
    
    # the whole application home is loaded once all views are loaded
    path('', views.app_home, name='app-home'),
]
