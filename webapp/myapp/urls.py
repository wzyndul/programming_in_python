# myapp/urls.py
from django.urls import path
from .views import home, add, delete, api_data, predict, api_predictions

urlpatterns = [
    path('', home, name='home'),
    path('add', add, name='add'),
    path('delete/<int:record_id>', delete, name='delete'),
    path('api/data', api_data, name='api_data'),
    path('api/data/<int:record_id>', api_data, name='api_data'),
    path('predict', predict, name='predict'),
    path('api/predictions/', api_predictions, name='api_predictions'),
]
