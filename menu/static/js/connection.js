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

        $('.nav-tabs > li.active').removeClass('active');
        $("#tab_1").addClass('active');
        $('#tab_1-tab').parent().addClass('active');

        $.ajax({
            url: createConnectionUrl,
            data: data,
            type: 'POST',
            dataType: 'JSON',
            success: function(data) {
                $('#tab_1').html(data.obj.sellers);
                $('#tab_2').html(data.obj.buyers);
                $('.nav-tabs > li.active').removeClass('active');
                $("#tab_" + $('input[name="connection-type"]:checked').val()).addClass('active');
                $('#tab_' + $('input[name="connection-type"]:checked').val() + '-tab').parent().addClass('active');

            }
        });
    });
});
