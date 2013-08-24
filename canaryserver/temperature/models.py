from django.db import models

# Create your models here.

class Temperature(models.Modle):
    data = models.IntegerField(default=null)
    timestamp = models.DateTimeField()
