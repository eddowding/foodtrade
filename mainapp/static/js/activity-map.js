

var connections = [];
var map = L.map('map').setView([map_lat,map_lon], 12);

		L.tileLayer('http://{s}.tile.cloudmade.com/BC9A493B41014CAABB98F0471D759707/997/256/{z}/{x}/{y}.png', {
			maxZoom: 18,
			attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>'
		}).addTo(map);

	

		for(i=0;i<connections.length;i++)
		{
			var con = connections[i];
			var first_name = con.firstname;
			var last_name =  con.lastname;
			var blood_group = con.blood_group;
			var twitter = con.twitter;

			
			
			L.marker([parseFloat(con.lat), parseFloat(con.lon)]).addTo(map).bindPopup("<b>Name: </b>"+first_name + " "+last_name +"<br /><b>Twitter: </b>"+twitter+"<br /><b>Blood Group: </b>"+blood_group);
			
			
		}


