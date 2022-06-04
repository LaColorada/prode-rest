from django.urls import path

from prode import views

urlpatterns = [
    path('', views.home, name='home')
]
