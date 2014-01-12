

var map = L.map('map').setView([map_lat,map_lon], 7);

		L.tileLayer('http://{s}.tile.cloudmade.com/0c670d97b5984ce79b34deb902915b3e/110167/256/{z}/{x}/{y}.png', {
			maxZoom: 18,
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>'
		}).addTo(map);


 

	L.icon({
			iconUrl:'/images/map_marker.png',
			iconRetinaUrl:'/images/map_marker.png',
			iconSize:[18, 18],
			iconAnchor:[9, 18],
			popupAnchor:[0, -18]
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



function reload_controls()
{
	for(var i = 0;i<map_controls.length;i++)
	{
		map.removeLayer(map_controls[i]);
	}
	map_controls =[];
		for(i=0;i<connections.length;i++)
		{
			var con = connections[i];
			var name = con.user.name;
			var status =  con.status;
			
			
			var ctrl = L.marker([parseFloat(con.location.coordinates[1]), parseFloat(con.location.coordinates[0])]).addTo(map).bindPopup("<b>"+name + "</b> <br />"+status+"<br />");
			
			map_controls.push(ctrl);
		}

}

reload_controls();