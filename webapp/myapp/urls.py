# myapp/urls.py
from django.urls import path
from .views import home, add, delete, api_get_data

urlpatterns = [
    path('', home, name='home'),
    path('add/', add, name='add'),
    path('delete/<int:record_id>/', delete, name='delete'),
path('api/data/', api_get_data, name='api_get_data'),
]
