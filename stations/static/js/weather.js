$.noConflict();
jQuery(document).ready(function($){

    //BACKGROUND IMAGE
    $.backstretch('/static/images/clouds.png');

    //map();

    // LIGHTBOX
    $(".fancybox").fancybox({
        openEffect  : 'fade',
        closeEffect : 'fade'
    });

    pronos();
    // ACCORDION
    $('[data-toggle="collapse"]').on('click', function(){
        var $this = $(this);

        if( !$this.hasClass('active') ){
            $this.text('-').addClass('active');
        }else{
            $this.text('+').removeClass('active');
        }
    });


    // SELECTS
    $('select.form-control').selectpicker({
        style: 'btn-info',
        size: 6
    });


    Dashboard.inicializar();

});//jQuery

var Util = {
    getFechaActual : null,
    getFechaActualResta : null
};

/**
 * Obtiene la fecha actual
 * @return {String}
 */
Util.getFechaActual = function()
{
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!
    var yyyy = today.getFullYear();
    if (dd < 10) {
        dd = '0' + dd;
    }
    if (mm < 10) {
        mm = '0' + mm;
    }
    var today = yyyy + '-' + mm + '-' + dd;
    return today;
};

/**
 * Obtiene la fecha actual menos la cantidad de dias
 * @param dias
 */
Util.getFechaActualResta = function(dias)
{
    var today = new Date();
    var minus = new Date(today.getTime() - (dias * 24 * 3600 * 1000));


    var dd = minus.getDate();
    var mm = minus.getMonth() + 1; //January is 0!
    var yyyy = minus.getFullYear();
    if (dd < 10) {
        dd = '0' + dd;
    }
    if (mm < 10) {
        mm = '0' + mm;
    }
    var minus = yyyy + '-' + mm + '-' + dd;
    return minus;

};


var Loader = {
    showLoader : null,
    removeLoader : null,
    addLoaderElement : null,
    removeLoaderElement : null
};

// extender de HomeCharts para tener la implementacion de los metodos que se comparten
var HighCharts = {
    _loader : Loader,
    graficoLinea : null
};

HighCharts.graficoLinea = function(elementoSelector, datos, titulo, labelValor)
{
    jQuery(elementoSelector).highcharts({
        chart: {
            zoomType: 'x'
        },
        title: {
            text: titulo
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                    'Click and drag in the plot area to zoom in' :
                    'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime',
            //minRange: 14 * 24 * 3600000 // fourteen days
        },
        // yAxis: {
        //     title: {
        //         text: 'Exchange rate'
        //     }
        // },
        legend: {
            enabled: false
        },
        plotOptions: {
            area: {
                // fillColor: {
                //     linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                //     stops: [
                //         [0, Highcharts.getOptions().colors[0]],
                //         [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                //     ]
                // },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },
        series: [{
            type: 'line',
            name: labelValor,
            //pointInterval: 24 * 3600 * 1000,
            //pointStart: Date.UTC(2006, 0, 1),
            data: datos,
            turboThreshold: 1000000000
        }]
    });
};

HighCharts.graficoBarra = function(elementoSelector, datosX, datosY, titulo, labelValor)
{
    jQuery(elementoSelector).highcharts({
        chart: {
            type: 'column'
        },
        title: {
            text: titulo
        },
        // subtitle: {
        //     text: 'Source: WorldClimate.com'
        // },
        xAxis: {
            categories: datosX
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Valores'
            }
        },
        // tooltip: {
        //     headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        //     pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
        //         '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
        //     footerFormat: '</table>',
        //     shared: true,
        //     useHTML: true
        // },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: labelValor,
            data: datosY
        }]
    });
};

HighCharts.graficoPolarGrados = function(elementoSelector, datosX, datosY, titulo, labelValor)
{
    // jQuery(elementoSelector).highcharts({
    //     chart: {
    //         polar: true,
    //         type: 'line'
    //     },

    //     title: {
    //         text: 'Budget vs spending',
    //         x: -80
    //     },

    //     pane: {
    //         size: '80%'
    //     },

    //     xAxis: {
    //         categories: datosX,
    //         tickmarkPlacement: 'on',
    //         lineWidth: 0
    //     },

    //     yAxis: {
    //         gridLineInterpolation: 'polygon',
    //         lineWidth: 0,
    //         min: 0
    //     },

    //     tooltip: {
    //         shared: true,
    //         pointFormat: '<span style="color:{series.color}">{series.name}: <b>${point.y:,.0f}</b><br/>'
    //     },

    //     legend: {
    //         align: 'right',
    //         verticalAlign: 'top',
    //         y: 70,
    //         layout: 'vertical'
    //     },

    //     series: [{
    //         name: 'Allocated Budget',
    //         data: datosY,
    //         pointPlacement: 'on'
    //     }]

    // });

    jQuery(elementoSelector).highcharts({
        chart: {
            polar: true
        },

        title: {
            text: titulo
        },

        pane: {
            startAngle: 0,
            endAngle: 360
        },

        xAxis: {
            tickInterval: 22.5,
            min: 0,
            max: 360,
            labels: {

                formatter: function () {
                    var dir = {0 : 'N', 22.5 : 'NNE', 45 : 'NE', 67.5 : 'ENE', 90 : 'E', 112.5 : 'ESE', 135 : 'SE', 157.5 : 'SSE', 180 : 'S', 202.5 : 'SSW', 225 : 'SW', 247.5 : 'WSW', 270 : 'W', 292.5 : 'WNW', 315 : 'NW', 337.5 : 'NNW'};
                    return dir[this.value];
                    //return this.value + ' °';
                }
            }
        },

        yAxis: {
            min: 0
        },

        plotOptions: {
            series: {
                pointStart: 0,
                pointInterval: 22.5
            },
            column: {
                pointPadding: 0,
                groupPadding: 0
            }
        },

        series: [
            {
                type: 'line',
                name: labelValor,
                data: datosY
            }
        ]
    });
};

var HomeCharts = {
    _loader : Loader,
    _graficos : HighCharts,
    _fechaInicio : null,
    _fechaFin : null,
    _fechaDiezDiasFin : null,
    temperaturaHistorico : null,
    velocidadHistorico : null,
    vientoHistorico : null,
    lluviaHistorico : null,
    graficoLinea : null,
    cargarDatosSincrono : null,
    inicializar : null
};

HomeCharts.inicializar = function()
{
    HomeCharts._fechaInicio = Util.getFechaActual();
    HomeCharts._fechaFin = Util.getFechaActualResta(30);
    HomeCharts._fechaDiezDiasFin = Util.getFechaActualResta(10);
};

HomeCharts.cargarDatosSincrono = function(url, desde, hasta)
{
    var resultDatos;

    jQuery.ajax({
        url : url + "?desde=" + desde + "&hasta=" + hasta,
        type : "GET",
        async : false,
        dataType : "json",
        success : function (response) {
            resultDatos = response.data;
        }
    });

    return resultDatos;
};

HomeCharts.temperaturaHistorico = function(elementoSelector)
{
    var datos = HomeCharts.cargarDatosSincrono('/temperatura/historico/' + Dashboard._idEstacion, HomeCharts._fechaInicio, HomeCharts._fechaFin);

    var serie = [];

    // preparar los datos
    for (var i = 0; i < datos.length; i++)
    {
        serie.push({x: datos[i].datetime * 1000, y: datos[i].outtemp, name: datos[i].datetime  * 1000});
    }

    HomeCharts._graficos.graficoLinea(elementoSelector, serie, '', 'Temperatura');
};

HomeCharts.vientoHistorico = function(elementoSelector)
{
    var datos = HomeCharts.cargarDatosSincrono('/viento/historico/' + Dashboard._idEstacion, HomeCharts._fechaInicio, HomeCharts._fechaFin);

    var serie = [];

    // preparar los datos
    for (var i = 0; i < datos.length; i++)
    {
        serie.push({x: datos[i].datetime, y: datos[i].windspeed, name: datos[i].datetime});
    }

    HomeCharts._graficos.graficoLinea(elementoSelector, serie, '', 'Velocidad');
};

HomeCharts.vientoDireccionHistorico = function(elementoSelector)
{
    // var datos = HomeCharts.cargarDatosSincrono('/viento/direccion_historico/' + Dashboard._idEstacion, HomeCharts._fechaInicio, HomeCharts._fechaFin);

    // var serie = [];

    // // preparar los datos
    // for (var i = 0; i < datos.length; i++)
    // {
    //     serie.push({x: datos[i].datetime, y: datos[i].winddir, name: datos[i].datetime});
    // }

    // HomeCharts._graficos.graficoLinea(elementoSelector, serie, '', 'Direccion');

    var datos = HomeCharts.cargarDatosSincrono('/viento/conteo_direccion/' + Dashboard._idEstacion, HomeCharts._fechaInicio, HomeCharts._fechaFin);

    HomeCharts._graficos.graficoPolarGrados(elementoSelector, datos['direcciones'], datos['valores'], 'Precipitacion Acumulada por dia', 'Lluvia (mm)');
};

HomeCharts.precipitacionHistorico = function(elementoSelector)
{
    // var datos = HomeCharts.cargarDatosSincrono('/precipitacion/historico/' + Dashboard._idEstacion, HomeCharts._fechaInicio, HomeCharts._fechaFin);

    // var serie = [];

    // // preparar los datos
    // for (var i = 0; i < datos.length; i++)
    // {
    //     serie.push({x: datos[i].datetime, y: datos[i].rain_mm, name: datos[i].datetime});
    // }

    // HomeCharts._graficos.graficoLinea(elementoSelector, serie, '', 'Precipitacion');

    var datos = HomeCharts.cargarDatosSincrono('/precipitacion/acumulado_dia/' + Dashboard._idEstacion, HomeCharts._fechaInicio, HomeCharts._fechaDiezDiasFin);

    HomeCharts._graficos.graficoBarra(elementoSelector, datos['dias'], datos['valores'], 'Precipitacion Acumulada por dia', 'Lluvia (mm)');

};


var Dashboard = {
    _idEstacion : null,
    inicializar : null,
    temperaturaTabListener : null,
    vientoTabListener : null
};

Dashboard.inicializar = function()
{
    HomeCharts.inicializar();
    Dashboard._idEstacion = 1;
    Dashboard.temperaturaTabListener();

    //HomeCharts._fechaFin = '2012-02-05';
    //HomeCharts._fechaInicio = '2012-01-25';
    //HomeCharts._fechaDiezDiasFin = '2012-01-29';
};

Dashboard.temperaturaTabListener = function()
{
    jQuery("#btnGrafTemp").click(function(){
        // es el valor antes de terminar la transicion por lo que todavia no se ve
        if (jQuery('#collapse-temperature').is(':hidden'))
        {
            HomeCharts.temperaturaHistorico("#temp-tab1");
        }
    });

    jQuery("#btnGrafVientoVel").click(function(){
        // es el valor antes de terminar la transicion por lo que todavia no se ve
        if (jQuery('#collapse-wind-speed').is(':hidden'))
        {
            HomeCharts.vientoHistorico("#wind-speed-tab1");
        }
    });

    jQuery("#btnGrafVientoDir").click(function(){
        // es el valor antes de terminar la transicion por lo que todavia no se ve
        if (jQuery('#collapse-winddir').is(':hidden'))
        {
            HomeCharts.vientoDireccionHistorico("#winddir-tab1");
        }
    });

    jQuery("#btnGrafPrecipitaciones").click(function(){
        // es el valor antes de terminar la transicion por lo que todavia no se ve
        if (jQuery('#collapse-rainfall').is(':hidden'))
        {
            HomeCharts.precipitacionHistorico("#rainfall-tab1");
        }
    });





    /*jQuery("#btnGrafTemp").click(function(){
        // es el valor antes de terminar la transicion por lo que todavia no se ve
        if (jQuery('#collapse-temperature').is(':hidden'))
        {
            HomeCharts.temperaturaHistorico("#temp-tab1");
        }
    });

    jQuery("#btnGrafTemp").click(function(){
        // es el valor antes de terminar la transicion por lo que todavia no se ve
        if (jQuery('#collapse-temperature').is(':hidden'))
        {
            HomeCharts.temperaturaHistorico("#temp-tab1");
        }
    });*/
};


// getValores.json
//  {"fecha":"2014-11-05","hora":"11:10:00","vientoInt":"3.1","vientoDir":"152","vientoMax":"3.8","vientoMaxHora":"01:50:00","vientoMaxDir":"180","precipitacion":null,"precipitacionDia":null,"precipitacionMes":"18.2000000700355","precipitacionAnho":"1892.30000220984","humedad":"68","tempSuelo":"22.8","tempAire":"18.2","tempMin":"14.1","tempMinHora":"07:40:00","tempMax":"19.5","tempMaxHora":"00:00:00","presionAtm":"1000","radiacion":"398","vientoPreDir":"SSE","vientoPreCount":"38"}

// http://meteo.uni.edu.py/api.php?f=getMeteoData&tipo=tempAire&desde=2014-10-06&hasta=2014-11-05
// {"fecha":"2014-10-27","hora":"14:30:00","data":"34.6"},

// ultima lectura registrada en la estacion
//Lecturas Obtenidas el 2014-11-05 a las 11:20:00 UTC / 08:20:00 GMT-0300 (PYST)


function pronos(){

        var filas = jQuery('#climaContent').find('table tr');
        var pronoFecha = jQuery('#climaContent').find('div.Estilo8').text();
        var dia = jQuery(jQuery(filas.get(3)).find('td').get(0)).text();
        var icono = jQuery(jQuery(filas.get(4)).find('td').get(0)).find('div').html();
        var pronostico = jQuery(jQuery(filas.get(5)).find('td').get(0)).find('div span').html();
        var temperaturas = jQuery(jQuery(filas.get(6)).find('td').get(0)).find('strong');
        var minima = jQuery(temperaturas.get(0)).text();
        var maxima = jQuery(temperaturas.get(1)).text();

        icono = jQuery(icono).attr('src', 'http://www.meteorologia.gov.py/' + jQuery(icono).attr('src')).attr('title', pronostico);

        jQuery('#pronosDate').html(pronoFecha);
        jQuery('#cellDia1').html(dia);
        jQuery('#cellIcono1').html(icono);
        jQuery('#cellMinima1').html( minima);
        jQuery('#cellMaxima1').html( maxima);

        dia = jQuery(jQuery(filas.get(3)).find('td').get(2)).text();
        icono = jQuery(jQuery(filas.get(4)).find('td').get(2)).find('div').html();
        pronostico = jQuery(jQuery(filas.get(5)).find('td').get(2)).find('div span').html();
        temperaturas = jQuery(jQuery(filas.get(6)).find('td').get(2)).find('strong');
        minima = jQuery(temperaturas.get(0)).text();
        maxima = jQuery(temperaturas.get(1)).text();

        icono = jQuery(icono).attr('src', 'http://www.meteorologia.gov.py/' + jQuery(icono).attr('src')).attr('title', pronostico);

        jQuery('#cellDia2').html(dia);
        jQuery('#cellIcono2').html(icono);
        jQuery('#cellMinima2').html(minima);
        jQuery('#cellMaxima2').html(maxima);

        dia = jQuery(jQuery(filas.get(3)).find('td').get(4)).text();
        icono = jQuery(jQuery(filas.get(4)).find('td').get(4)).find('div').html();
        pronostico = jQuery(jQuery(filas.get(5)).find('td').get(4)).find('div span').html();
        temperaturas = jQuery(jQuery(filas.get(6)).find('td').get(4)).find('strong');
        minima = jQuery(temperaturas.get(0)).text();
        maxima = jQuery(temperaturas.get(1)).text();

        icono = jQuery(icono).attr('src', 'http://www.meteorologia.gov.py/' + jQuery(icono).attr('src')).attr('title', pronostico);

        jQuery('#cellDia3').html(dia);
        jQuery('#cellIcono3').html(icono);
        jQuery('#cellMinima3').html(minima);
        jQuery('#cellMaxima3').html(maxima);
        jQuery('#pronostico').show();

}


// MAP
/*
function map(){

    var $ = jQuery;

    $('.map .gMap').gmap3({
      map:{
        options:{
          center:[-27.208104,-55.9238545],
          zoom: 10,
                scrollwheel: false,
          panControl: false,
        overviewMapControl: true,
        mapTypeControl: false,
        scaleControl: true,
        streetViewControl: false,
        zoomControl: false,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        }
      },
        marker:{
            values:[
                {
                    address:'General Artigas, Paraguay',
                    data:'Estación 1',
                    tag: 'estacion-1',
                    options:{icon: 'http://maps.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png'}
                },
                {
                    address:'La Paz, Paraguay',
                    data:'Estación 2',
                    tag: 'estacion-2',
                    options:{icon: 'http://maps.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png'}
                },
                {
                    address:'Fram, Paraguay',
                    data:'Estación 3',
                    tag: 'estacion-3',
                    options:{icon: 'http://maps.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png'}
                },
                {
                    address:'Coronel Bogado, Paraguay',
                    data:'Estación 4',
                    tag: 'estacion-4',
                    options:{icon: 'http://maps.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png'}
                },
                {
                    address:'Carmen del Paraná, Paraguay',
                    data:'Estación 5',
                    tag: 'estacion-5',
                    options:{icon: 'http://maps.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png'}
                },
                {
                    address:'Encarnación, Paraguay',
                    data:'Estación 6',
                    tag: 'estacion-6',
                    options:{icon: 'http://maps.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png'}
                },
                {
                    address:'San Juan del Paraná, Paraguay',
                    data:'Estación 7',
                    tag: 'estacion-7',
                    options:{icon: 'http://maps.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png'}
                }
            ],
            options:{
          draggable: false
        },
        events:{
            click:function(marker, map, event){
                map_info(event.data, event.tag);
            },
          mouseover: function(marker, event, context){
            var map = $(this).gmap3('get'),
                 infowindow = $(this).gmap3({get:{name:'infowindow'}});

            if( infowindow ){

              infowindow.open(map, marker);
              infowindow.setContent(context.data);
            }else{
              $(this).gmap3({
                infowindow:{
                  anchor:marker,
                  options:{content: context.data}
                }
              });
            }

          },
          mouseout: function(){

            var infowindow = $(this).gmap3({get:{name:'infowindow'}});
            if (infowindow){
              infowindow.close();
            }

          }
        }

        }
    });
}//map()
*/

/*
function map_info($station, $data){
    // Return values for the info panel of the map

    var $ = jQuery;


    switch( $data ){
        case 'estacion-1':
            var $temperatura = 24,
                     $humedad = 81,
                     $rocio = 21,
                     $viento = 45,
                     $viento_direccion = 45,
                     $lluvia = 0,
                     $radiacion = 0,
                     $barometro = 1008;
        break;

        case 'estacion-2':
            var $temperatura = 18,
                     $humedad = 45,
                     $rocio = 22,
                     $viento = 15,
                     $viento_direccion = 9,
                     $lluvia = 1,
                     $radiacion = 1.4,
                     $barometro = 1038;
        break;

        case 'estacion-3':
            var $temperatura = 7,
                     $humedad = 13,
                     $rocio = 64,
                     $viento = 42,
                     $viento_direccion = 13,
                     $lluvia = 2,
                     $radiacion = 6,
                     $barometro = 2008;
        break;

        case 'estacion-4':
            var $temperatura = 12,
                     $humedad = 37,
                     $rocio = 24,
                     $viento = 25,
                     $viento_direccion = 15,
                     $lluvia = 3,
                     $radiacion = 2,
                     $barometro = 248;
        break;

        case 'estacion-5':
            var $temperatura = 14,
                     $humedad = 35,
                     $rocio = 26,
                     $viento = 24,
                     $viento_direccion = 29,
                     $lluvia = 3,
                     $radiacion = 6,
                     $barometro = 398;
        break;

        case 'estacion-6':
            var $temperatura = 4,
                     $humedad = 27,
                     $rocio = 30,
                     $viento = 75,
                     $viento_direccion = 132,
                     $lluvia = 2,
                     $radiacion = 6,
                     $barometro = 4688;
        break;

        case 'estacion-7':
            var $temperatura = 23,
                     $humedad = 1,
                     $rocio = 35,
                     $viento = 92,
                     $viento_direccion = 145,
                     $lluvia = 2,
                     $radiacion = 5,
                     $barometro = 1408;
        break;
    }


    $('.panel-map-info h5').text($station);
    $('#pmi-temperatura span').text($temperatura);
    $('#pmi-humedad span').text($humedad);
    $('#pmi-rocio span').text($rocio);
    $('#pmi-viento span').text($viento);
    $('#pmi-viento-direccion span').text($viento_direccion);
    $('#pmi-lluvia span').text($lluvia);
    $('#pmi-radiacion span').text($radiacion);
    $('#pmi-barometro span').text($barometro);
}//map_info()

*/




/*
DOCUMENTACIÓN DEL MAPA:
Al clickear el pin en el mapa se devuelve el valor de la variable "tag"
*/

