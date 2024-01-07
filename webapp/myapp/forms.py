from django import forms
from .models import DataEntry


class DataEntryForm(forms.ModelForm):
    class Meta:
        model = DataEntry
        fields = ['continuous_feature1', 'continuous_feature2', 'categorical_feature']
