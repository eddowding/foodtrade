var confirmDelete = function(url) {
  var status = confirm('Are you sure?');
  
  if (status) {
    window.location = url;
  }
};
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

  $('#name').editable();
  $('#public').click(function() {
    $.ajax({
      url: dishAdminUpdateUrl,
      type: 'POST',
      data: {name: 'public', pk: '', value: $(this).is(':checked')}
    });
  });

  $('#ingredient_name').editable();
  $('#is_in_ac').click(function() {
    $.ajax({
      url: ingredientAdminUpdateUrl,
      type: 'POST',
      data: {name: 'is_in_ac', pk: '', value: $(this).is(':checked')}
    });
  });

  $('#user').change(function() {
    $.ajax({
      url: establishmentAdminUpdateUrl,
      type: 'POST',
      data: {name: 'user', pk: '', value: $(this).val()}
    });
  });
});
