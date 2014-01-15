global_this = '';
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

function conn_handler(value, prof_id)
{
	if (validate_login()['status'] == '1'){
				if (value == 'buy_from'){
					var buy = document.getElementById('buy_from').checked
					if (buy==true){
						// create connection of logged in user and profile user
						ajax_request("add_connection", 'create_conn', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'}"});
					}
					else{
						// delete connection
						ajax_request("del_connection", 'create_conn', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'}"})
					}
				}
				else
				{
					var sell = document.getElementById('sell_to').checked
					if (sell==true){
						// create connection of logged in user and profile user
						ajax_request("add_connection", 'create_conn', {conn_data: "{'prof_id': " +prof_id +", 'status': 'sell_to'}"});
					}
					else{
						// delete connection
						ajax_request("del_connection", 'create_conn', {conn_data: "{'prof_id': " +prof_id +",'status': 'sell_to'}"});
					}

				}
	}
	else{
		$('#ad_cons_id').tooltip('show');
	}
}

function third_party_connection(prof_id){
	alert('third_party_connection');
	var business_id = $('#ddl_try').val();
	// buyer checked
	console.log(typeof(business_id));
	if($('#option1_conn').is(':checked')){
		// var conn_data = {prof_id: prof_id, status: 'buy_from', buss_id: businesses_id };
		ajax_request("third_party_conn", 'create_conn', {conn_data: "{'prof_id': " + prof_id + ",'buss_id': " + business_id + ",'status': 'buy_from'}"});
	}
	// seller checked
	if($('#option2_conn').is(':checked')){
		// var conn_data = {prof_id: prof_id, status: 'sell_to', buss_id: businesses_id };
		ajax_request("third_party_conn", 'create_conn', {conn_data: "{'prof_id': " + prof_id + ",'buss_id': " + business_id + ",'status': 'sell_to'}"});
	}
}
function create_conn(){
	
}

function invite_connect(prof_username, logged_username){
	var message = "Hey, "+ prof_username + " - you may like @foodtradeHQ - the 'dating site for food businesses' #realfood. We're there [http://foodtrade.com/profile/"+logged_username+"]";
	ajax_request("post_tweet_admin", 'create_conn', {message: message});
}

function add_food(prof_id){
	// var food = document.getElementById('addfood_id').value;
	if (validate_login()['status'] == '1'){
		var food = document.getElementsByClassName('chosen-single')[0].children[0].innerHTML;
		var data = {useruid: prof_id, food_name: food};
		ajax_request("addfood", 'create_conn', {data: JSON.stringify(data)});
		document.getElementsByClassName('chosen-single')[0].children[0].innerHTML = '';
		var append_data = '<tr><td>'+food+'</td><td><div class="pull-right"><a href="#"><i class="fa fa-heart-o" title="Vouch for this"></i></a></div></td></tr>';
		$("#food_tbody").prepend(append_data);
	}
	else{
		$('#adfoo_id').tooltip('show');
	}

}

function recommend_food(logged_in_id, food_name, prof_id){
	var data = {recommender_id: logged_in_id, food_name: food_name, business_id: prof_id}
	ajax_request("vouch_for_food", 'create_conn', {data: JSON.stringify(data)});

}

function delete_food(prof_id, food_name, my_this){
	var data = {useruid: prof_id, food_name: food_name};
	ajax_request("deletefood", 'create_conn', {data: JSON.stringify(data)});
	global_this = my_this;
	var del_id = global_this.parentElement.parentElement.parentElement.parentElement.getAttribute('id');
	$('#'+del_id).remove();
}

function add_customer(prof_id, c_id){
	var data = {useruid: prof_id, customeruid: c_id};
	ajax_request("addcustomer", 'create_conn', {data: JSON.stringify(data)});
}

function add_member(org_id, mem_id){
	var data = {orguid: org_id, memberuid: mem_id};
	ajax_request("addmember", 'create_conn', {data: JSON.stringify(data)});
}

function add_team(org_id, team_id){
	var data = {orguid: org_id, memberuid: team_id};
	ajax_request("addteam", 'create_conn', {data: JSON.stringify(data)});
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

function UpdateStatus(id_name)
{
	message = $('#'+id_name).val();
	if(message=="")
	{
		alert("You can't post empty status.");
		return;
	}

	ajax_request("post_tweet", 'CloseNewPostModal', {message: message});	
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
		$('#btn_update_activity').tooltip('show');
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

function ShowReply(reply_id, mentions)
{
	if($('#'+reply_id).val()=="")
	{
	$('#'+reply_id).val(mentions+" ");
	}
}


function BlurReply(reply_id, mentions)
{
	if($('#'+reply_id).val().trim()==mentions){
		$('#'+reply_id).val("");
	}
}


var nnn;
$('.enterhandler').bind('keypress', function(e) {
	if(validate_login()['status'] == '1'){
		var code = e.keyCode || e.which;
		 if(code == 13) { //Enter keycode
		   //Do something
		   status_msg =this.value;
		   if(status_msg=="")
		   {
		   		return;
		   }
		   PostStatus(status_msg);
		   this.value=0;
		 }
	}
	else{
		/*$('#btn_must_be_logged').click();*/
		$('#' + String(this.attributes.id.value)).tooltip('show');
	}
});

/*function ajax_success_validate_logged_in(data){
	alert(data);
	data = jQuery.parseJSON(data);
	loggedIn = data['status'];
 }*/
