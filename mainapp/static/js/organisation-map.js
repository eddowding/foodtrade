var map = new L.map('map', {
    center: new L.LatLng(map_lat,map_lon),
    crs: default_csr,
    zoom: default_zoom,
      continuousWorld: false,
        worldCopyJump: false,
    layers: [current_base_layer]
});



// create the control
var command = L.control({position: 'topright'});

command.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'command');

    div.innerHTML = '<form><input id="command" type="checkbox" '+ ((showcon=="show")?"checked":"") +' /> Show Connections</form>'; 
    return div;
};

command.addTo(map);




document.getElementById ("command").addEventListener ("click", handleCommand, false);


L.circle([map_lat,map_lon], 24140.2, {
			stroke: 1,
			color: '#00cc00',
			opacity:0.8,
			weight:1,
			fill: 0,
		}).addTo(map);
L.circle([map_lat,map_lon], 48280.3, {
			stroke: 1,
			color: '#ff9900',
			opacity:0.8,
			weight:1,
			fill: 0,
		}).addTo(map);
	
L.circle([map_lat,map_lon], 160934, {
			stroke: 1,
			color: '#444',
			opacity:0.8,
			weight:1,
			fill: 0,
		}).addTo(map);
 

var card_str = '<div class="card-box"><div class="content text-center"><div class=""><a href="/profile/'+username+'"><img src="'+photo+'" alt="'+name+'" class="img-circle img-thumbnail img-responsive" style="width:40px;" /></a>';
    card_str += '</div><div class="text"><b><a href="/profile/'+username+'">'+name+'</a></b>';
    card_str += '<p>'+description+'</p></div>';
    card_str += '<a href="/profile/'+username+'" class="btn btn-primary btn-sm">View profile &raquo;</a></div> </div>';    

if(parseInt(map_lon) != parseInt(def_lon) || parseInt(def_lat) != parseInt(map_lat))
         	{
            var rIcon = new RedIcon();
      rIcon.options.iconUrl = photo;
         		L.marker([parseFloat(map_lat), parseFloat(map_lon)], {icon: rIcon}).addTo(map).bindPopup(card_str);
         	}

 
var map_controls = [];
Search = {dot_controls:[], line_controls:[]};

  var connection_lines = new L.LayerGroup();
  var connection_dots = new L.LayerGroup();


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

function highlight_connections(userid)
{
	    var con_dots = Search.dot_controls['user_'+userid];
	    console.log(userid);

    var con_lines = Search.line_controls['user_'+userid];

if(con_dots == undefined)
{
    con_dots = [];
}
if(con_lines == undefined)
{
    con_lines = [];
}
for(var i = 0;i<con_dots.length;i++)
{
    var item = con_dots[i];
    item.setStyle({fillColor:"#cc0000", color:"#cc0000", opacity:1, fillOpacity:1});
    
}


for(var i = 0;i<con_lines.length;i++)
{
    var item = con_lines[i];
    item.setStyle({color:"#cc0000", opacity:1, fillOpacity:1});
}

}
function unhightlight_connections(userid)
{
	    var con_dots = Search.dot_controls['user_'+userid];


    var con_lines = Search.line_controls['user_'+userid];

    if(con_dots == undefined)
    {
        con_dots = [];
    }
    if(con_lines == undefined)
    {
        con_lines = [];
    }

    for(var i = 0;i<con_dots.length;i++)
    {
        var item = con_dots[i];
        item.setStyle({fillColor:"#cc0000", weight:1,
              fill:1,
              radius: 6, color:"#cc0000", opacity:0.1, fillOpacity:0.1});
    }


    for(var i = 0;i<con_lines.length;i++)
    {
        var item = con_lines[i];
        item.setStyle({color:"#cc0000", opacity:0.1, fillOpacity:0.1});
    }
}



  function map_profile_card(user)
{
  		var con = user;
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
        
        card_str +=  '<a class="" href="/activity/?q='+encodeURIComponent(type_user[j])+'&tab=profile&stype=profile&pwant=all&put=Companies">'+type_user[j]+'</a>';
       }
        card_str += '</div>';
    }

    card_str += '<p>'+description+'</p></div>';
    card_str += '<a href="/profile/'+username+'" class="btn btn-primary btn-sm">View profile &raquo;</a></div> </div>';
    return card_str;
}
function get_current_users()
{
     var ids = [];

     for(var i=0;i<connections.length;i++)
     { 
            ids.push(parseInt(connections[i]['id']))
     }
     return ids;
}

function show_connections()
{
    $.post( "/ajax-handler/get_connection_network", {ids:JSON.stringify(get_current_users())} , function( data ) {
        connections1 = data.connections;
        user_dict = data.users;
        var ids = get_current_users();
        for(var i = 0;i<connections1.length;i++)
        {
            var current_user1 = connections1[i]['b_useruid'];
            var current_user2 = connections1[i]['c_useruid'];
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
            var opacity = 0.1;
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

function reload_connections()
{
	   connection_dots.clearLayers();
   connection_lines.clearLayers();
	for(var i = 0;i<map_controls.length;i++)
	{
		map.removeLayer(map_controls[i]);
	}
	if(map_controls.length>0)
	{
		connections = new_connections;
	}
	map_controls =[];
	var max_lat = parseFloat(map_lat);
	var min_lat = parseFloat(map_lat);
	var max_lon = parseFloat(map_lon);
	var min_lon = parseFloat(map_lon);
		for(var i=0;i<connections.length;i++)
		{
			var con = connections[i];
			// var name = con.business_org_name;
			var name = con.name;
			var description = con.description;
			var photo =  con.photo;
			var username = con.username;
			var profile_img = con.photo;
			var type = con.type;
			var relation = con.relation;
			var latitude =  con.latitude;
         	var longitude =  con.longitude;
         	var type_user = con.type;


			var current_lat = parseFloat(latitude);
			var current_lon = parseFloat(longitude);
			if(parseInt(current_lon) == parseInt(def_lon) && parseInt(def_lat) == parseInt(current_lat))
         	{
         		continue;
         	}
			if(current_lat>max_lat)
			{
				max_lat = current_lat;
			}
			if(current_lat<min_lat)
			{
				min_lat = current_lat;
			}

			
			if(current_lon>max_lon)
			{
				max_lon = current_lon;
			}

			if(current_lon<min_lon)
			{
				min_lon = current_lon;
			}



			color = '#890D2F';
			if(relation=="buyer")
			{
				color = "#FC8628";
			}
			// var polyline = L.polyline([
			// [parseFloat(map_lat), parseFloat(map_lon)],
			// [parseFloat(latitude), parseFloat(longitude)]
			// ],{
			// 	color: color,
			// 	weight: 2,
			// 	opacity: 0.8
			// }).addTo(map);
			// map_controls.push(polyline);
var card_str = '<div class="card-box"><div class="text-center"><div class=""><a href="/profile/'+username+'"><img src="'+photo+'" alt="'+name+'" class="img-circle img-thumbnail img-responsive" style="width:40px;" /></a>';
    card_str += '</div><div class="text"><b><a href="/profile/'+username+'">'+name+'</a></b>';

    if(type.length>0)
      {
      card_str += '<div class="clearfix">';
        for(var j=0;j<type.length;j++)
        {  
        card_str +=  '<a class="" href="/activity/?q='+type[j]+'">'+type[j]+'</a>';
        }
        card_str += '</div>';
    }

    card_str += '<p class="scroll50">'+description+'</p></div>';
    card_str += '<a href="/profile/'+username+'" class="btn btn-primary btn-sm">View profile &raquo;</a></div> </div>';    




if(parseInt(current_lon) != parseInt(def_lon) || parseInt(def_lat) != parseInt(current_lat))
{ 
			var dot = L.circleMarker([parseFloat(latitude), parseFloat(longitude)],  {
			userid: connections[i].id,
			color: '#000',
			opacity:0.7,
			weight:1,
			fill:1,
			radius: 6,
			fillColor: "#cc0000",
			fillOpacity: 1,

		}).addTo(map).bindPopup(card_str);
			map_controls.push(dot);
			dot.on('mouseover', function (e) {
            var user_id = this.options.userid;
            highlight_connections(user_id);
        });
        dot.on('mouseout', function (e) {
            var user_id = this.options.userid;
            unhightlight_connections(user_id);
        });


		}
		show_connections();
}



	if(max_lat == min_lat && max_lon==min_lon)
		{
			var padding = 0.3
			max_lat += padding;
			min_lat -= padding;
			max_lon += padding;
			min_lon -= padding;
		}


	  map.fitBounds([
	    [min_lat, min_lon],
	    [max_lat, max_lon]
	  ]);

	  
		}

		
    map.scrollWheelZoom.disable();
    L.control.fullscreen().addTo(map);


setTimeout(function(){reload_connections()},3000);