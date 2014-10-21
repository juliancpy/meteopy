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
    url(r'^estacion/(\d+)$', 'stations.views.estacion_view', name='estacion'),
    url(r'^chart/$', 'stations.views.temp_home_chart_view', name='temp_home_chart_view'),
)
