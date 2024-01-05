# myapp/urls.py
from django.urls import path
from .views import home, add_data

urlpatterns = [
    path('', home, name='home'),
    path('add/', add_data, name='add_data'),
]
