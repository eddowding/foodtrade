var map = new L.map('map', {
    center: new L.LatLng(map_lat,map_lon),
    crs: default_csr,
    zoom: default_zoom,
      continuousWorld: false,
        worldCopyJump: false,
    layers: [current_base_layer]
});

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
         		L.marker([parseFloat(map_lat), parseFloat(map_lon)], {icon: redIcon}).addTo(map).bindPopup(card_str);
         	}


if(parseInt(map_lon) != parseInt(def_lon) || parseInt(def_lat) != parseInt(map_lat))
         	{
		 L.marker([parseFloat(map_lat), parseFloat(map_lon)], {icon: redIcon}).addTo(map).bindPopup(card_str);
}
// 
var map_controls = [];
function reload_connections()
{
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
			
			color: '#000',
			opacity:0.7,
			weight:1,
			fill:1,
			radius: 6,
			fillColor: "#cc0000",
			fillOpacity: 1,

		}).addTo(map).bindPopup(card_str);
			map_controls.push(dot);
		}

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