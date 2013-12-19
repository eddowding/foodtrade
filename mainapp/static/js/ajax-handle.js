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