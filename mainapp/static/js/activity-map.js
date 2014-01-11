

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