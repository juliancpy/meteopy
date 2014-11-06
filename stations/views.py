import cgi
import datetime
import urllib2
from django.db.models import Min, Max, Sum
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404
from stations.models import Station, Data, Link
from django.shortcuts import render_to_response

# Calculo de conversion de un valor de temperatura F a C.
def convert_celsius(data):
    value = (data-32)*5/9
    return value

def home(request, id_estacion=1):
    TO_KMPH = 1.609344
    stations = Station.objects.all()
    links = Link.objects.all()
    sttn = get_object_or_404(Station, pk=id_estacion)
    try:
        data = Data.objects.filter(station=sttn).latest('datetime')
    except Data.DoesNotExist:
        return HttpResponseNotFound('<h1>No se encontraron DATOS para esta estacion</h1>')
    if data:
        datadays = Data.objects.filter(station_name=data.station.name, datetime__year=data.datetime.year,
                               datetime__month=data.datetime.month, datetime__day=data.datetime.day)
        rain_day = Data.objects.filter(datetime__year=data.datetime.year, datetime__month=data.datetime.month,
                                       datetime__day=data.datetime.day).values('station_name').annotate(Sum('rain'))


        url ='http://www.meteorologia.gov.py/interior.php?depto=' + str(data.station.departamento)
        r = urllib2.urlopen(url)
        _, params = cgi.parse_header(r.headers.get('Content-Type', ''))
        encoding = params.get('charset', 'iso-8859-1')
        unicode_text = r.read().decode(encoding)

        #
        # Calculos de maximos y minimos para temperatura, velocidad del viento y las precipitaciones
        #
        outtemp_min = datadays.values('datetime').annotate(val=Min('outtemp')).order_by('val')[0]
        # Convertimos el valor obtindo a celsius.
        outtemp_min['val']=convert_celsius(outtemp_min['val'])
        outtemp_max = datadays.values('datetime').annotate(val=Max('outtemp')).order_by('-val')[0]
        # Convertimos el valor obtindo a celsius.
        outtemp_max['val']=convert_celsius(outtemp_max['val'])
        windspeed_max = datadays.values('datetime').annotate(val=Max('windspeed')).order_by('-val')[0]
        # Convertimos el valor obtindo de mph a kmph
        windspeed_max['val']=windspeed_max['val']*TO_KMPH
        # precipitacion acumulada del dia.
        rain_day_acum = Data.objects.filter(datetime__year=data.datetime.year, datetime__month=data.datetime.month,datetime__day=data.datetime.day, station_name=data.station_name).values('station_name').annotate(val=Sum('rain'))
        extra = {'outtemp_max': outtemp_max, 'outtemp_min': outtemp_min, 'windspeed_max': windspeed_max,'rain_day_acum':rain_day_acum}

    else:
        return HttpResponseNotFound('<h1>No se encontraron DATOS para esta estacion</h1>')



    return render_to_response('home.html', { 'stations': stations, 'datadays':datadays, 'last_data': data, 'extra': extra,'rain_day': rain_day, 'pronos': unicode_text, 'links':links})

#Data.objects.filter(datetime__year='2013', datetime__month='10', datetime__day='13').values('station_name').annotate(Sum('rain'))

def menu_view(request):
    stations = Station.objects.all()
    return render_to_response('menu.html', {'stations': stations})
