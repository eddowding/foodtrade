function load_map(lat,lng)
{
  map = new L.map('map', {
      center: new L.LatLng(lat,lng),
      crs: default_csr,
      zoom: default_zoom,
        continuousWorld: false,
          worldCopyJump: false,
      layers: [current_base_layer]
  });
  L.control.fullscreen().addTo(map);
map.on('dragend', map_dragged);

}


var layer_group = new L.LayerGroup();

// L.circle([map_lat,map_lon], 24140.2, {
//       stroke: 1,
//       color: '#00cc00',
//       opacity:0.5,
//       weight:2,
//       fill: 0,
// }).addTo(layer_group);



// L.circle([map_lat,map_lon], 48280.3, {
//       stroke: 1,
//       color: '#ff9900',
//       opacity:0.5,
//       weight:2,
//       fill: 0,
// }).addTo(layer_group);
  
// L.circle([map_lat,map_lon], 160934, {
//       stroke: 1,
//       color: '#999',
//       opacity:0.9,
//       weight: 1,
//       fill: 0,
//     }).addTo(layer_group);





var markers = new L.MarkerClusterGroup();
function show_connections_on_map()
{
  
   markers.clearLayers();

  var results = Search[Search.tab+"_results"].result;


    for(var i=0;i<results.length;i++)
    {
      
      var current_lat = parseFloat(results[i].latlng.coordinates[1]);
      var current_lon = parseFloat(results[i].latlng.coordinates[0]);
      var card = (Search.tab=="market")?map_update_card(results[i]):map_profile_card(results[i]);
      var ctrl = L.marker([parseFloat(current_lat), parseFloat(current_lon)],{icon: redIcon}).bindPopup(card);
     
        markers.addLayer(ctrl);
         }
    
        map.addLayer(markers);
        if(results.length>0){
            // map.fitBounds(markers.getBounds());
        }
}


function map_dragged(e) {      
      var current_center = map.getCenter();
      Search.filters[Search.tab].lng = current_center.lng;
      Search.filters[Search.tab].lat = current_center.lat;    
      Search.search_start();
        
}
