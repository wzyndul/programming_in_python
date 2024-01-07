from django.db import models


class DataEntry(models.Model):
    continuous_feature1 = models.FloatField()
    continuous_feature2 = models.FloatField()
    categorical_feature = models.IntegerField()
