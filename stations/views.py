import time
from datetime import datetime
from django.db.models import Min, Max, Sum
from django.shortcuts import render, get_object_or_404
from stations.models import Station, Data
from django.shortcuts import render_to_response
from chartit import DataPool, Chart
import simplejson

def home(request):
    stations = Station.objects.all()
    data = Data.objects.order_by('datetime')
    lastdata = data[0]
    datadays = data.filter(station_name = lastdata.station.name, datetime__year=lastdata.datetime.year, datetime__month=lastdata.datetime.month, datetime__day=lastdata.datetime.day)

    weatherdata = DataPool( series= [{'options': { 'source': datadays}, 'terms': [('datetime', lambda d: time.mktime(d.timetuple())), 'outtemp']}])
    #Step 2: Create the Chart object
    cht = Chart(datasource = weatherdata, series_options =[{'options': {'type': 'line', 'stacking': True}, 'terms': {'datetime': [ 'outtemp']}}],
                chart_options =
                {'title': {
                    'text': 'Weather Data of Boston and Houston'},
                 'xAxis': {
                     'title': {
                         'text': 'Month number'}}})

    #outtemp_min = datadays.values('datetime').annotate(min_outtemp= Min('outtemp')).order_by('min_outtemp')[0]
    outtemp_max = datadays.values('datetime').annotate(max_outtemp= Max('outtemp')).order_by('-max_outtemp')[0]
    extra = {'outtemp_max': outtemp_max}
#    return render_to_response('home.html', {'stations': stations, 'last_data': lastdata, 'datadays': datadays, 'extra': extra, 'temphomechart': cht})
    return render_to_response('home.html', {'temphomechart': cht})



def menu_view(request):
    stations = Station.objects.all()
    return render_to_response('menu.html', {'stations': stations})

def estacion_view(request, id_estacion):
    estaciones = Station.objects.all()
    est = get_object_or_404(Station, pk = id_estacion)
    data = Data.objects.filter(station=est)
    #data = Data.objects.filter( station_id = id_estacion )
    min_temp = Data.objects.aggregate(Min('outtemp'))
    max_temp = Data.objects.aggregate(Max('outtemp'))
    template = "home.html"
    return render_to_response(template,locals())

# def temp_home_chart_view(request):
#     #Step 1: Create a DataPool with the data we want to retrieve.
#     data = Data.objects.order_by('datetime')
#     lastdata = data[0]
#     datadays = data.filter(station_name = lastdata.station.name, datetime__year=lastdata.datetime.year, datetime__month=lastdata.datetime.month)
#     weatherdata = DataPool( series= [{'options': { 'source': Station.objects.all()}, 'terms': ['name', 'lat', 'lg']}])
#     #Step 2: Create the Chart object
#     cht = Chart(datasource = weatherdata, series_options =[{'options':{'type': 'line','stacking': True},'terms':{'name': [ 'lat','lg']}}],
#                 chart_options =
#                 {'title': {
#                     'text': 'Weather Data of Boston and Houston'},
#                  'xAxis': {
#                      'title': {
#                          'text': 'Month number'}}})
#
#     #Step 3: Send the chart object to the template.
#     return render_to_response("home.html",{'temphomechart': cht})