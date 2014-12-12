$(document).ready(function() {
    var establishments = new Bloodhound({
        remote: {
            url: establishmentLookupNameUrl + '?q=%QUERY',
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

    $('#menuModal input#establishment').typeahead(null, {
        displayKey: 'name',
        name: 'establishment',
        source: establishments.ttAdapter()
    });

    var establishmentSelected = false;

    $('#menuModal input#establishment').on('typeahead:selected', function(ev, establishment) {
        $('#menuModal input[name="establishment"]').val(establishment.value);
        establishmentSelected = true;
    });

    $('#menuModal button.btn').click(function(ev) {
        var data = {
            'name': $('#menuModal input[name="name"]').val()
        };
        if (establishmentSelected) {
            data.establishment = $('#menuModal input[name="establishment"]').val();
        } else {
            data.establishment = $('#menuModal input#establishment').val();
        }

        $.ajax({
            url: createMenuUrl,
            data: data,
            type: 'POST',
            dataType: 'JSON',
            success: function(data) {
                $('.menus').html(data.html);
                $('#menuModal input[name="establishment"]').val('');
                $('#menuModal input#establishment').val('');
                $('#menuModal input[name="name"]').val('');
                establishmentSelected = false;
            }
        });
    });
});
