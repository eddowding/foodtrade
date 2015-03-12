$(document).ready(function() {
  $.fn.editable.defaults.mode = 'inline';
  $('#email').editable();
  $('#superuser').click(function() {
    $.ajax({
      url: userAdminUpdateUrl,
      type: 'POST',
      data: {name: 'superuser', pk: '', value: $(this).is(':checked')}
    });
  });
});
