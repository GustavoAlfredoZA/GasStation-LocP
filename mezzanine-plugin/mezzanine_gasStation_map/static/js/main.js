var mymap = L.map('mapid').setView([19.6493721,-101.2209878], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
  maxZoom: 18,
  attribution:'Gustavo Alfredo Zarate Acosta Antonio Chacon Flores, ' +
  'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
  id: 'mapbox/streets-v11',
  tileSize: 512,
  zoomOffset: -1
}).addTo(mymap);

function onLocationFound(e) {
        var radius = e.accuracy / 2;
        var curr_latitude = e.latitude;
        var curr_longitude = e.longitude
        L.circle(e.latlng,{color:'red', radius: '10'}).addTo(mymap).bindPopup("Estas cerca de aquí").openPopup();
        L.circle(e.latlng, radius).addTo(mymap);
}

function onLocationError(e) {
        alert(e.message);
}

mymap.on('locationfound', onLocationFound);
mymap.on('locationerror', onLocationError);
mymap.locate({setView: false, maxZoom: 16});
mymap.on('locationfound', onLocationFound);
mymap.on('locationerror', onLocationError);
mymap.locate({setView: false, maxZoom: 16});

var popup = L.popup();

function onMapClick(e) {
  popup
  .setLatLng(e.latlng)
  .setContent("You clicked the map at " + e.latlng.toString())
  .openOn(mymap);
}

var stateFilters = L.layerGroup().addTo(mymap);
var alldatageojson = $.getJSON("../static/mezzanine_gasStation_map/js/data.json");

function stateSelect(){
  alldatageojson.then( function(data) {
    var miSelect = document.getElementById("list").value;
    var alldata = L.geoJson(data, {
      filter: function(feature, layer){
        if(miSelect != "All")
        return (feature.properties.state == miSelect );
        else
        return true;
      },
      onEachFeature: function (feature, layer) {
        var label = "<b>" + feature.properties.name + "</b><br/>"
        if(feature.properties.regular!=null){
          label = label + "Precio de gasolina regular:   $" + feature.properties.regular + "<br/>"
        }
        if(feature.properties.premium!=null){
          label = label + "Precio de gasolina premium: $" + feature.properties.premium + "<br/>"
        }
        if(feature.properties.diesel!=null){
          label = label + "Precio de diesel: $" + feature.properties.diesel
        }
        layer.bindPopup(label);
      }
    });
    stateFilters.clearLayers();
    stateFilters.addLayer(alldata);
  });
}

$.getJSON("../static/mezzanine_gasStation_map/js/mexicostatesprod.json", function(data) {
    var mexstates = L.geoJson(data, {
      onEachFeature: function (feature, layer) {
        var label = feature.properties.gns_name
        layer.bindPopup(label);
      },
      style: function(){
        return {
          color: 'white',
          fillOpacity: 0.1,
          weight: 0.1
        }
      }
    });
    mexstates.addTo(mymap);
});

//$( "select" )
//  .change(function () {
//    var str = "";
//    $( "select option:selected" ).each(function() {
//      str += $( this ).text() + " ";
//    });
//    $( ".tableInfo" ).text( str );
//}).change();


$(document).ready( function () {
  alldatageojson.then( function(data){

    $.fn.dataTable.ext.search.push(

      function( settings, data, dataIndex ) {

        var stateSelectl = String($("#list").val() || "");
        var min = parseInt( $('#min').val(), 10 );
        var max = parseInt( $('#max').val(), 10 );
        var pricer = parseFloat( data[2] ) || 0;
        var pricep = parseFloat( data[3] ) || 0;
        var priced = parseFloat( data[4] ) || 0;
        var namestate = String( data[1] ) ;
        document.getElementById("test").innerHTML = stateSelectl
        if (namestate != stateSelectl && stateSelectl != "All" && stateSelectl != ""){
          return false;
        }

        if ( ( ( isNaN( min ) && isNaN( max ) ) ||
        ( isNaN( min ) && pricer <= max ) ||
        ( min <= pricer   && isNaN( max ) ) ||
        ( min <= pricer   && pricer <= max ) ) &&

        ( ( isNaN( min ) && isNaN( max ) ) ||
        ( isNaN( min ) && pricep <= max ) ||
        ( min <= pricep   && isNaN( max ) ) ||
        ( min <= pricep   && pricep <= max ) ) &&

        ( ( isNaN( min ) && isNaN( max ) ) ||
        ( isNaN( min ) && priced <= max ) ||
        ( min <= priced   && isNaN( max ) ) ||
        ( min <= priced   && priced <= max ) ) )
        {
          return true;
        }
        return false;
      }

    );

    $(document).ready(function() {
        var table = $('#table_all').DataTable();
        // Event listener to the two range filtering inputs to redraw on input
        $('#min, #max').keyup( function() {
            table.draw();
        } );
        $('#list').on('change', function(){
            table.draw();
        });


    } );



    $('#table_all').DataTable( {

      deferRender:    true,
      scrollY:        200,
      scrollCollapse: true,
      scroller:       true,
      info:           true,
      data: data['features'],
      orderCellsTop: true,
      columns:[
        {data:'properties.name'},
        {data:'properties.state',defaultContent: "Sin información"},
        {data:'properties.regular',defaultContent: "Sin información"},
        {data:'properties.premium',defaultContent: "Sin información"},
        {data:'properties.diesel',defaultContent: "Sin información"},

      ],
      initComplete: function () {
        this.api().columns().every( function () {
          var column = this;
          var select = $('<select><option value=""></option></select>')
          .appendTo( $(column.footer()).empty() )
          .on( 'change', function () {
            var val = $.fn.dataTable.util.escapeRegex(
              $(this).val()
            );

            column
            .search( val ? '^'+val+'$' : '', true, false )
            .draw();
          } );

          column.data().unique().sort().each( function ( d, j ) {
            select.append( '<option value="'+d+'">'+d+'</option>' )
          } );
        } );
      }

    });

  });

});
