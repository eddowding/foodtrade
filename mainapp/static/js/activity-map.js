

var map = L.map('map').setView([map_lat,map_lon], 7);

		L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {
			maxZoom: 18,
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>'
		}).addTo(map);

L.circle([map_lat,map_lon], 24140.2, {
			color: '#333333',
		}).addTo(map);
L.circle([map_lat,map_lon], 48280.3, {
			color: '#333333',
		}).addTo(map);
	
L.circle([map_lat,map_lon], 160934, {
			color: '#333333',
		}).addTo(map);
		for(i=0;i<connections.length;i++)
		{
			var con = connections[i];
			var name = con.user.name;
			var last_name =  con.status;
			
			
			L.marker([parseFloat(con.location.coordinates[1]), parseFloat(con.location.coordinates[0])]).addTo(map).bindPopup("<b>"+name + "</b> <br /><b>"+status+"</b><br />");
			
			
		}

