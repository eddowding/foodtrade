$(document).ready(function() {
  $('.save-btn').click(function (ev) {
    var id = $(this).attr('data-id');
    var data = {operation: 'save', id: id};
    $('#form_' + id).serializeArray().forEach(function (value, index) {
      data[value.name] = value.value;
    });
    $.ajax({
      url: '/tools/location/save/',
      data: data,
      type: 'GET',
      dataType: 'JSON',
      success: function (data) {
        if (data.status) {
          $('#row_' + id).hide();
        }
      }
    });
  });

  $('.ignore-btn').click(function (ev) {
    var id = $(this).attr('data-id');
    var data = {operation: 'ignore', id: id};
    $('#form_' + id).serializeArray().forEach(function (value, index) {
      data[value.name] = value.value;
    });
    $.ajax({
      url: '/tools/location/save/',
      data: data,
      type: 'GET',
      dataType: 'JSON',
      success: function (data) {
        if (data.status) {
          $('#row_' + id).hide();
        }
      }
    });
  });
});
