from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Device(models.Model):
    serial = models.CharField(max_length=200)
    customer =  models.ForeignKey(Customer)
    def __unicode__(self):
        return self.serial

class Temperature(models.Model):
    data = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(Device)

    def __unicode__(self):
        return unicode(self.data)


