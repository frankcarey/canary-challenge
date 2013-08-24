from django.contrib import admin
from canary.models import Customer
from canary.models import Device
from canary.models import Temperature

admin.site.register(Customer)
admin.site.register(Device)
admin.site.register(Temperature)
