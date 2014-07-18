global_this = '';
vouch_this = '';
var friends;
function ajax_request(s_handler, c_handler, input_data)
{
   $.ajax({
    type: "POST",
    url: "/ajax-handler/" + s_handler,
    data: input_data,
    success: function(data) {
      window[c_handler](data);
    }
});
}

function tweetlistener(input, counter, button){
    $('#'+input).change(function(){
        checktweet(input, counter, button);
    });
    $('#'+input).keyup(function(){
        checktweet(input, counter, button);
    });
}

function checktweet(input, counter, button){
    var tweettext = $("#"+input).val();
    var char = 120- parseInt(tweettext.length);
    if(char <= 0){
        $("#"+counter).text('');
        $('#'+button).attr('disabled', 'disabled');
    }
    else{
        $("#"+counter).text(char+' characters remaining');
        $('#'+button).removeAttr('disabled');
    }
}
    
function save_favourites(profile_id, user_id){
	if($('#favourite_btn').prop('checked')==true){
		if(profile_id!=user_id){
			ajax_request("save_favourites", 'empty', {data: "{'profile_id': " + parseInt(profile_id) + ",'useruid': " + parseInt(user_id) +"}"});
		}	
	}
	else{
		if(profile_id!=user_id){
				ajax_request("save_favourites", 'empty', {data: "{'profile_id': " + parseInt(profile_id) + ",'useruid': " + parseInt(user_id) +",'delete': " + 1 +"}"});
			}		
	}
	

}

function add_org_to_biz(member_id, orguid){
	// var org_ids_list = $('#org_chosen').val();
	// for(i=0;i<org_ids_list.length;i++){
	ajax_request("third_party_add_org", 'org_ajax_add', {data: "{'memberuid': " + member_id + ",'orguid': " + parseInt(orguid) +"}"});
	// }
}
// get business tags
function get_business_tags(){
ajax_request("get_business_tags", 'signup_tags_ajax', {data: "{'abc': 'abc' }"});
}

function signup_tags_ajax(data){
$('#business_tags_id').html(data);
$("#business_tags_id").trigger('chosen:updated');
}

function del_org_from_biz(member_id, org_id){
ajax_request("third_party_delete_org", 'org_ajax', {data: "{'memberuid': " + member_id + ",'orguid': " + org_id +"}"});
}

function org_ajax(data){
	data= jQuery.parseJSON(data);
	if(data['status']=='ok'){
		$('.search-choice').remove();
		$("#org_chosen").val('').trigger('chosen:updated');
		$('#groupsGrid').html(data['html']);
		$('#orgConnNo').html('');
		$('#orgConnNo').html(data['org_count']);
	}
}

function org_ajax_add(data){
	data= jQuery.parseJSON(data);
	if(data['status']=='ok'){
		$('#groupsGrid').html(data['html']);
		$('#orgConnNo').html('');
		$('#orgConnNo').html(data['org_count']);
	}
}
function conn_handler(value, prof_id, conn_id)
{
	conn_id = typeof conn_id !== 'undefined' ? conn_id : 0;
	if (validate_login()['status'] == '1'){
				if (value == 'buy_from'){
					var buy = document.getElementById('buy_from').checked
					if (buy==true){
						// create connection of logged in user and profile user
						// ajax_request("add_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'}"});
						ajax_request("add_connection", 'suppliers_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'sell_to'}"});
					}
					else{

						footable_row = $("#stockist_connections tr.self_conn");
						// delete connection
						// ajax_request("del_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'}"})
						ajax_request("del_connection", 'suppliers_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'sell_to'}"})
					}
				}
				else if(value == "sell_to")
				{
					var sell = document.getElementById('sell_to').checked
					if (sell==true){
						// create connection of logged in user and profile user
						// ajax_request("add_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'sell_to'}"});
						ajax_request("add_connection", 'stockists_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'}"});
					}
					else{
						footable_row = $("#supplier_connections tr.self_conn");
						// delete connection
						// ajax_request("del_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +",'status': 'sell_to'}"});
						ajax_request("del_connection", 'stockists_ajax', {conn_data: "{'prof_id': " +prof_id +",'status': 'buy_from'}"});
					}

				}
				else if(value == "close_buy_from"){
						ajax_request("profile_user_delete_conn", 'stockists_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'" + ", 'conn_id': " + conn_id +"}"});
						/*ajax_request("del_connection", 'stockists_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'" + ", 'conn_id': " + conn_id +"}"});*/

				}
				else if(value == "close_sell_to"){				
					ajax_request("profile_user_delete_conn", 'suppliers_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'sell_to'" + ", 'conn_id': " + conn_id +"}"});
					/*ajax_request("del_connection", 'suppliers_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'sell_to'" + ", 'conn_id': " + conn_id +"}"});*/
				}				
	}
	else{
		$('#ad_cons_id').tooltip('show');
	}
}

function third_party_connection(prof_id, buss_var, link_type){
	// var business_id = $('#buss_chosen').val().join('');
	// var business_ids_list = $('#buss_chosen').val();

	// for(i=0;i<business_ids_list.length;i++){
	// buyer checked

	if(link_type=='stockists' && buss_var!=""){
		// var conn_data = {prof_id: prof_id, status: 'buy_from', buss_id: businesses_id };
		ajax_request("third_party_conn", 'stockists_ajax', {conn_data: "{'prof_id': " + prof_id + ",'buss_id': " + parseInt(buss_var) + ",'status': 'buy_from'}"});
		
	}
	// seller checked
	if(link_type=='suppliers' && buss_var!=""){
		// var conn_data = {prof_id: prof_id, status: 'sell_to', buss_id: businesses_id };
		ajax_request("third_party_conn", 'suppliers_ajax', {conn_data: "{'prof_id': " + prof_id + ",'buss_id': " + parseInt(buss_var) + ",'status': 'sell_to'}"});
	}
	// }
	
}

function plot_connection_layers_on_map(connection){
	var max_lat = parseFloat(map_lat);
	var min_lat = parseFloat(map_lat);
	var max_lon = parseFloat(map_lon);
	var min_lon = parseFloat(map_lon);	
	var con = connection;
	var name = con['name'];
	// var name = con.business_org_name;
	var description = con['description'];
	var photo =  con['profile_img'];
	var username = con['username'];
	var type = con['type_user'];
	var relation = con.relation;
	var latitude =  con['latlng']['coordinates'][1];
	var longitude =  con['latlng']['coordinates'][0];
	var current_lat = parseFloat(latitude);
	var current_lon = parseFloat(longitude);
	if (current_lat==undefined || current_lon ==undefined){
		return
	}
	if(parseInt(current_lon) == parseInt(def_lon) && parseInt(def_lat) == parseInt(current_lat)){
		return;
	}
	if(current_lat>max_lat){
		max_lat = current_lat;
	}
	if(current_lat<min_lat){
		min_lat = current_lat;
	}
	if(current_lon>max_lon){
		max_lon = current_lon;
	}

	if(current_lon<min_lon){
		min_lon = current_lon;
	}

	color = '#890D2F';
	if(relation=="buyer"){
		color = "#FC8628";
	}

	if(parseInt(current_lon) != parseInt(def_lon) || parseInt(def_lat) != parseInt(current_lat)){
		var polyline = L.polyline([
			[parseFloat(map_lat), parseFloat(map_lon)],
			[parseFloat(latitude), parseFloat(longitude)]
			],{
			color: color,
			weight: 2,
			opacity: 0.8
			}).addTo(map);

		/*map_controls.push(polyline);*/
		lines_dic[username] = polyline;
	}

	var card_str = '<div class="card-box"><div class="content text-center"><div class=""><a href="/profile/'+username+'"><img src="'+photo+'" alt="'+name+'" class="img-circle img-thumbnail img-responsive" style="width:73px;" /></a>';
		card_str += '</div><div class="text"><h3><a href="/profile/'+username+'">'+name+'</a></h3>';
	
	if(type.length>0){
		card_str += '<div class="clearfix">';
	for(var j=0;j<type.length;j++){  
		card_str +=  '<a class="" href="/activity/?q='+type[j]+'">'+type[j]+'</a>';
	}
		card_str += '</div>';
	}

	card_str += '<p>'+description+'</p></div>';
	card_str += '<a href="/profile/'+username+'" class="btn btn-primary btn-sm">View profile &raquo;</a></div> </div>';    

	var ctrl = L.marker([parseFloat(current_lat), parseFloat(current_lon)], {icon: redIcon}).addTo(map).bindPopup(card_str);			
	control_dict[username] = ctrl;
	/*map_controls.push(ctrl);*/
}

function remove_con(username1)
{
	cnt = control_dict[username1];
	cnt1 = lines_dic[username1];
	map.removeLayer(cnt);
	map.removeLayer(cnt1);
}

function stockists_ajax(data){
	new_dat = data;
	data = jQuery.parseJSON(data);
	if(data['status']=='ok'){
		if(data['action']=='delete'){
			try{
			$('[data-title="' + data['username'] + '"]').parent().remove();
        	myfootable.removeRow(footable_row);
		}
		catch(e){
			footable_row.remove();
		}

			//delete the row
			
			remove_con(data['username']);		
		}
		else{
			$('.search-choice').remove();
			current_html = $("#supplier_connections").html();
			new_html =  data['html'] + current_html;
			$("#supplier_connections").html(new_html);
			
		 	$('#suppliersTable').trigger('footable_initialize');
            $('#stockistsTable').trigger('footable_resize');
            $('#suppliersTable').trigger('footable_initialize');
            $('#suppliersTable').trigger('footable_resize');
		}

        	$('#c_con_no').html(data['b_conn_no']);
			$('#b_con_no').html(data['c_conn_no']);	
	}
}


function suppliers_ajax(data){
	// clear selected choice	
		data=jQuery.parseJSON(data);
		if(data['action'] == 'delete'){
			try{
			$('[data-title="' + data['username'] + '"]').parent().remove();
        	myfootable.removeRow(footable_row);
		}
		catch(e){
			footable_row.remove();
		}


			new_connections = connections;						
			//delete the row      	
			remove_con(data['username']);
		}		
		else{
			$('.search-choice').remove();
			// $("#buss_chosen").val('').trigger('chosen:updated');
			current_html = $('#stockist_connections').html();

			new_html =  data['html'] + current_html;
			$('#stockist_connections').html(new_html);	
			$('#stockistsTable').trigger('footable_initialize');
          	$('#stockistsTable').trigger('footable_resize');
          	$('#stockistsTable').trigger('footable_initialize');
          	$('#stockistsTable').trigger('footable_resize');
          	
		}


        	$('#c_con_no').html(data['b_conn_no']);
			$('#b_con_no').html(data['c_conn_no']);	
}

function get_next_page_b_conn(buss_username, current_conn_page){
	ajax_request('pull_connections', 'get_next_page_conn_success', {'username':buss_username,'page_num':current_conn_page, 'type':'b'});
}

function get_next_page_c_conn(buss_username, current_conn_page){
	ajax_request('pull_connections', 'get_next_page_conn_success', {'username':buss_username,'page_num':current_conn_page, 'type':'c'});	
}

function get_next_page_conn_success(data){
	data = jQuery.parseJSON(data);
	if (data['status']=='ok'){
		conn_arr = data['conn_data'];

		for (var i=0; i<conn_arr.length; i++){
			if (conn_arr[i]['user']['address'] != 'Antartica'){
				plot_connection_layers_on_map(conn_arr[i]['user']);				
			}
		}
		if (data['type']=='b'){								  
			$('#suppliers_connections').prepend(data['table_html']);
		}
		else{
			$('#stockist_connections').prepend(data['table_html']);			
		}

		if(data['type']=='b'){
			get_next_page_b_conn(data['username'], data['next_page_num']);			
		}
		else{
			get_next_page_c_conn(data['username'], data['next_page_num']);				
		}
	}
	else{
		  $('#suppliersTable').trigger('footable_initialize');
          $('#stockistsTable').trigger('footable_resize');
          $('#suppliersTable').trigger('footable_initialize');
          $('#suppliersTable').trigger('footable_resize');
	}
}



function create_conn(){
	location.reload();
}

function invite_connect(prof_username, logged_username){
	var message = "Hey, "+ prof_username + " - you may like @foodtradeHQ - the 'dating site for food businesses' #realfood. We're there [http://foodtrade.com/profile/"+logged_username+"]";
	ajax_request("post_tweet_admin", 'create_conn', {message: message});
}

function add_food(prof_id, we_buy){
	if (validate_login()['status'] == '1'){
		
		// var elements = document.getElementsByClassName('search-choice');
	    // var food = elements[0].children[0].innerHTML;
	    var food = $('.search-choice').children()[0].innerHTML;
	    we_buy = typeof we_buy !== 'undefined' ? we_buy : '';
	    var data = {useruid: prof_id, food_name: food};
	    data['we_buy'] = we_buy== '' ? 0 : 1;
	    if(data['we_buy']==1){
			ajax_request("addfood", 'webuy_food_ajax', {data: JSON.stringify(data)});
	    }
	    else{
			ajax_request("addfood", 'food_ajax', {data: JSON.stringify(data)});
		}
	}
	else{
		$('#adfoo_id').tooltip('show');
	}

}

function food_ajax(data){
$('.search-choice').remove();
$("#myselect").val('').trigger('chosen:updated');
$('#ajax_food_tr').html(data);

$('#produceTable').trigger('footable_initialize');
$('#produceTable').trigger('footable_resize');
$('#produceTable').trigger('footable_initialize');
$('#produceTable').trigger('footable_resize');
// var $container1 = $('#foods').isotope({itemSelector: '.food'});
}

function webuy_food_ajax(data){
$('.search-choice').remove();
$("#webuy_select").val('').trigger('chosen:updated');
$('#webuy_foods').html(data);
$('#webuy_foods').trigger('footable_initialize');
$('#webuy_foods').trigger('footable_resize');
$('#webuy_foods').trigger('footable_initialize');
$('#webuy_foods').trigger('footable_resize');
/*var $container1 = $('#webuy_foods').isotope({itemSelector: '.food'});*/
}

function recommend_food(logged_in_id, food_name, prof_id, username, my_this, we_buy){
	var data = {recommender_id: logged_in_id, food_name: food_name, business_id: prof_id, action: 'add'};
	vouch_this = my_this;
	we_buy = typeof we_buy !== 'undefined' ? we_buy : '';
    data['we_buy'] = we_buy== '' ? 0 : 1;
	if(!(vouch_this.checked)){
		var url = window.location.href;
		msg = "I've just vouched for #" + food_name.toLocaleLowerCase() + " from " + username + " " + url;
		$('#tweet-recomm').val(msg);
	}
	else{
		data['action'] = 'remove';
	}
	console.log(data);
	if(data['we_buy']==1){
		ajax_request("vouch_for_food", 'webuy_food_ajax', {data: JSON.stringify(data)});	
	}
	else{
		ajax_request("vouch_for_food", 'food_ajax', {data: JSON.stringify(data)});
	}
	// ajax_request("vouch_for_food", 'empty', {data: JSON.stringify(data)});
}

function empty(){}


function delete_food(prof_id, food_name, my_this, we_buy){
	we_buy = typeof we_buy !== 'undefined' ? we_buy : '';
	var data = {useruid: prof_id, food_name: food_name};
	data['we_buy'] = we_buy== '' ? 0 : 1;
    if(data['we_buy']==1){
		ajax_request("deletefood", 'webuy_food_ajax', {data: JSON.stringify(data)});
	}
	else{
		ajax_request("deletefood", 'food_ajax', {data: JSON.stringify(data)});
	}
	global_this = my_this;

	// var del_id = global_this.parentElement.parentElement.parentElement.parentElement.getAttribute('id');
	// var del_id = global_this.parentElement.parentElement.parentElement.parentElement.parentElement.getAttribute('id');
	// $('#'+del_id).remove();
}

function add_customer(prof_id, c_id){
	var checked = $('#customer-chkbx').is(':checked');
	var data = {useruid: prof_id, customeruid: c_id};
	if (checked){
		// add customer
		ajax_request("addcustomer", 'create_conn', {data: JSON.stringify(data)});
	}
	else{
		// delete that customer
		ajax_request("deletecustomer", 'create_conn', {data: JSON.stringify(data)});
	}
	
}

function add_member(org_id, mem_id, action){
	var data = {orguid: org_id, memberuid: parseInt(mem_id)};
	if(action == 'self'){
		var checked = $('.member-chkbx').is(':checked');
		if (checked){
			// add member
			ajax_request("addmember", 'member_ajax', {data: JSON.stringify(data)});
		}
		else{
			// delete that member
			ajax_request("deletemember", 'member_ajax', {data: JSON.stringify(data)});
		}
	}
	else if(action == 'third_add'){
		ajax_request("addmember", 'member_ajax', {data: JSON.stringify(data)});
	}
	else if(action == 'third_delete'){
		ajax_request("deletemember", 'member_ajax', {data: JSON.stringify(data)});
	}
}

function member_ajax(data){
	$('#member_ajax').html(data);
}

function add_team(org_id, team_id){
	// var data = {orguid: org_id, memberuid: team_id};
	// ajax_request("addteam", 'create_conn', {data: JSON.stringify(data)});
	console.log(org_id);
	console.log(team_id);
	var checked = $('#team-chkbx').is(':checked');
	var data = {orguid: org_id, memberuid: team_id};
	if (checked){
		// add member
		ajax_request("addteam", 'create_conn', {data: JSON.stringify(data)});
	}
	else{
		// delete that member
		ajax_request("deleteteam", 'create_conn', {data: JSON.stringify(data)});
	}
}

function PostStatus(status_val)
{
	ajax_request("post_tweet", 'CloseNewPostModal', {message: status_val});
}

// function CreateConnection(b_useruid, c_useruid)
// {
// 	ajax_request("add_connection", 'create_conn', {conn_data: {'b_useruid'; b_useruid, 'c_useruid': c_useruid}});
// }

// function DeleteConnection(b_useruid, c_useruid)
// {
// 	ajax_request("del_connection", 'del_conn', {conn_data: {'b_useruid'; b_useruid, 'c_useruid': c_useruid}});
// }

function UpdateStatus(id_name, noappend)
{
	noappend = typeof noappend !== 'undefined' ? noappend : '';
	message = $('#'+id_name).val();
	if(message=="")
	{
		alert("You can't post empty status.");
		return;
	}
	if(noappend == 'noappend'){
		ajax_request("post_tweet", 'CloseNewPostModal', {message: message, noappend: 'noappend'});
	}
	else{
		ajax_request("post_tweet", 'CloseNewPostModal', {message: message});
	}
}

var loggedIn = '';
function UpdateActivity(id_name)
{
	message = $('#'+id_name).val();
	if(message=="")
	{
		alert("You can't post empty status.");
		return;
	}
	if(validate_login()['status'] == '1'){
		ajax_request("post_tweet", 'update_activity', {message: message});
	}
	else{
		/*$('#btn_must_be_logged').click();*/
		/*$('#btn_update_activity').tooltip('show');*/
		window.location('/accounts/twitter/login/?process=?login');
	}	
}

function update_activity(status_id)
{
	message = $('#newstatus').val();
	activity_html = $('#status_template').html();
	activity_html = activity_html.replace('===status===',message);
	$('ul.chat').prepend(activity_html);
	$('#newstatus').val("");
}



function CloseNewPostModal()
{
	$('#newtwitterpost').modal('hide');
}















/*function ajax_success_validate_logged_in(data){
	alert(data);
	data = jQuery.parseJSON(data);
	loggedIn = data['status'];
 }*/
