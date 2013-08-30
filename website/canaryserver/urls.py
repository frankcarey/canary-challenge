from django.conf.urls import patterns, include, url
from canary.models import Temperature, Device
from rest_framework import viewsets, routers
from rest_framework.routers import DefaultRouter

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# rest_framework ViewSets define the view behavior.
class TemperatureViewSet(viewsets.ModelViewSet):
    model = Temperature

# rest_framework ViewSets define the view behavior.
class DeviceViewSet(viewsets.ModelViewSet):
    model = Device
    filter_fields = ['serial']


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'temperatures', TemperatureViewSet)
router.register(r'devices', DeviceViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'canaryserver.views.home', name='home'),
    # url(r'^canaryserver/', include('canaryserver.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/', include(router.urls)),
)

