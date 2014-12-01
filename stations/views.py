import cgi
import urllib2
import json
import pprint
import calendar
import pytz
import csv
from datetime import datetime, timedelta, date, time

from django.db.models import Min, Max, Sum
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.core.serializers.json import DjangoJSONEncoder
from django.template import loader, Context

from stations.models import Station, Data, Link
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


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

        # http://stackoverflow.com/questions/1317714/how-can-i-filter-a-date-of-a-datetimefield-in-django
        # http://stackoverflow.com/questions/7217811/query-datetime-by-todays-date-in-django
        # http://stackoverflow.com/questions/6040175/datetime-and-date-comparison-in-django-queryset
        # mysql buscar fecha como texto
        # http://stackoverflow.com/questions/14104304/mysql-select-where-datetime-matches-day-and-not-necessarily-time

        dia_hora_min = datetime.combine(data.datetime.date(), time.min)
        dia_hora_max = datetime.combine(data.datetime.date(), time.max)
        Data.objects.filter(station=sttn, datetime__range=(dia_hora_min, dia_hora_max))

        #ultimosRegistros = Data.objects.filter(station=sttn, datetime__year=data.datetime.year, datetime__month=data.datetime.month,
        #                                datetime__day=data.datetime.day)

        ultimosRegistros = Data.objects.filter(station=sttn, datetime__range=(dia_hora_min, dia_hora_max))


        # se coloca un order_by() vacio pues el modelo tiene una clase Meta con order by 'datetime'
        # rain_day = Data.objects.filter(station=sttn, datetime__year=data.datetime.year, datetime__month=data.datetime.month,
        #                                 datetime__day=data.datetime.day).values('station').annotate(Count('rain')).order_by()


        # totalLluviaDia = ultimosRegistros.values('station').annotate(val = Sum('rain')).order_by()[0]['val']
        # minTempDia = ultimosRegistros.values('datetime').annotate(val=Min('outtemp')).order_by('val')[0]
        # pprint.pprint(minTempDia.outtemp)
        # maxTempDia = ultimosRegistros.values('station').annotate(val = Max('outtemp')).order_by()[0]['val']

        totalLluviaDia = ultimosRegistros.aggregate(val = Sum('rain'))['val']*25.4
        minTempDia = ultimosRegistros.aggregate(val = Min('outtemp'))['val']
        maxTempDia = ultimosRegistros.aggregate(val = Max('outtemp'))['val']

        maxVelVientoDia = ultimosRegistros.aggregate(val = Max('windspeed'))['val']

        #pprint.pprint(maxVelVientoDia)

        # dirMaxVelVientoDia = Data.objects.filter(station=sttn, datetime__year=data.datetime.year, datetime__month=data.datetime.month,
        #                                          datetime__day=data.datetime.day, windspeed=maxVelVientoDia).order_by('-datetime')[0].winddir

        try:
            dataMaxVelVientoDia = Data.objects.filter(station=sttn, datetime__range=(dia_hora_min, dia_hora_max), windspeed=maxVelVientoDia).order_by('-datetime')[0]

            dataMinTempDia = Data.objects.filter(station=sttn, datetime__range=(dia_hora_min, dia_hora_max), outtemp=minTempDia).order_by('-datetime')[0]

            dataMaxTempDia = Data.objects.filter(station=sttn, datetime__range=(dia_hora_min, dia_hora_max), outtemp=maxTempDia).order_by('-datetime')[0]
        except IndexError:
            dataMaxTempDia = None
            dataMinTempDia = None
            dataMaxVelVientoDia = None

        url ='http://www.meteorologia.gov.py/interior.php?depto=' + str(data.station.departamento)
        r = urllib2.urlopen(url)
        _, params = cgi.parse_header(r.headers.get('Content-Type', ''))
        encoding = params.get('charset', 'iso-8859-1')
        unicode_text = r.read().decode(encoding)

        # desde = datetime.strptime('2012-01-31', '%Y-%m-%d')
        # desde = desde.replace(hour=00, minute=01)
        #
        # hasta = datetime.strptime('2012-02-01', '%Y-%m-%d')
        # hasta = hasta.replace(hour=23, minute=59)

        #http://stackoverflow.com/questions/2278076/count-number-of-records-by-date-in-django/2283913#2283913
        #lluvia = Data.objects.filter(datetime__gt = desde, datetime__lt = hasta).extra({'date_rain' : "date(datetime)"}).values('date_rain').annotate(rain_sum=Sum('rain')).order_by()

        #pprint.pprint(lluvia)


        extra = {
            'outtemp_max': dataMaxTempDia,
            'outtemp_min' : dataMinTempDia,
            'windspeed_max' : dataMaxVelVientoDia,
            'rain_day_acum' : totalLluviaDia,
        }

        respuesta = {
            'stations': stations,
            'datadays':ultimosRegistros,
            'last_data': data,
            'extra': extra,
            'rain_day': totalLluviaDia,
            'pronos': unicode_text,
            'links':links
        }

        return render_to_response('home.html', respuesta)

    else:
        return HttpResponseNotFound('<h1>No se encontraron DATOS para esta estacion</h1>')

#Data.objects.filter(datetime__year='2013', datetime__month='10', datetime__day='13').values('station_name').annotate(Sum('rain'))

def menu_view(request):
    stations = Station.objects.all()
    return render_to_response('menu.html', {'stations': stations})

def reporte(request):
    stations = Station.objects.all()
    return render_to_response('reporte.html', {'stations' : stations})

@csrf_exempt
def reporte_generar(request):

    reporte = reporte_generar_datos(request)

    template = loader.get_template('reporte-tabla.html')
    c = Context({ 'datos': reporte['datos'], 'titulos' : reporte['titulos'] })
    rendered = template.render(c)

    response_data = {}
    response_data['status'] = 'ok'
    response_data['data'] = rendered

    return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")

@csrf_exempt
def reporte_generar_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response

# metodo privado que genera los datos de los reportes
def reporte_generar_datos(request):

    campo_estaciones = request.POST.get("rep_estaciones", "all")
    campo_atributos = request.POST.get("rep_atributos", "outtemp")
    campo_informe = request.POST.get("rep_informe", "mes")

    #campo_desde = request.POST.get("rep_desde", datetime.today().strftime("%Y-%m-%d"))
    campo_desde = request.POST.get("rep_desde", '2014-11-17')
    campo_desde = datetime.strptime(campo_desde, '%Y-%m-%d')
    campo_desde = campo_desde.replace(hour=00, minute=01)

    #campo_hasta = request.POST.get("rep_hasta", datetime.today().strftime("%Y-%m-%d"))
    campo_hasta = request.POST.get("rep_hasta", '2014-11-17')
    campo_hasta = datetime.strptime(campo_hasta, '%Y-%m-%d')
    campo_hasta = campo_hasta.replace(hour=23, minute=59)

    titulos_nombres = {'winddir' : 'Viento Direccion', 'et' : 'Radiacion Solar', 'outhumidity' : 'Humedad', 'rain' : 'Lluvia', 'barometer' : 'Barometro', 'outtemp' : 'Temperatura', 'heatindex' : 'Sensacion Termica', 'uv' : 'Ultravioleta'}

    pprint.pprint(campo_estaciones)

    if (campo_estaciones != 'all'):
        filtro_estaciones = Q(station_id__in=campo_estaciones.split(','))
    else:
        filtro_estaciones = Q(pk__gt=0)

    filtro_desde = Q(datetime__gt = campo_desde)
    filtro_hasta = Q(datetime__lt = campo_hasta)

    datos = list(Data.objects.filter(filtro_estaciones, filtro_desde, filtro_hasta))

    result = []

    if (campo_informe == 'all'):
        # codigo para datos sin promedio
        for d in datos:
            fila = {'fecha' : d.datetime.strftime("%Y-%m-%d %H:%M:%S")}

            for campo in campo_atributos.split(','):
                fila[campo] = d.__dict__[campo]

            result.append(fila)
    else:
        if (campo_informe == 'hora'):
            campo_informe = '%Y-%m-%d %H'

        if (campo_informe == 'dia'):
            campo_informe = '%Y-%m-%d'

        if (campo_informe == 'mes'):
            campo_informe = '%Y-%m'

        promedios = {}

        # generar sumatoria de datos
        for d in datos:
            agrupacion = d.datetime.strftime(campo_informe)

            if (agrupacion in promedios):
                promedios[agrupacion]['cantidad'] += 1
                promedios[agrupacion]['winddir']   += (d.winddir if d.winddir != None else 0)
                promedios[agrupacion]['et']        += (d.et if d.et != None else 0)
                promedios[agrupacion]['outhumidity'] += (d.outhumidity if d.outhumidity != None else 0)
                promedios[agrupacion]['rain']      += (d.rain if d.rain != None else 0)
                promedios[agrupacion]['barometer'] += (d.barometer if d.barometer != None else 0)
                promedios[agrupacion]['outtemp']   += (d.outtemp if d.outtemp != None else 0)
                promedios[agrupacion]['heatindex'] += (d.heatindex if d.heatindex != None else 0)
                promedios[agrupacion]['soiltemp1'] += (d.soiltemp1 if d.soiltemp1 != None else 0)
                promedios[agrupacion]['et']        += (d.et if d.et != None else 0)
                promedios[agrupacion]['heatindex'] += (d.heatindex if d.heatindex != None else 0)
                promedios[agrupacion]['uv']        += (d.uv if d.uv != None else 0)

            else:
                promedios[agrupacion] = {}
                promedios[agrupacion]['cantidad'] = 1
                promedios[agrupacion]['winddir']   = (d.winddir if d.winddir != None else 0)
                promedios[agrupacion]['et']        = (d.et if d.et != None else 0)
                promedios[agrupacion]['outhumidity'] = (d.outhumidity if d.outhumidity != None else 0)
                promedios[agrupacion]['rain']      = (d.rain if d.rain != None else 0)
                promedios[agrupacion]['barometer'] = (d.barometer if d.barometer != None else 0)
                promedios[agrupacion]['outtemp']   = (d.outtemp if d.outtemp != None else 0)
                promedios[agrupacion]['heatindex'] = (d.heatindex if d.heatindex != None else 0)
                promedios[agrupacion]['soiltemp1'] = (d.soiltemp1 if d.soiltemp1 != None else 0)
                promedios[agrupacion]['et']        = (d.et if d.et != None else 0)
                promedios[agrupacion]['heatindex'] = (d.heatindex if d.heatindex != None else 0)
                promedios[agrupacion]['uv']        = (d.uv if d.uv != None else 0)

        # calcular promedio
        for indice in promedios:
            promedios[indice]['winddir']     = promedios[indice]['winddir'] / promedios[indice]['cantidad']
            promedios[indice]['et']          = promedios[indice]['et'] / promedios[indice]['cantidad']
            promedios[indice]['outhumidity'] = promedios[indice]['outhumidity'] / promedios[indice]['cantidad']
            promedios[indice]['rain']        = promedios[indice]['rain'] / promedios[indice]['cantidad']
            promedios[indice]['barometer']   = promedios[indice]['barometer'] / promedios[indice]['cantidad']
            promedios[indice]['outtemp']     = promedios[indice]['outtemp'] / promedios[indice]['cantidad']
            promedios[indice]['heatindex']   = promedios[indice]['heatindex'] / promedios[indice]['cantidad']
            promedios[indice]['soiltemp1']   = promedios[indice]['soiltemp1'] / promedios[indice]['cantidad']
            promedios[indice]['et']          = promedios[indice]['et'] / promedios[indice]['cantidad']
            promedios[indice]['heatindex']   = promedios[indice]['heatindex'] / promedios[indice]['cantidad']
            promedios[indice]['uv']          = promedios[indice]['uv'] / promedios[indice]['cantidad']

        for indice in promedios:
            fila = promedios[indice]
            fila['fecha'] = indice
            result.append(fila)

    filas = []
    titulos = ['Fecha']
    #pprint.pprint(result)

    for campo in campo_atributos.split(','):
            titulos.append(titulos_nombres[campo])

    for registro in result:
        fila = []
        fila.append(registro['fecha'])
        for campo in campo_atributos.split(','):
            fila.append(registro[campo])

        filas.append(fila)

    #pprint.pprint(filas)
    return { 'datos': filas, 'titulos' : titulos }


def details_view(request, id_estacion=1):
    TO_KMPH = 1.609344
    stations = Station.objects.all()
    links = Link.objects.all()
    sttn = get_object_or_404(Station, pk=id_estacion)

    try:
        data = Data.objects.filter(station=sttn).latest('datetime')
    except Data.DoesNotExist:
        return HttpResponseNotFound('<h1>No se encontraron DATOS para esta estacion</h1>')

    if data:
        dia_hora_min = datetime.combine(data.datetime.date(), time.min)
        dia_hora_max = datetime.combine(data.datetime.date(), time.max)
        Data.objects.filter(station=sttn, datetime__range=(dia_hora_min, dia_hora_max))

        ultimosRegistros = Data.objects.filter(station=sttn, datetime__range=(dia_hora_min, dia_hora_max))

        totalLluviaDia = ultimosRegistros.aggregate(val = Sum('rain'))['val']*25.4
        minTempDia = ultimosRegistros.aggregate(val = Min('outtemp'))['val']
        maxTempDia = ultimosRegistros.aggregate(val = Max('outtemp'))['val']
        minHumDia = ultimosRegistros.aggregate(val = Min('outhumidity'))['val']
        maxHumDia = ultimosRegistros.aggregate(val = Max('outhumidity'))['val']

        maxVelVientoDia = ultimosRegistros.aggregate(val = Max('windspeed'))['val']

        try:
            dataMaxVelVientoDia = Data.objects.filter(station=sttn, datetime__range=(dia_hora_min, dia_hora_max), windspeed=maxVelVientoDia).order_by('datetime')[0]

            dataMinTempDia = Data.objects.filter(station=sttn, datetime__range=(dia_hora_min, dia_hora_max), outtemp=minTempDia).order_by('-datetime')[0]

            dataMaxTempDia = Data.objects.filter(station=sttn, datetime__range=(dia_hora_min, dia_hora_max), outtemp=maxTempDia).order_by('-datetime')[0]
            dataMinHumDia = Data.objects.filter(station=sttn, datetime__range=(dia_hora_min, dia_hora_max), outhumidity=minHumDia).order_by('-datetime')[0]
            dataMaxHumDia = Data.objects.filter(station=sttn, datetime__range=(dia_hora_min, dia_hora_max), outhumidity=maxHumDia).order_by('datetime')[0]
        except IndexError:
            dataMaxTempDia = None
            dataMinTempDia = None
            dataMaxVelVientoDia = None
            dataMinHumDia = None
            dataMaxHumDia = None



        extra = {
            'outtemp_max': dataMaxTempDia,
            'outtemp_min': dataMinTempDia,
            'windspeed_max': dataMaxVelVientoDia,
            'humidity_max': dataMaxHumDia,
            'humidity_min': dataMinHumDia,
            'rain_day_acum': totalLluviaDia,
        }

    else:
        return HttpResponseNotFound('<h1>No se encontraron DATOS para esta estacion</h1>')
    return render_to_response('details.html', {'stations': stations,'links':links, 'data': data,'extra': extra, 'id':id_estacion})
