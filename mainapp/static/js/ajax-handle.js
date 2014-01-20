global_this = '';
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


function conn_handler(value, prof_id, conn_id)
{
	conn_id = typeof conn_id !== 'undefined' ? conn_id : 0;
	if (validate_login()['status'] == '1'){
				if (value == 'buy_from'){
					var buy = document.getElementById('buy_from').checked
					if (buy==true){
						// create connection of logged in user and profile user
						ajax_request("add_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'}"});
					}
					else{
						// delete connection
						ajax_request("del_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'}"})
					}
				}
				else if(value == "sell_to")
				{
					var sell = document.getElementById('sell_to').checked
					if (sell==true){
						// create connection of logged in user and profile user
						ajax_request("add_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'sell_to'}"});
					}
					else{
						// delete connection
						ajax_request("del_connection", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +",'status': 'sell_to'}"});
					}

				}
				else if(value == "close_buy_from"){
					
					ajax_request("profile_user_delete_conn", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'buy_from'" + ", 'conn_id': " + conn_id +"}"});
				}
				else if(value == "close_sell_to"){
					
					ajax_request("profile_user_delete_conn", 'conn_ajax', {conn_data: "{'prof_id': " +prof_id +", 'status': 'sell_to'" + ", 'conn_id': " + conn_id +"}"});
				}				
	}
	else{
		$('#ad_cons_id').tooltip('show');
	}
}

function third_party_connection(prof_id){
	var business_id = $('#buss_chosen').val().join('');
	// buyer checked
	if($('#option1_conn').is(':checked')){
		// var conn_data = {prof_id: prof_id, status: 'buy_from', buss_id: businesses_id };
		ajax_request("third_party_conn", 'conn_ajax', {conn_data: "{'prof_id': " + prof_id + ",'buss_id': " + business_id + ",'status': 'buy_from'}"});
		
	}
	// seller checked
	if($('#option2_conn').is(':checked')){
		// var conn_data = {prof_id: prof_id, status: 'sell_to', buss_id: businesses_id };
		ajax_request("third_party_conn", 'conn_ajax', {conn_data: "{'prof_id': " + prof_id + ",'buss_id': " + business_id + ",'status': 'sell_to'}"});
	}
	// $('.search-choice').remove();
	// $("#buss_chosen").val('');
}
function conn_ajax(data){
// clear selected choice
$('.search-choice').remove();
$("#buss_chosen").val('').trigger('chosen:updated');

$('#all-connections').html(data);
reload_connections();
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
		// var food = document.getElementsByClassName('chosen-single')[0].children[0].innerHTML;
		var elements = document.getElementsByClassName('search-choice');
	    var food = elements[0].children[0].innerHTML;
	    // alert(food);
		var data = {useruid: prof_id, food_name: food};
		ajax_request("addfood", 'create_conn', {data: JSON.stringify(data)});
		// document.getElementsByClassName('chosen-single')[0].children[0].innerHTML = '';
		// $('#myselect').trigger('chosen:open');
		$('.search-choice').remove();
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

function add_member(org_id, mem_id){
	var checked = $('.member-chkbx').is(':checked');
	var data = {orguid: org_id, memberuid: mem_id};
	if (checked){
		// add member
		ajax_request("addmember", 'create_conn', {data: JSON.stringify(data)});
	}
	else{
		// delete that member
		ajax_request("deletemember", 'create_conn', {data: JSON.stringify(data)});
	}
	
}

function add_team(org_id, team_id){
	// var data = {orguid: org_id, memberuid: team_id};
	// ajax_request("addteam", 'create_conn', {data: JSON.stringify(data)});
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

function ShowReply(reply_id, mentions)
{
	if(validate_login()['status'] == '1'){
		if($('#'+reply_id).val()=="")
		{
		$('#'+reply_id).val(mentions+" ");
		}
	}
	else{
		window.location='/accounts/twitter/login/?process=login'
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
		/*$('#' + String(this.attributes.id.value)).tooltip('show');*/
		  /*alert("roshan");*/
		  window.location = '/accounts/twitter/login/?process=login';
	}
});

/*function ajax_success_validate_logged_in(data){
	alert(data);
	data = jQuery.parseJSON(data);
	loggedIn = data['status'];
 }*/
