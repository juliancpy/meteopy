# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from daterange_filter.filter import DateRangeFilter
from django.db.models import Min, Sum


class Station(models.Model):
    name = models.CharField(max_length=255)
    path_db = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    lat = models.FloatField()
    lg = models.FloatField()


class StationAdmin(admin.ModelAdmin):
    list_display = ('name','zone','path_db','lat','lg')
    list_filter = ('zone', 'path_db')




class Data(models.Model):
    datetime = models.DateTimeField(db_column='dateTime')  # Field name made lowercase.
    usunits = models.IntegerField(db_column='usUnits')  # Field name made lowercase.
    interval = models.IntegerField()
    barometer = models.FloatField(blank=True, null=True)
    pressure = models.FloatField(blank=True, null=True)
    altimeter = models.FloatField(blank=True, null=True)
    intemp = models.FloatField(db_column='inTemp', blank=True, null=True)  # Field name made lowercase.
    outtemp = models.FloatField(db_column='outTemp', blank=True, null=True)  # Field name made lowercase.
    inhumidity = models.FloatField(db_column='inHumidity', blank=True, null=True)  # Field name made lowercase.
    outhumidity = models.FloatField(db_column='outHumidity', blank=True, null=True)  # Field name made lowercase.
    windspeed = models.FloatField(db_column='windSpeed', blank=True, null=True)  # Field name made lowercase.
    winddir = models.FloatField(db_column='windDir', blank=True, null=True)  # Field name made lowercase.
    windgust = models.FloatField(db_column='windGust', blank=True, null=True)  # Field name made lowercase.
    windgustdir = models.FloatField(db_column='windGustDir', blank=True, null=True)  # Field name made lowercase.
    rainrate = models.FloatField(db_column='rainRate', blank=True, null=True)  # Field name made lowercase.
    rain = models.FloatField(blank=True, null=True)
    dewpoint = models.FloatField(blank=True, null=True)
    windchill = models.FloatField(blank=True, null=True)
    heatindex = models.FloatField(blank=True, null=True)
    et = models.FloatField(db_column='ET', blank=True, null=True)  # Field name made lowercase.
    radiation = models.FloatField(blank=True, null=True)
    uv = models.FloatField(db_column='UV', blank=True, null=True)  # Field name made lowercase.
    extratemp1 = models.FloatField(db_column='extraTemp1', blank=True, null=True)  # Field name made lowercase.
    extratemp2 = models.FloatField(db_column='extraTemp2', blank=True, null=True)  # Field name made lowercase.
    extratemp3 = models.FloatField(db_column='extraTemp3', blank=True, null=True)  # Field name made lowercase.
    soiltemp1 = models.FloatField(db_column='soilTemp1', blank=True, null=True)  # Field name made lowercase.
    soiltemp2 = models.FloatField(db_column='soilTemp2', blank=True, null=True)  # Field name made lowercase.
    soiltemp3 = models.FloatField(db_column='soilTemp3', blank=True, null=True)  # Field name made lowercase.
    soiltemp4 = models.FloatField(db_column='soilTemp4', blank=True, null=True)  # Field name made lowercase.
    leaftemp1 = models.FloatField(db_column='leafTemp1', blank=True, null=True)  # Field name made lowercase.
    leaftemp2 = models.FloatField(db_column='leafTemp2', blank=True, null=True)  # Field name made lowercase.
    extrahumid1 = models.FloatField(db_column='extraHumid1', blank=True, null=True)  # Field name made lowercase.
    extrahumid2 = models.FloatField(db_column='extraHumid2', blank=True, null=True)  # Field name made lowercase.
    soilmoist1 = models.FloatField(db_column='soilMoist1', blank=True, null=True)  # Field name made lowercase.
    soilmoist2 = models.FloatField(db_column='soilMoist2', blank=True, null=True)  # Field name made lowercase.
    soilmoist3 = models.FloatField(db_column='soilMoist3', blank=True, null=True)  # Field name made lowercase.
    soilmoist4 = models.FloatField(db_column='soilMoist4', blank=True, null=True)  # Field name made lowercase.
    leafwet1 = models.FloatField(db_column='leafWet1', blank=True, null=True)  # Field name made lowercase.
    leafwet2 = models.FloatField(db_column='leafWet2', blank=True, null=True)  # Field name made lowercase.
    rxcheckpercent = models.FloatField(db_column='rxCheckPercent', blank=True, null=True)  # Field name made lowercase.
    txbatterystatus = models.FloatField(db_column='txBatteryStatus', blank=True, null=True)  # Field name made lowercase.
    consbatteryvoltage = models.FloatField(db_column='consBatteryVoltage', blank=True, null=True)  # Field name made lowercase.
    hail = models.FloatField(blank=True, null=True)
    hailrate = models.FloatField(db_column='hailRate', blank=True, null=True)  # Field name made lowercase.
    heatingtemp = models.FloatField(db_column='heatingTemp', blank=True, null=True)  # Field name made lowercase.
    heatingvoltage = models.FloatField(db_column='heatingVoltage', blank=True, null=True)  # Field name made lowercase.
    supplyvoltage = models.FloatField(db_column='supplyVoltage', blank=True, null=True)  # Field name made lowercase.
    referencevoltage = models.FloatField(db_column='referenceVoltage', blank=True, null=True)  # Field name made lowercase.
    windbatterystatus = models.FloatField(db_column='windBatteryStatus', blank=True, null=True)  # Field name made lowercase.
    rainbatterystatus = models.FloatField(db_column='rainBatteryStatus', blank=True, null=True)  # Field name made lowercase.
    outtempbatterystatus = models.FloatField(db_column='outTempBatteryStatus', blank=True, null=True)  # Field name made lowercase.
    intempbatterystatus = models.FloatField(db_column='inTempBatteryStatus', blank=True, null=True)  # Field name made lowercase.
    station_name = models.CharField(max_length=255)
    station = models.ForeignKey(Station)
    @property
    def outtemp_min(self):
        outtemp_min = {}
        outtemp_min = self.values('datetime').annotate(min_outtemp = Min('outtemp')).order_by('min_outtemp')[0]
        return 'outtemp'

    class Meta:
        ordering = ["datetime"]



class DataAdmin(admin.ModelAdmin):
    list_display = ('station_name','datetime','outtemp','outhumidity','rain','windspeed')
    list_filter = (
        'station_name', 
        ('datetime', DateRangeFilter),
    )

