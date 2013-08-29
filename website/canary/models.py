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
    def save(self, *args, **kwargs):
        # Publish the update to redis.
        import redis, json
        redisClient = redis.Redis()
        redisClient.publish('device.' + self.serial, json.dumps({'privacyMode': self.privacyMode}))
        return super(Device, self).save(*args, **kwargs)


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


