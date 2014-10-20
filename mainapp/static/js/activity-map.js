  var markers = new L.LayerGroup();
  var connection_lines = new L.LayerGroup();
  var connection_dots = new L.LayerGroup();
  // add the event handler
function handleCommand() {
   
   var checked = this.checked;
   if(!checked)
   {
     connection_dots.clearLayers();
     connection_lines.clearLayers();
     showcon = "hide";
     $.post( "/ajax-handler/update_map_settings", {status:"hide"} , function( data ) {

     });

   }
   else
   {
      $.post( "/ajax-handler/update_map_settings", {status:"show"} , function( data ) {

     });
      showcon = "show";
      show_connections();
   }
}
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

map.on('zoomend', map_dragged);
map._layersMinZoom=min_zoom_level;

// create the control
var command = L.control({position: 'topright'});

command.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'command');

    div.innerHTML = '<form><input id="command" type="checkbox" '+ ((showcon=="show")?"checked":"") +' />Show Connections</form>'; 
    return div;
};

command.addTo(map);




document.getElementById ("command").addEventListener ("click", handleCommand, false);
}


// L.circle([lat,lng], 320934, {
//       stroke: 1,
//       color: '#999',
//       opacity:0.9,
//       weight: 1,
//       fill: 0,
//     }).addTo(markers);

// L.circle([map_lat,map_lon], 24140.2, {
//       stroke: 1,
//       color: '#00cc00',
//       opacity:0.5,
//       weight:2,
//       fill: 0,
// }).addTo(markers);



// L.circle([map_lat,map_lon], 48280.3, {
//       stroke: 1,
//       color: '#ff9900',
//       opacity:0.5,
//       weight:2,
//       fill: 0,
// }).addTo(markers);

 

// var markers = new L.MarkerClusterGroup();

function get_current_users()
{
    var results = Search[Search.tab+"_results"];
     var ids = [];

     for(var i=0;i<results.length;i++)
     { 
        console.log(results[i]['useruid']);
            ids.push(parseInt(results[i]['useruid']))
     }
     return ids;
}
function show_connections()
{
    $.post( "/ajax-handler/get_connection_network", {ids:JSON.stringify(get_current_users())} , function( data ) {
        connections = data.connections;
        user_dict = data.users;
        var ids = get_current_users();
        for(var i = 0;i<connections.length;i++)
        {
            var current_user1 = connections[i]['b_useruid'];
            var current_user2 = connections[i]['c_useruid'];
            console.log(current_user1, current_user2);
            try
            {
            var user_lng1 = user_dict['user_'+current_user1]['latlng']['coordinates'][0];
            var user_lat1 = user_dict['user_'+current_user1]['latlng']['coordinates'][1];

            var user_lng2 = user_dict['user_'+current_user2]['latlng']['coordinates'][0];
            var user_lat2 = user_dict['user_'+current_user2]['latlng']['coordinates'][1];
          }
          catch(err)
          {
            continue;
          }
            console.log(user_lat1, user_lat2, user_lng1, parseFloat(user_lng2));
            var opacity = 0.3;
            if(ids.indexOf(current_user1)<0)
            {
            var con_dot1 = L.circleMarker([parseFloat(user_lat1),parseFloat(user_lng1)], {
            color: '#000',
            opacity:opacity,
            weight:1,
            fill:1,
            radius: 6,
            fillColor: "#cc0000",
            fillOpacity: opacity,

        }).bindPopup(map_profile_card(user_dict['user_'+current_user1]));
            connection_dots.addLayer(con_dot1);
            try {
                Search.dot_controls['user_'+current_user1].push(con_dot1);
            }
            catch(err) {
              Search.dot_controls['user_'+current_user2] = [];
              Search.dot_controls['user_'+current_user2].push(con_dot1);
            }
            


            }
            if(ids.indexOf(current_user2)<0)
            {              
              var con_dot2 = L.circleMarker([parseFloat(user_lat2),parseFloat(user_lng2)], {
              color: '#000',
              opacity:opacity,
              weight:1,
              fill:1,
              radius: 6,
              fillColor: "#cc0000",
              fillOpacity: opacity,
            }).bindPopup(map_profile_card(user_dict['user_'+current_user1]));
                connection_dots.addLayer(con_dot2);
                try {
                Search.dot_controls['user_'+current_user1].push(con_dot2);
            }
            catch(err) {
              Search.dot_controls['user_'+current_user1] = [];
                 Search.dot_controls['user_'+current_user1].push(con_dot2);
            }
            }

var color = '#890D2F';
            var con_line = L.polyline([
            [parseFloat(user_lat1), parseFloat(user_lng1)],
            [parseFloat(user_lat2), parseFloat(user_lng2)]
            ],{
                color: color,
                weight: 2,
                opacity: opacity
            });
            connection_lines.addLayer(con_line);
            try {
                Search.line_controls['user_'+current_user1].push(con_line);
            }
            catch(err) {
              Search.line_controls['user_'+current_user1] = [];
                 Search.line_controls['user_'+current_user1].push(con_line);
            }
          try {
                Search.line_controls['user_'+current_user2].push(con_line);
            }
            catch(err) {
              Search.line_controls['user_'+current_user2] = [];
                 Search.line_controls['user_'+current_user2].push(con_line);
            }
        }
        map.addLayer(connection_dots);
        map.addLayer(connection_lines);
     }, "json");

}

function show_connections_on_map()
{
  
   markers.clearLayers();
   connection_dots.clearLayers();
   connection_lines.clearLayers();

  var results = Search[Search.tab+"_results"];

    Search.map_controls = {};
    Search.dot_controls = {};
    Search.line_controls = {};
    for(var i=0;i<results.length;i++)
    {      
      var current_lat = parseFloat(results[i].latlng.coordinates[1]);
      var current_lon = parseFloat(results[i].latlng.coordinates[0]);
      var card = (Search.tab=="market")?get_box_update_map(results[i]):map_profile_card(results[i]);
      var rIcon = new RedIcon();
      rIcon.options.iconUrl = results[i].profile_img;
      var ctrl = L.marker([parseFloat(current_lat), parseFloat(current_lon)],{icon: rIcon, userid: results[i].useruid}).bindPopup(card);
      var marker_index = (Search.tab=="market")?results[i].username+"_"+results[i].updates.tweet_id:results[i].username;
      ctrl.on('mouseover', function (e) {
            var user_id = this.options.userid;
            highlight_connections(user_id);
        });
        ctrl.on('mouseout', function (e) {
            var user_id = this.options.userid;
            unhightlight_connections(user_id);
        });
      Search.map_controls[results[i].username] = ctrl;
        markers.addLayer(ctrl);
    }
    
        map.addLayer(markers);
        if(results.length>0){
          if(initial_flag)
          {
            initial_flag = false;
            var group = new L.featureGroup(markers.getLayers());
            map.fitBounds(group.getBounds());
            map.fitBounds(map.getBounds());
          }


            map.panTo(new L.LatLng(Search.filters[Search.tab].lat,Search.filters[Search.tab].lng));
        }
        show_connections();
}


function map_dragged(e) {
      var current_center = map.getCenter();
      Search.filters[Search.tab].lng = current_center.lng;
      Search.filters[Search.tab].lat = current_center.lat;    
      Search.clear_filters(Search.tab);
      Search.search_start();
        
}

