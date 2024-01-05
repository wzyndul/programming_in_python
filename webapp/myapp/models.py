from django.db import models

class DataEntry(models.Model): #TODO for now it has just 2 features
    continuous_feature1 = models.FloatField()
    continuous_feature2 = models.FloatField()
    categorical_feature = models.IntegerField()