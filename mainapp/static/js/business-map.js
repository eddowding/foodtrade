

var map = L.map('map').setView([map_lat,map_lon], 7);

		L.tileLayer('http://{s}.tile.cloudmade.com/0c670d97b5984ce79b34deb902915b3e/110167/256/{z}/{x}/{y}.png', {
			maxZoom: 18,
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>'
		}).addTo(map);


		L.icon({
			iconUrl:'http://foodtrade.com/wp-content/uploads/2013/09/favi21.png',
			iconSize:[18,18],
			iconAnchor:[9,18],
			popupAnchor:[0,-18]
		});

L.circle([map_lat,map_lon], 24140.2, {
			color: '#333333',
			opacity:0,
			weight:2,
		}).addTo(map);
L.circle([map_lat,map_lon], 48280.3, {
			color: '#333333',
			opacity:0,
			weight:2,
		}).addTo(map);
	
L.circle([map_lat,map_lon], 160934, {
			color: '#333333',
			opacity:0,
			weight:2,
		}).addTo(map);
L.marker([parseFloat(map_lat), parseFloat(map_lon)]).addTo(map);

		for(var i=0;i<connections.length;i++)
		{
			var con = connections[i];
			var name = con.name;
			var description = con.description;
			var photo =  con.photo;
			var username = con.username;
			var type = con.type;
			var relation = con.relation;
			var latitude =  con.latitude;
         	var longitude =  con.longitude;

			color = 'red';
			if(relation=="buyer")
			{
				color = "orange";
			}
			var polyline = L.polyline([
			[parseFloat(map_lat), parseFloat(map_lon)],
			[parseFloat(latitude), parseFloat(longitude)]
			],{color: color}).addTo(map)
		}

