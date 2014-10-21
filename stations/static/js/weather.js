$.noConflict();
jQuery(document).ready(function($){

	//BACKGROUND IMAGE
	$.backstretch('/static/images/clouds.png');
	
	
	//map();
	
	
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











