from stations.models import *
from django.contrib import admin

admin.site.register(Station, StationAdmin)
admin.site.register(Data, DataAdmin)
