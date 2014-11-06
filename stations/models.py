# coding=utf-8
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
    DEPTOS = ((1, 'Concepcion'), (2, 'San Pedro'),(3, 'Coridillera'),(4, 'Guairá'),(5, 'Caaguazú'),(6, 'Caazapa'),(7, 'Itapúa'),
              (8, 'Misiones'),(9, 'Paraguarí'),(10, 'Alto Parana'),(11, 'Central'),(12, 'Neembucu'),(13, 'Amambay'),(14, 'Canindeyú'),(15, 'Presidente Hayes'),(16, 'Alto Paraguay'),(17, 'Boqueron'),)
    name = models.CharField(max_length=255)
    path_db = models.CharField(max_length=255)
    departamento = models.IntegerField(unique=True, choices=DEPTOS, default=0)
    lat = models.FloatField()
    lg = models.FloatField()

    def __unicode__(self):
        return self.name

class StationAdmin(admin.ModelAdmin):
    list_display = ('id','name','departamento','path_db','lat','lg')
    list_filter = ('departamento', 'path_db')


class Link(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    help = models.CharField(max_length=255)
    def __unicode__(self):
        return self.title

class LinkAdmin(admin.ModelAdmin):
    list_display = ('id','title','link', 'help')
    list_filter = ('title','id')



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
    def outtemp_celsius(self):
        temp = self.outtemp
        new_temp=(temp-32)*5/9
        return new_temp
    def windspeed_kmh(self):
        speed = self.windspeed * 1.609
        return speed
    def rain_mm(self):
        rain = self.rain / 0.039370
        return rain

    def pressure_hpa(self):
        pressure = self.pressure * 33.86
        return pressure

    class Meta:
        ordering = ["datetime"]

    def __unicode__(self):
        return "%s " % self.datetime
    def get_wdir(self):
        dir = self.winddir
        direction=""
        if dir >= 11.25 and dir < 33.75:
            direction="NNE"
        elif dir >=33.75 and dir < 56.25:
            direction="NE"
        elif dir >=56.25 and dir < 78.75:
            direction="ENE"
        elif dir >=78.25 and dir < 101.25:
            direction="Este"
        elif dir >=101.25 and dir < 123.75:
            direction="ESE"
        elif dir >=123.75 and dir < 146.25:
            direction="SE"
        elif dir >=146.25 and dir < 168.75:
            direction="SSE"
        elif dir >=168.75 and dir < 191.25:
            direction="S"
        elif dir >=191.25 and dir < 213.75:
            direction="S"
        elif dir >=213.75 and dir < 236.25:
            direction="SSW"
        elif dir >=236.25 and dir < 258.75:
            direction="WSW"
        elif dir >=258.75 and dir < 281.25:
            direction="W"
        elif dir >=281.25 and dir < 303.75:
            direction="WNW"
        elif dir >=303.75 and dir < 326.25:
            direction="NW"
        elif dir >=326.25 and dir < 348.75:
            direction="NNW"
        else:
            direction="N"
        return "%s " % direction




class DataAdmin(admin.ModelAdmin):
    list_display = ('station_name','station', 'datetime','outtemp','outhumidity','rain','windspeed')
    list_filter = (
        'station_name', 
        ('datetime', DateRangeFilter),
    )

