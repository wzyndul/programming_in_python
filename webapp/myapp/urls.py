# myapp/urls.py
from django.urls import path
from .views import home, add, delete

urlpatterns = [
    path('', home, name='home'),
    path('add/', add, name='add'),
    path('delete/<int:record_id>/', delete, name='delete'),
]
