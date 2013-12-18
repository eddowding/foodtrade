function ajax_request(s_handler, c_handler, input_data)
   $.ajax({
    type: "POST",
    url: "/ajax-handler/"+s_handler,
    data: input_data,
    success: function(data) {
      window[c_handler](data);
    }
});
}



