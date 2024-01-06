from rest_framework import serializers
from .models import DataEntry


class DataEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataEntry
        fields = '__all__'


class PredictionSerializer(serializers.Serializer):
    continuous_feature1 = serializers.FloatField(default=0)
    continuous_feature2 = serializers.FloatField(default=0)
