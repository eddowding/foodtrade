function ajax_request(s_handler, c_handler, input_data)
{
   $.ajax({
    type: "POST",
    url: "/ajax-handler/"+s_handler,
    data: input_data,
    success: function(data) {
      window[c_handler](data);
    }
});
}


function PostStatus(status_val)
{
	ajax_request("post_tweet", 'CloseNewPostModal', {message: status_val});
}



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
	if($('#'+reply_id).val().trim()==mentions)
	{
	$('#'+reply_id).val("");
	}
}


var nnn;
$('.enterhandler').bind('keypress', function(e) {
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
});