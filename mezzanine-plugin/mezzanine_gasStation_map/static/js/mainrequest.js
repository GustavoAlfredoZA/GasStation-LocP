var mymap = L.map('mapid').setView([19.6493721,-101.2209878], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
  maxZoom: 18,
  attribution:'Gustavo Alfredo Zarate Acosta Antonio Chacon Flores, ' +
  'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1
}).addTo(mymap);

$.getJSON("https://gasolinera-cerca.herokuapp.com/static/js/mexicostatesprod.json", function(data) {
    var mexstates = L.geoJson(data, {
      onEachFeature: function (feature, layer) {
        var label = feature.properties.gns_name;
        layer.bindPopup(label);
      },
      style: function(){
        return {
          color: 'white',
          fillOpacity: 0.1,
          weight: 0.1
        };
      }
    });
    mexstates.addTo(mymap);
});


function flyTo(Loc) {
        window.location.hash = '#mapid';
        mymap.flyTo(Loc, 16);
}




var stateFilters = L.layerGroup().addTo(mymap);
var alldatageojson = $.getJSON("https://gasolinera-cerca.herokuapp.com/static/js/data.json");

function stateSelect(){
  alldatageojson.then( function(data) {

    var min = parseFloat( $('#min').val(), 10 );
    var max = parseFloat( $('#max').val(), 10 );
    var miSelect = String($("#list").val() || "");
    var checkregular = document.getElementById('regular').checked;
    var checkpremium = document.getElementById('premium').checked;
    var checkdiesel = document.getElementById('diesel').checked;

    var alldata = L.geoJson(data, {
      filter: function(feature, layer){
        var pricer = parseFloat(feature.properties.regular)  || 0;
        var pricep = parseFloat(feature.properties.premium)  || 0;
        var priced = parseFloat(feature.properties.diesel)  || 0;

        if( ( ( ( isNaN( min ) == false ) && ( pricer < min ) ) ||
        ( ( isNaN( max ) == false ) && ( pricer > max ) ) ) && ( checkregular == true ) ){
          return false;
        }

        if( ( ( ( isNaN( min ) == false ) && ( pricep < min ) ) ||
        ( ( isNaN( max ) == false ) && ( pricep > max ) ) ) && ( checkpremium == true ) ){
          return false;
        }

        if( ( ( ( isNaN( min ) == false ) && ( priced < min ) ) ||
        ( ( isNaN( max ) == false ) && ( priced > max ) ) ) && ( checkdiesel == true ) ){
          return false;
        }


        if(miSelect != "All" && miSelect!= "")
        return (feature.properties.state == miSelect );
        return true;
      },
      onEachFeature: function (feature, layer) {
        var label = '<div class="jumbotron"><h6>'+ feature.properties.name + '</h6><ul class="list-group">';
        label = label + '<li class="list-group-item">Se encuentra a '+feature.properties.realdistance+' km. Tiempo aproximado a llegar '+feature.properties.duration+'</i> <li class="list-group-item">';
        if(feature.properties.regular!=null){
          label = label + 'Precio de gasolina regular:   $' + feature.properties.regular + '<br/>';
        }
        if(feature.properties.premium!=null){
          label = label + 'Precio de gasolina premium: $' + feature.properties.premium + '<br/>';
        }
        if(feature.properties.diesel!=null){
          label = label + 'Precio de diesel: $' + feature.properties.diesel;
        }

        label = label + '</li></ul><p><button type="button" class="btn btn-primary filterbutton" id="filterbutton"  onclick="tsearch(\''+feature.properties.name+'\')">Mostrar en la tabla</button></p></div>';
        layer.bindPopup(label);
      }
    });
    stateFilters.clearLayers();
    stateFilters.addLayer(alldata);
  });
}


function tsearch(name){
  window.location.hash = '#table_all';
  table.search( name ).draw();
}

function onLocationFound(e) {
        var radius = e.accuracy / 2;
        var curr_latitude = e.latitude;
        var curr_longitude = e.longitude;
        L.circle(e.latlng,{color:'red', radius: '10'}).addTo(mymap).bindPopup("Te encuantras cerca de aquí").openPopup();
        L.circle(e.latlng, radius).addTo(mymap);
}

function onLocationError(e) {
        alert(e.message);
}

mymap.on('locationfound', onLocationFound);
mymap.on('locationerror', onLocationError);
mymap.locate({setView: false, maxZoom: 16});

var popup = L.popup();

$(document).ready( function () {

  stateSelect();

  alldatageojson.then( function(data){

    $.fn.dataTable.ext.search.push(

      function( settings, data, dataIndex ) {

        var checkregular = document.getElementById('regular').checked;
        var checkpremium = document.getElementById('premium').checked;
        var checkdiesel = document.getElementById('diesel').checked;
        var stateSelectl = String($("#list").val() || "");
        var min = parseFloat( $('#min').val(), 10 );
        var max = parseFloat( $('#max').val(), 10 );
        var pricer = parseFloat( data[2] ) || 0;
        var pricep = parseFloat( data[3] ) || 0;
        var priced = parseFloat( data[4] ) || 0;
        var namestate = String( data[1] ) ;
        if( ( namestate != "Baja California" && stateSelectl == "BC" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Baja California Sur" && stateSelectl == "BS" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Coahuila" && stateSelectl == "CO" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Chihuahua" && stateSelectl == "CH" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Durango" && stateSelectl == "DG" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Sinaloa" && stateSelectl == "SI" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Sonora" && stateSelectl == "SO" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Zacatecas" && stateSelectl == "ZA" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Nuevo León" && stateSelectl == "NL" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "San Luis Potosí" && stateSelectl == "SL" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Tamaulipas" && stateSelectl == "TM" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Aguascalientes" && stateSelectl == "AG" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Colima" && stateSelectl == "CL" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Jalisco" && stateSelectl == "JA" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Michoacán" && stateSelectl == "MI" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Nayarit" && stateSelectl == "NA" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Campeche" && stateSelectl == "CM" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Oaxaca" && stateSelectl == "OA" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Puebla" && stateSelectl == "PU" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Tabasco" && stateSelectl == "TB" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Tlaxcala" && stateSelectl == "TL" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Ciudad de México" && stateSelectl == "DF" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Guanajuato" && stateSelectl == "GJ" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Guerrero" && stateSelectl == "GR" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Hidalgo" && stateSelectl == "HG" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Estado de México" && stateSelectl == "MX" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Morelos" && stateSelectl == "MO" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Querétaro" && stateSelectl == "QT" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Veracruz" && stateSelectl == "VE" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Chiapas" && stateSelectl == "CS" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Quintana Roo" && stateSelectl == "QR" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        else if( ( namestate != "Yucatán" && stateSelectl == "YU" ) && stateSelectl != "All" && stateSelectl != ""){return false;}
        if( ( ( ( isNaN( min ) == false ) && ( pricer < min ) ) ||
        ( ( isNaN( max ) == false ) && ( pricer > max ) ) ) && ( checkregular == true ) ){
          return false;
        }

        if( ( ( ( isNaN( min ) == false ) && ( pricep < min ) ) ||
        ( ( isNaN( max ) == false ) && ( pricep > max ) ) ) && ( checkpremium == true ) ){
          return false;
        }

        if( ( ( ( isNaN( min ) == false ) && ( priced < min ) ) ||
        ( ( isNaN( max ) == false ) && ( priced > max ) ) ) && ( checkdiesel == true ) ){
          return false;
        }
        return true;
      }

    );

    $('#filterbutton, #reset').on('click', function(){
      table.draw();
    });

    table = $('#table_all').DataTable( {
      order : [[ 4, "desc" ]],
      deferRender:    true,
      scrollY:        500,
      scrollCollapse: true,
      scroller:       true,
      info:           true,
      data: data.features,
      orderCellsTop: true,
      columns:[
        {
          "className":      'details-control',
          "orderable":      false,
          "data":           null,
          "defaultContent": ''
        },
        {data:'properties.name'},
        {
          data:'properties.state',
          defaultContent: "Sin información",
          render: function (data, type, row) {
            if (row.properties.state === 'BC') {return 'Baja California';}
            else if (row.properties.state === 'BS') {return 'Baja California Sur';}
            else if (row.properties.state === 'CO') {return 'Coahuila';}
            else if (row.properties.state === 'CH') {return 'Chihuahua';}
            else if (row.properties.state === 'DG') {return 'Durango';}
            else if (row.properties.state === 'SI') {return 'Sinaloa';}
            else if (row.properties.state === 'SO') {return 'Sonora';}
            else if (row.properties.state === 'ZA') {return 'Zacatecas';}
            else if (row.properties.state === 'NL') {return 'Nuevo León';}
            else if (row.properties.state === 'SL') {return 'San Luis Potosí';}
            else if (row.properties.state === 'TM') {return 'Tamaulipas';}
            else if (row.properties.state === 'AG') {return 'Aguascalientes';}
            else if (row.properties.state === 'CL') {return 'Colima';}
            else if (row.properties.state === 'JA') {return 'Jalisco';}
            else if (row.properties.state === 'MI') {return 'Michoacán';}
            else if (row.properties.state === 'NA') {return 'Nayarit';}
            else if (row.properties.state === 'CM') {return 'Campeche';}
            else if (row.properties.state === 'OA') {return 'Oaxaca';}
            else if (row.properties.state === 'PU') {return 'Puebla';}
            else if (row.properties.state === 'TB') {return 'Tabasco';}
            else if (row.properties.state === 'TL') {return 'Tlaxcala';}
            else if (row.properties.state === 'DF') {return 'Ciudad de México';}
            else if (row.properties.state === 'GJ') {return 'Guanajuato';}
            else if (row.properties.state === 'GR') {return 'Guerrero';}
            else if (row.properties.state === 'HG') {return 'Hidalgo';}
            else if (row.properties.state === 'MX') {return 'Estado de México';}
            else if (row.properties.state === 'MO') {return 'Morelos';}
            else if (row.properties.state === 'QT') {return 'Querétaro';}
            else if (row.properties.state === 'VE') {return 'Veracruz';}
            else if (row.properties.state === 'CS') {return 'Chiapas';}
            else if (row.properties.state === 'QR') {return 'Quintana Roo';}
            else if (row.properties.state === 'YU') {return 'Yucatán';}
            else {
                return row.properties.state;
              }
            }
        },
        {data:'properties.regular',defaultContent: "Sin información"},
        {data:'properties.realGasr',defaultContent: "Sin información"},
        {data:'properties.premium',defaultContent: "Sin información"},
        {data:'properties.realGasp',defaultContent: "Sin información"},
        {data:'properties.diesel',defaultContent: "Sin información"},
        {data:'properties.realGasd',defaultContent: "Sin información"},
      ],
    });

    function format ( d ) {
      if(d.properties.regular == undefined ){
        var litrosr = 0;
        var realr = 0;
      }
      else {
        var litrosr = (parseFloat(d.properties.litrosr)).toFixed(3);
        var realr = d.properties.realGasr;
      }
      if(d.properties.premium == undefined ){
        var litrosp = 0;
        var realp = 0;
      }
      else {
        var litrosp = (parseFloat(d.properties.litrosp)).toFixed(3);
        var realp = d.properties.realGasp;
      }
      if(d.properties.diesel == undefined ){
        var litrosd = 0;
        var reald = 0;

      }
      else {
        var litrosd = (parseFloat(d.properties.litrosd)).toFixed(3);
        var reald = d.properties.realGasd;
      }

      var spend = (d.properties.spend);

      // `d` is the original data object for the row
      return '<p>Calculos apartir de comprar $'+d.properties.money+' (MXN) de combustible iniciando un recorrido desde la ubicacion ('+d.properties.startX+','+d.properties.startY+') hasta la ubicación de la gasolinera en ('+d.geometry.coordinates[1]+','+d.geometry.coordinates[0]+')</p><table>'+
              '<tr>'+
                '<th>Información</th>'+
                '<th>Gasolina regular</th>'+
                '<th>Gasolina Premium</th>'+
                '<th>Diesel</th>'+
              '</tr>'+
              '<tr>'+
                '<td><button type="button" class="btn btn-primary locbutton" id="locbutton"  onclick=flyTo(['+d.geometry.coordinates[1]+','+d.geometry.coordinates[0]+'])>Mostrar en el mapa</button></td>'+
                '<td>Te alcanza para '+litrosr+' litros</td>'+
                '<td>Te alcanza para '+litrosp+' litros</td>'+
                '<td>Te alcanza para '+litrosd+' litros</td>'+
              '</tr>'+
              '<tr>'+
                '<td>Se encuentra a '+d.properties.realdistance+' km.</td>'+
                '<td>Pero te vas a gastar '+spend+' litros en llegar</td>'+
                '<td>Pero te vas a gastar '+spend+' litros en llegar</td>'+
                '<td>Pero te vas a gastar '+spend+' litros en llegar</td>'+
              '</tr>'+
              '<tr>'+
                '<td>Tiempo aproximado a llegar '+d.properties.duration+'</td>'+
                '<td>Por lo que te qudarian '+realr+' litros</td>'+
                '<td>Por lo que te qudarian '+realp+' litros</td>'+
                '<td>Por lo que te qudarian '+reald+' litros</td>'+
              '</tr>'+
            '</table>';
    }
    $('#table_all tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );



  });

});
