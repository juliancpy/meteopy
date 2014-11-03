import cgi
import datetime
import urllib2
from django.db.models import Min, Max, Sum
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404
from stations.models import Station, Data
from django.shortcuts import render_to_response



def home(request, id_estacion=1):
    stations = Station.objects.all()
    sttn = get_object_or_404(Station, pk=id_estacion)
    try:
        data = Data.objects.filter(station=sttn).latest('datetime')
    except Data.DoesNotExist:
        return HttpResponseNotFound('<h1>No se encontraron DATOS para esta estacion</h1>')
    if data:
        datadays = Data.objects.filter(station_name=data.station.name, datetime__year=data.datetime.year,
                               datetime__month=data.datetime.month, datetime__day=data.datetime.day)
        extra = {'temp_min': 'mint', 'temp_max': 'maxt'}
        rain_day = Data.objects.filter(datetime__year=data.datetime.year, datetime__month=data.datetime.month,datetime__day=data.datetime.day).values('station_name').annotate(Sum('rain'))

        url ='http://www.meteorologia.gov.py/interior.php?depto=' + str(data.station.departamento)
        r = urllib2.urlopen(url)
        _, params = cgi.parse_header(r.headers.get('Content-Type', ''))
        encoding = params.get('charset', 'iso-8859-1')
        unicode_text = r.read().decode(encoding)

        #extra = datadays.raw('select id, min(outtemp)as mint, max(outtemp) as maxt from stations_data where day(datetime) = day(%s)', [lastdata.datetime])[0]

    else:
        return HttpResponseNotFound('<h1>No se encontraron DATOS para esta estacion</h1>')

    #temp_min = lastdata.outtemp_min['min']

    #extra = {'tem_min': temp_min}
    #outtemp_min = datadays.values('datetime').annotate(min_outtemp= Min('outtemp')).order_by('min_outtemp')[0]
    #outtemp_max = datadays.values('datetime').annotate(max_outtemp= Max('outtemp')).order_by('-max_outtemp')[0]
    #extra = {'outtemp_max': outtemp_max, 'outtemp_min': outtemp_min}
    #return render_to_response('base.html', { 'last_data': lastdata, 'datadays': datadays, 'extra':extra })

    return render_to_response('home.html', { 'stations': stations, 'datadays':datadays, 'last_data': data, 'extra': extra,'rain_day': rain_day, 'pronos': unicode_text})

#Data.objects.filter(datetime__year='2013', datetime__month='10', datetime__day='13').values('station_name').annotate(Sum('rain'))

def menu_view(request):
    stations = Station.objects.all()
    return render_to_response('menu.html', {'stations': stations})
