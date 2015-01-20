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
    
    /*$('.connection_stockists').typeahead(null, {
        displayKey: 'name',
        name: 'establishment',
        source: establishments.ttAdapter()
    });*/

    var connectionId = null;

    var objectType = null;
    
    //var connectionType = null;
    
    $('.connection-type').on('typeahead:selected', function(ev, establishment) {
        connectionId = establishment.value;
        objectType = establishment.type;
        $('.add-connection').removeClass('disabled');
    });

    $('.connection').on('typeahead:selected', function(ev, establishment) {
        connectionId = establishment.value;
        objectType = establishment.type;
        $('.add-connection').removeClass('disabled');
    });
    
    /*$('.connection_stockists').on('typeahead:selected', function(ev, establishment) {
        connectionId = establishment.value;
        objectType = establishment.type;
        $('.add-connection').removeClass('disabled');
    });*/


    $('.add-connection').click(function(ev) {
    	var tabid = $('.nav-tabs > li.active > a').attr('id');
    	if (tabid == 'tab_1-tab'){
    		connectionType = '1';
    	}
    	else if (tabid == 'tab_2-tab'){
    		connectionType = '2';
    	}
    	else{
        	var connectionType = $('input[name="connection-type"]:checked').val();
       }
        var data = {
            connection_id: connectionId,
            connection_type: connectionType,
            object_type: objectType
        };

        //$('.nav-tabs > li.active').removeClass('active');
        //$("#tab_1").addClass('active');
        //$('#tab_1-tab').parent().addClass('active');

        $.ajax({
            url: createConnectionUrl,
            data: data,
            type: 'POST',
            dataType: 'JSON',
            success: function(data) {
            	$('#suppliers').html(data.obj.sellers);
                $('#stockists').html(data.obj.buyers);
                $('.nav-tabs > li.active').removeClass('active');
                if (connectionType == '1'){
                	//$("#tab_1-tab").addClass('active');
                	//$("#tab_1-tab").parent().addClass('active');
                	$("#tab_1-tab" ).trigger( "click" );
                }
                else if (connectionType == '2'){
                	//$("#tab_2-tab").addClass('active');
                	//$("#tab_2-tab").parent().addClass('active');
                	$("#tab_2-tab" ).trigger( "click" );
                }
                //establishments.initialize();
                //$("#tab_" + $('input[name="connection-type"]:checked').val()).addClass('active');
                //$('#tab_' + $('input[name="connection-type"]:checked').val() + '-tab').parent().addClass('active');

            }
        });
    });
});
