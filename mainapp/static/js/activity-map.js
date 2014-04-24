		var base_layer = L.tileLayer('https://{s}.tiles.mapbox.com/v3/foodtrade.i26pc0n5/{z}/{x}/{y}.png', {
			maxZoom: 18,
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>'
		});
 var openspaceLayer = L.tileLayer.osopenspace("F481BBF739A6038DE0430B6CA40AB6D2", {debug: true}); 

      // map.addLayer(openspaceLayer);
      var show_os_map = true;

if(map_lat>49.89193 && map_lat<61.08466 && map_lon>-9.38053 && map_lon<2.07316&&show_os_map)
{
	var default_csr = L.OSOpenSpace.getCRS();
	current_base_layer = openspaceLayer;
	var default_zoom = 4;
}
else
{
	var default_csr = L.CRS.EPSG3857;
	current_base_layer = base_layer;
	var default_zoom = 9;
}

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
			opacity:0.5,
			weight:2,
			fill: 0,
}).addTo(map);
L.circle([map_lat,map_lon], 48280.3, {
			stroke: 1,
			color: '#ff9900',
			opacity:0.5,
			weight:2,
			fill: 0,
}).addTo(map);
	
L.circle([map_lat,map_lon], 160934, {
			stroke: 1,
			color: '#999',
			opacity:0.9,
			weight: 1,
			fill: 0,
		}).addTo(map);




var map_controls = [];




$("#map").on('click dblclick keyup mousedown mousewheel', function() {
       
    	var current_center = map.getCenter();
    	var cent_lon = current_center.lng;
    	var cent_lat = current_center.lat;
    	var current_zoom_level = map.getZoom();

    	var is_current_base = (map.options.crs == L.CRS.EPSG3857);
    	var switching_zoom_level = 7;
// Check if the view is set to UK 
	if(cent_lat>49.89193 && cent_lat<61.08466 && cent_lon>-9.38053 && cent_lon<2.07316&&show_os_map)
    {
    	// Check if it is showing non OS map
    	if(is_current_base)
    	{

    		if(current_zoom_level > 16)
    		{
    			map.options.crs=L.OSOpenSpace.getCRS();
	    		map.removeLayer(base_layer)
	    		map.addLayer(openspaceLayer);
				map.setView([cent_lat,cent_lon],9);

    		}
    		var over_zoom = current_zoom_level-5;
    // 		if(over_zoom>9)
    // 		{
    // 			over_zoom = 9;
    // 		}
    // 		if(over_zoom - switching_zoom_level>0)
    // 		{
    // 			map.options.crs=L.OSOpenSpace.getCRS();
	   //  		map.removeLayer(base_layer)
	   //  		map.addLayer(openspaceLayer);
				// map.setView([cent_lat,cent_lon],over_zoom);

    // 		}
    	}
    	 else
	    {

	    	if(current_zoom_level<9)
	    	{
	    		map.options.crs=L.CRS.EPSG3857;
	    		map.removeLayer(openspaceLayer)
	    		map.addLayer(base_layer);
    			map.setView([cent_lat,cent_lon],16+current_zoom_level-9);
	    	}
	    	// if(current_zoom_level<switching_zoom_level+1)
	    	// {
	    			    	
	    	// 	map.options.crs=L.CRS.EPSG3857;
	    	// 	map.removeLayer(openspaceLayer)
	    	// 	map.addLayer(base_layer);
    		// 	map.setView([cent_lat,cent_lon],current_zoom_level+5);
	    	// }
	    	
	    }
    }
    else
    {
   //  	if(current_zoom_level<1+switching_zoom_level&&(!is_current_base))
   //  	{
   //  		map.options.crs=L.CRS.EPSG3857;
   //  		map.removeLayer(openspaceLayer)
   //  		map.addLayer(base_layer);
			// map.setView([cent_lat,cent_lon],current_zoom_level+5);
   //  	}
    	if((!is_current_base))
    	{
    		map.options.crs=L.CRS.EPSG3857;
    		map.removeLayer(openspaceLayer)
    		map.addLayer(base_layer);
			map.setView([cent_lat,cent_lon],9);
    	}
    }        
});
function reload_controls()
{
	for(var i = 0;i<map_controls.length;i++)
	{
		map.removeLayer(map_controls[i]);
	}
	map_controls =[];
	var max_lat = parseFloat(map_lat);
	var min_lat = parseFloat(map_lat);
	var max_lon = parseFloat(map_lon);
	var min_lon = parseFloat(map_lon);
		for(i=0;i<connections.length;i++)
		{
			var con = connections[i];
			if (typeof(con.user.business_org_name) == undefined){
				var name = (con.sign_up_as =="Business" || con.sign_up_as == "Organisation") && con.user.business_org_name!= '' ? con.user.business_org_name: con.user.name;
			}
			else{
				var name = con.user.name;
			}
			var status =  con.status;
			var profile_img = con.user.profile_img;
			var username = con.user.username;
			var description = con.user.description;
			var type_user = con.type_user;
			var sign_up_as = con.sign_up_as;
			if(!type_user)
			{
				type_user = [];
			}
			// if(sign_up_as != "Business")
			// {
			// 	continue;
			// }

			var current_lat = parseFloat(con.location.coordinates[1]);
			var current_lon = parseFloat(con.location.coordinates[0]);
			if(current_lon == def_lon && current_lat == def_lat)
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

var card_str = '<div class="card-box"><div class="content"><div class="pull-left"><a href="/profile/'+username+'"><img src="'+profile_img+'" alt="'+name+'" class="img-rounded img-responsive" style="width:40px;" /></a>';

                
                      card_str += '</div><div class="text"><h5><a href="/profile/'+username+'">'+name+'</a></h5>';

                      card_str += '<p class="small">'+description+'</p></div></div>';
                      if(type_user.length>0)
                      {
                    card_str += '<div class="numbers clearfix"><div class="tags tags-biztype pull-left">';
                    for(var j=0;j<type_user.length;j++)
                    {  
                      
                      card_str +=  '<a href="/activity/?b='+type_user[j]+'">'+type_user[j]+'</a>';
                     }
                      card_str += '</div></div>';
                }
                  card_str += '</div> ';
                  	var tweet_id = (con.result_type == username)?con.tweetuid:username;
			var ctrl = L.marker([parseFloat(current_lat), parseFloat(current_lon)],{tweet_id:tweet_id,icon: redIcon}).addTo(map).bindPopup(card_str);
			
			map_controls.push(ctrl);

		}



		if(max_lat == min_lat && max_lon==min_lon)
		{
			var padding = 0.3
			max_lat += padding;
			min_lat -= padding;
			max_lon += padding;
			min_lon -= padding;
		}



// 		  map.fitBounds([
//     [min_lat, min_lon],
//     [max_lat, max_lon]
// ]);
		


}




setTimeout(function(){reload_controls()},3000);
