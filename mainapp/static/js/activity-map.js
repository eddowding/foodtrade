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

function reload_controls()
{
  
  layer_group.clearLayers();

  var results = result_object.result;

    for(i=0;i<results.length;i++)
    {
      var con = results[i];
      var name = con.name;
      var status =  con.description;
      var profile_img = con.profile_img;
      var username = con.username;
      var banner = con.banner_url;
      var description = con.description;
      var type_user = con.type_user;
      var sign_up_as = con.sign_up_as;
      if(!type_user)
      {
        type_user = [];
      }


      
      // if(sign_up_as != "Business")
      // {
      //  continue;
      // }

      var current_lat = parseFloat(con.latlng.coordinates[1]);
      var current_lon = parseFloat(con.latlng.coordinates[0]);
      // if(current_lon == def_lon && current_lat == def_lat)
      //     {
      //       continue;
      //     }
      
var card_str = '<div class="card-box"><div class="content text-center"><div class=""><a href="/profile/'+username+'"><img src="'+profile_img+'" alt="'+name+'" class="img-circle img-thumbnail img-responsive" style="width:73px;" /></a>';
    card_str += '</div><div class="text"><h3><a href="/profile/'+username+'">'+name+'</a></h3>';

    if(type_user.length>0)
    {
      card_str += '<div class="  clearfix">';
      for(var j=0;j<type_user.length;j++)
      {  
        
        card_str +=  '<a class="" href="/activity/?b='+type_user[j]+'">'+type_user[j]+'</a>';
       }
        card_str += '</div>';
    }

    card_str += '<p>'+description+'</p></div>';
    card_str += '<a href="/profile/'+username+'" class="btn btn-primary btn-sm">View profile &raquo;</a></div> </div>';

var ctrl = L.marker([parseFloat(current_lat), parseFloat(current_lon)],{icon: redIcon}).bindPopup(card_str);
      
        markers.addLayer(ctrl);
    
   map.addLayer(markers);

    }

 

//  MAKES MAP ZOOM TO EXTENT OF ALL CONNECTIONS 
//      map.fitBounds([
//     [min_lat, min_lon],
//     [max_lat, max_lon]
// ]);

      
}



    L.control.fullscreen().addTo(map);
     


function map_dragged(e) {
       markers.clearLayers();
      var current_center = map.getCenter();
      var map_lon = current_center.lng;
      var map_lat = current_center.lat;    
      ajax_request("get_search_result", 'update_map', {lng: map_lon, lat:map_lat});
        
}


function update_map(data)
{
    result_object = jQuery.parseJSON(data);
    reload_controls();
}

map.on('dragend', map_dragged);


// setTimeout(function(){reload_controls()},3000);
