$(document).ready(function() {
  if (establishmentCount == 0) {
    $('#addEstablishmentModal').modal('show');
  }

  var establishments = new Bloodhound({
    remote: {
      url: establishmentLookupNameUrl + '?q=%QUERY&_tmp=' + (new Date).getTime(),
      filter: function(establishments) {
        return establishments.objs;
      }

    },
    datumTokenizer: function(establishment) {
      return Bloodhound.tokenizers.whitespace(establishment.name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace
  });

  establishments.initialize();

  $('#addEstablishmentModal input#establishment').typeahead(null, {
    displayKey: 'name',
    name: 'establishment',
    source: establishments.ttAdapter()
  });

  var establishmentSelected = false;

  $('#addEstablishmentModal input#establishment').on('typeahead:selected', function(ev, establishment) {
    $('#addEstablishmentModal input[name="establishment"]').val(establishment.value);
    establishmentSelected = true;
  });

  $('#addEstablishmentModal').keypress(function(e) {
    var key = e.which;
    if (key == 13) // the enter key code
    {
      $('#addEstablishmentModal button.btn').click();
      return false;
    }
  });

  $('#addEstablishmentModal button.btn').click(function(ev) {
    var data = {};
    if (establishmentSelected) {
      data.establishment = $('#addEstablishmentModal input[name="establishment"]').val();
    } else {
      data.establishment = $('#addEstablishmentModal input#establishment').val();
    }

    $.ajax({
      url: createEstablishmentUrl + '?_tmp=' + (new Date).getTime(),
      data: data,
      type: 'POST',
      dataType: 'JSON',
      success: function(data) {
        if (data.status) {
          $('#addEstablishmentModal input[name="establishment"]').val('');
          $('#addEstablishmentModal input#establishment').val('');
          $('#addEstablishmentModal input[name="name"]').val('');
          establishmentSelected = false;
          window.location.reload();
        }
      }
    });
  });
});
