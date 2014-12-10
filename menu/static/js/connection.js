$(document).ready(function() {
    var establishments = new Bloodhound({
        remote: {
            url: '/menu/establishment/lookup/name/?q=%QUERY',
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

    $('.connection').typeahead(null, {
        displayKey: 'name',
        name: 'establishment',
        source: establishments.ttAdapter()
    });

    var connectionId = null;

    var objectType = null;

    $('.connection').on('typeahead:selected', function(ev, establishment) {
        connectionId = establishment.value;
        objectType = establishment.type;
        $('.add-connection').removeClass('disabled');
    });

    $('.add-connection').click(function(ev) {
        var connectionType = $('input[name="connection-type"]:checked').val();
        var data = {
            connection_id: connectionId,
            connection_type: connectionType,
            object_type: objectType
        };
        $.ajax({
            url: createConnectionUrl,
            data: data,
            type: 'POST',
            dataType: 'JSON',
            success: function(data) {
                console.log(data);
            }
        });
    });
});
