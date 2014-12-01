from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'meteopy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'stations.views.home', name='home'),
    url(r'^estacion/(?P<id_estacion>\d+)/', 'stations.views.home'),
    url(r'^temperatura/historico/(?P<id_estacion>\d+)/', 'stations.views.temperatura_historico'),
    url(r'^viento/historico/(?P<id_estacion>\d+)/', 'stations.views.viento_historico'),
    url(r'^viento/direccion_historico/(?P<id_estacion>\d+)/', 'stations.views.viento_direccion_historico'),
    url(r'^precipitacion/historico/(?P<id_estacion>\d+)/', 'stations.views.precipitacion_historico'),
    url(r'^precipitacion/acumulado_dia/(?P<id_estacion>\d+)/', 'stations.views.precipitacion_acumulado_dia'),
    url(r'^viento/conteo_direccion/(?P<id_estacion>\d+)/', 'stations.views.viento_conteo_direccion'),
    url(r'^detalles/(?P<id_estacion>\d+)/', 'stations.views.details_view', name='detalles'),
    url(r'^detalles/$', 'stations.views.details_view', name='detalles'),
    url(r'^reporte/$', 'stations.views.reporte', name='reporte'),
    url(r'^reporte/generar$', 'stations.views.reporte_generar', name='reporte_generar'),
    url(r'^reporte/generar/csv$', 'stations.views.reporte_generar_csv', name='reporte_generar_csv'),

#    url(r'^chart/$', 'stations.views.temp_home_chart_view', name='temp_home_chart_view'),
)
