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
        L.marker(e.latlng).addTo(mymap).bindPopup("Estas cerca de aquí").openPopup();
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

$.getJSON("../static/mezzanine_gasStation_map/js/data.json", function(data) {
    var geojson = L.geoJson(data, {

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
    geojson.addTo(mymap);
});
