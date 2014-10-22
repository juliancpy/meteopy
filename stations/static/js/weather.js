$.noConflict();
jQuery(document).ready(function($){

	//BACKGROUND IMAGE
	$.backstretch('/static/images/clouds.png');
	
	//map();

	//chart_tmp();
    temp_prec_chart();
	// LIGHTBOX
	$(".fancybox").fancybox({
		openEffect	: 'fade',
		closeEffect	: 'fade'
	});

	
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

});//jQuery




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

function chart_tmp() {

    var $ = jQuery;
    $('#temp-tab1').highcharts({
        title: {
            text: 'Promedio de Temperatura Mensual',
            x: -20 //center
        },
        subtitle: {
            text: 'Fuente: www.meteorologia.gov.py',
            x: -20
        },
        xAxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        },
        yAxis: {
            title: {
                text: 'Temperature (°C)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '°C'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name: 'Fram',
            data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
        },]
    });
}

var chart;
function temp_prec_chart() {
    var $ = jQuery;
    $('#temp-tab2').highcharts({
        chart: {
            zoomType: 'xy'
        },
        title: {
            text: 'Temperature vs Rainfall'
        },
        xAxis: [{
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value} °C',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: 'Temperature',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            }
        }, { // Secondary yAxis
            title: {
                text: 'Rainfall',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                format: '{value} mm',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true
        }],

        tooltip: {
            shared: true
        },

        series: [{
            name: 'Rainfall',
            type: 'column',
            yAxis: 1,
            data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4],
            tooltip: {
                pointFormat: '<span style="font-weight: bold; color: {series.color}">{series.name}</span>: <b>{point.y:.1f} mm</b> '
            }
        }, {
            name: 'Rainfall error',
            type: 'errorbar',
            yAxis: 1,
            data: [[48, 51], [68, 73], [92, 110], [128, 136], [140, 150], [171, 179], [135, 143], [142, 149], [204, 220], [189, 199], [95, 110], [52, 56]],
            tooltip: {
                pointFormat: '(error range: {point.low}-{point.high} mm)<br/>'
            }
        }, {
            name: 'Temperature',
            type: 'spline',
            data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6],
            tooltip: {
                pointFormat: '<span style="font-weight: bold; color: {series.color}">{series.name}</span>: <b>{point.y:.1f}°C</b> '
            }
        }, {
            name: 'Temperature error',
            type: 'errorbar',
            data: [[6, 8], [5.9, 7.6], [9.4, 10.4], [14.1, 15.9], [18.0, 20.1], [21.0, 24.0], [23.2, 25.3], [26.1, 27.8], [23.2, 23.9], [18.0, 21.1], [12.9, 14.0], [7.6, 10.0]],
            tooltip: {
                pointFormat: '(error range: {point.low}-{point.high}°C)<br/>'
            }
        }]
    });
}







