

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
		}).addTo(map);
L.circle([map_lat,map_lon], 48280.3, {
			color: '#333333',
		}).addTo(map);
	
L.circle([map_lat,map_lon], 160934, {
			color: '#333333',
		}).addTo(map);
		for(i=0;i<connections.length;i++)
		{
			account = SocialAccount.objects.get(user__id = each['c_useruid'])
        usr_pr = userprof.get_profile_by_id(str(each['c_useruid']))
        user_info = UserInfo(each['c_useruid'])
        final_connections.append({'id': each['c_useruid'],
         'name': account.extra_data['name'],
         'description': account.extra_data['description'],
         'photo': account.extra_data['profile_image_url'],
         'username' : account.extra_data['screen_name'],
         'type': usr_pr['type_user'].split(','),
         'trade_conn_no': user_info.trade_connections_no,
         'food_no': user_info.food_no,
         'org_conn_no': user_info.organisation_connection_no
			var con = connections[i];
			var name = con.name;
			var description = con.description;
			var photo =  con.photo;
			var username = con.username;
			var type = con.type;
			var relation = con.relation;
			
			if(isNaN(parseFloat(con.lat)) || isNaN(parseFloat(con.lon)))
			{
				continue;
			}
			
			L.marker([parseFloat(con.lat), parseFloat(con.lon)]).addTo(map).bindPopup("<b>Name: </b>"+name+"<br /><b>Business Type: </b>"+business_type+"<br /> <b>Email: </b>"+ email+"<br/><b>Rating: </b>"+rating+"<br/><b>Address: </b>"+address+"<br /><b>Type: </b>"+type);

			color = 'red';
			if(type=="consumer")
			{
				color = "blue";
			}
			var polyline = L.polyline([
			[parseFloat(center.lat), parseFloat(center.lon)],
			[parseFloat(con.lat), parseFloat(con.lon)]
			],{color: color}).addTo(map)
		}

