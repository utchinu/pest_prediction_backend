from django.db import models


class Tutorial(models.Model):
    date = models.DateTimeField(blank=True)
    crop = models.CharField(max_length=200,blank=True)
    pest = models.CharField(max_length=200,blank=True)
    state_name = models.CharField(max_length=200,blank=True)
    district_name = models.CharField(max_length=200,blank=True)
    lattitude = models.FloatField(blank=True)
    longitude = models.FloatField(blank=True)
    count = models.IntegerField(blank=True)