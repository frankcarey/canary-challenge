from django.contrib import admin
from canary.models import Customer, Device, Temperature

class TemperatureInline(admin.TabularInline):
    model = Temperature
class DeviceInline(admin.TabularInline):
    model = Device
class CustomerAdmin(admin.ModelAdmin):
    inlines = [DeviceInline]
class DeviceAdmin(admin.ModelAdmin):
    inlines = [TemperatureInline]

admin.site.register(Device, DeviceAdmin)
admin.site.register(Customer, CustomerAdmin)
