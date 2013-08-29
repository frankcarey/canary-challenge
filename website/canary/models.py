from django.db import models
import datetime

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Device(models.Model):
    serial = models.CharField(max_length=200)
    privacyMode = models.BooleanField()
    customer =  models.ForeignKey(Customer)
    def __unicode__(self):
        return self.serial

class Temperature(models.Model):
    data = models.IntegerField()
    timestamp = models.DateTimeField(blank=True)
    device = models.ForeignKey(Device)
    def save(self, *args, **kwargs):
        # Create a timestamp if one is not given.
        if (not self.timestamp):
            self.timestamp = datetime.datetime.today()
        return super(Temperature, self).save(*args, **kwargs)
    def __unicode__(self):
        return unicode(self.data)


