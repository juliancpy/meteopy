import json
import pprint
import calendar
from datetime import datetime, timedelta


from django.db.models import Min, Max, Sum
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

from stations.models import Station, Data
from django.db.models import Q

def temperatura_historico(request, id_estacion = 1):

    try:
        station = Station.objects.get(pk=id_estacion)
    except Station.DoesNotExist:
        response_data = {}
        response_data['status'] = 'error'
        response_data['message'] = 'No existe la estacion indicada'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    # local_tz = pytz.timezone("America/Asuncion")
    # pprint.pprint(datetime.now().date())
    # pprint.pprint(datetime.fromtimestamp(1393671660).replace(tzinfo=local_tz))
    # datos = Data.objects.filter(datetime__lt = datetime.fromtimestamp(1393671660).replace(tzinfo=local_tz))
    # datos2 = Data.objects.filter(datetime__lt = datetime.fromtimestamp(1393671660).replace(tzinfo=local_tz)).values('pk', 'datetime', 'rain')
    # pprint.pprint(datos2)
    # pprint.pprint('hola mundo')

    # Date.UTC(year,month,day,hours,minutes,seconds,millisec)

    # pprint.pprint(datetime.strptime('2012-01-31', '%Y-%m-%d'))

    #datos = Data.objects.filter(datetime__lt = datetime.fromtimestamp(1393671660).replace(tzinfo=local_tz))
    #datos2 = Data.objects.filter(datetime__lt = datetime.fromtimestamp(1393671660).replace(tzinfo=local_tz)).values('pk', 'datetime', 'rain')

    # request.GET.get('q', '')
    desde = request.GET.get('desde', datetime.today().strftime("%Y-%m-%d"))
    desde = datetime.strptime(desde, '%Y-%m-%d')
    desde = desde.replace(hour=00, minute=01)
    pprint.pprint(desde)

    fechaHastaDefault = datetime.today() - timedelta(days=10)
    hasta = request.GET.get('hasta', fechaHastaDefault.strftime("%Y-%m-%d"))
    hasta = datetime.strptime(hasta, '%Y-%m-%d')
    hasta = hasta.replace(hour=23, minute=59)
    pprint.pprint(hasta)

    # forzar a que sea una lista el resultado para poder serializar - https://docs.djangoproject.com/en/dev/ref/models/querysets/
    datos = list(Data.objects.filter(station = station, datetime__gt = desde, datetime__lt = hasta).values('pk', 'datetime', 'rain', 'outtemp'))

    result = []

    for d in datos:
        result.append({'pk' : d['pk'], 'datetime' : calendar.timegm(datetime.timetuple(d['datetime'])), 'outtemp' : d['outtemp']})
        #result.append({'pk' : d['pk'], 'datetime' : d['datetime'].strftime('%Y-%m-%d %H:%M:%S'), 'outtemp' : d['outtemp']})

    response_data = {}
    response_data['status'] = 'ok'
    response_data['data'] = result

    return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")


def viento_historico(request, id_estacion = 1):

    try:
        station = Station.objects.get(pk=id_estacion)
    except Station.DoesNotExist:
        response_data = {}
        response_data['status'] = 'error'
        response_data['message'] = 'No existe la estacion indicada'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    desde = request.GET.get('desde', datetime.today().strftime("%Y-%m-%d"))
    desde = datetime.strptime(desde, '%Y-%m-%d')
    desde = desde.replace(hour=00, minute=01)
    pprint.pprint(desde)

    fechaHastaDefault = datetime.today() - timedelta(days=10)
    hasta = request.GET.get('hasta', fechaHastaDefault.strftime("%Y-%m-%d"))
    hasta = datetime.strptime(hasta, '%Y-%m-%d')
    hasta = hasta.replace(hour=23, minute=59)
    pprint.pprint(hasta)

    # forzar a que sea una lista el resultado para poder serializar - https://docs.djangoproject.com/en/dev/ref/models/querysets/
    datos = list(Data.objects.filter(~Q(windspeed=None), station = station,  datetime__gt = desde, datetime__lt = hasta))

    result = []

    for d in datos:
        result.append({'pk' : d.pk, 'datetime' : calendar.timegm(datetime.timetuple(d.datetime)) * 1000, 'windspeed' : d.windspeed_kmh})

    response_data = {}
    response_data['status'] = 'ok'
    response_data['data'] = result

    return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")


def viento_direccion_historico(request, id_estacion = 1):

    try:
        station = Station.objects.get(pk=id_estacion)
    except Station.DoesNotExist:
        response_data = {}
        response_data['status'] = 'error'
        response_data['message'] = 'No existe la estacion indicada'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    desde = request.GET.get('desde', datetime.today().strftime("%Y-%m-%d"))
    desde = datetime.strptime(desde, '%Y-%m-%d')
    desde = desde.replace(hour=00, minute=01)
    pprint.pprint(desde)

    fechaHastaDefault = datetime.today() - timedelta(days=10)
    hasta = request.GET.get('hasta', fechaHastaDefault.strftime("%Y-%m-%d"))
    hasta = datetime.strptime(hasta, '%Y-%m-%d')
    hasta = hasta.replace(hour=23, minute=59)
    pprint.pprint(hasta)

    # forzar a que sea una lista el resultado para poder serializar - https://docs.djangoproject.com/en/dev/ref/models/querysets/
    datos = list(Data.objects.filter(station = station, datetime__gt = desde, datetime__lt = hasta))

    result = []

    for d in datos:
        result.append({'pk' : d.pk, 'datetime' : calendar.timegm(datetime.timetuple(d.datetime)) * 1000, 'winddir' : d.winddir})

    response_data = {}
    response_data['status'] = 'ok'
    response_data['data'] = result

    return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")


def precipitacion_historico(request, id_estacion = 1):

    try:
        station = Station.objects.get(pk=id_estacion)
    except Station.DoesNotExist:
        response_data = {}
        response_data['status'] = 'error'
        response_data['message'] = 'No existe la estacion indicada'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    desde = request.GET.get('desde', datetime.today().strftime("%Y-%m-%d"))
    desde = datetime.strptime(desde, '%Y-%m-%d')
    desde = desde.replace(hour=00, minute=01)
    pprint.pprint(desde)

    fechaHastaDefault = datetime.today() - timedelta(days=10)
    hasta = request.GET.get('hasta', fechaHastaDefault.strftime("%Y-%m-%d"))
    hasta = datetime.strptime(hasta, '%Y-%m-%d')
    hasta = hasta.replace(hour=23, minute=59)
    pprint.pprint(hasta)

    # forzar a que sea una lista el resultado para poder serializar - https://docs.djangoproject.com/en/dev/ref/models/querysets/
    datos = list(Data.objects.filter(station = station, datetime__gt = desde, datetime__lt = hasta))

    result = []

    for d in datos:
        result.append({'pk' : d.pk, 'datetime' : calendar.timegm(datetime.timetuple(d.datetime)) * 1000, 'rain_mm' : d.rain_mm})

    response_data = {}
    response_data['status'] = 'ok'
    response_data['data'] = result

    return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")

def precipitacion_acumulado_dia(request, id_estacion = 1):

    try:
        station = Station.objects.get(pk=id_estacion)
    except Station.DoesNotExist:
        response_data = {}
        response_data['status'] = 'error'
        response_data['message'] = 'No existe la estacion indicada'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    desde = request.GET.get('desde', datetime.today().strftime("%Y-%m-%d"))
    desde = datetime.strptime(desde, '%Y-%m-%d')
    desde = desde.replace(hour=00, minute=01)
    pprint.pprint(desde)

    fechaHastaDefault = datetime.today() - timedelta(days=10)
    hasta = request.GET.get('hasta', fechaHastaDefault.strftime("%Y-%m-%d"))
    hasta = datetime.strptime(hasta, '%Y-%m-%d')
    hasta = hasta.replace(hour=23, minute=59)
    pprint.pprint(hasta)

    # http://stackoverflow.com/questions/2278076/count-number-of-records-by-date-in-django/2283913#2283913
    datos = list(Data.objects.filter(station = station, datetime__gt = desde, datetime__lt = hasta).extra({'date_rain' : "date(datetime)"}).values('date_rain').annotate(rain_sum=Sum('rain')).order_by())

    dias = []
    valores = []

    for d in datos:
        dato_fecha = datetime.strptime(d['date_rain'].isoformat(), '%Y-%m-%d')
        dias.append(dato_fecha.strftime('%b %d'))
        valores.append(d['rain_sum'])

    response_data = {}
    response_data['status'] = 'ok'
    response_data['data'] = {'dias' : dias, 'valores' : valores}

    return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")

def viento_conteo_direccion(request, id_estacion = 1):

    try:
        station = Station.objects.get(pk=id_estacion)
    except Station.DoesNotExist:
        response_data = {}
        response_data['status'] = 'error'
        response_data['message'] = 'No existe la estacion indicada'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    desde = request.GET.get('desde', datetime.today().strftime("%Y-%m-%d"))
    desde = datetime.strptime(desde, '%Y-%m-%d')
    desde = desde.replace(hour=00, minute=01)

    fechaHastaDefault = datetime.today() - timedelta(days=1)
    hasta = request.GET.get('hasta', fechaHastaDefault.strftime("%Y-%m-%d"))
    hasta = datetime.strptime(hasta, '%Y-%m-%d')
    hasta = hasta.replace(hour=23, minute=59)

    pprint.pprint(desde)
    pprint.pprint(hasta)

    # forzar a que sea una lista el resultado para poder serializar - https://docs.djangoproject.com/en/dev/ref/models/querysets/
    datos = list(Data.objects.filter(station = station, datetime__gt = desde, datetime__lt = hasta))

    pprint.pprint(datos)

    valores = {'N' : 0, 'NNE' : 0, 'NE' : 0, 'ENE' : 0, 'ESTE' : 0, 'ESE' : 0, 'SE' : 0, 'SSE' : 0, 'S' : 0, 'SSW' : 0, 'WSW' : 0, 'W' : 0, 'WNW' : 0, 'NW' : 0, 'NNW' : 0}
    direcciones = ['N', 'NNE', 'NE', 'ENE', 'ESTE', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

    for d in datos:
        if (d.get_wdir() in valores):
            valores[d.get_wdir()] += 1
        else:
            valores[d.get_wdir()] = 1

    resultado = []

    for index in direcciones:
        if (index in valores):
            resultado.append(valores[index])
        else:
            resultado.append(0)


    response_data = {}
    response_data['status'] = 'ok'
    response_data['data'] = {'direcciones' : direcciones, 'valores' : resultado}

    return HttpResponse(json.dumps(response_data, cls=DjangoJSONEncoder), content_type="application/json")
