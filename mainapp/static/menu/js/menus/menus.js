(function($){
    $(document).ready(function() {
      
        $.fn.editable.defaults.mode = 'inline';
        $('.editable').editable();

        //Activate tooltips
        $("[data-toggle='tooltip']").tooltip();
        $(".tooltip").tooltip();
        // Menu tree
        $("ul.my-tree").sortable();
        $(".has-success").hide();


        // Add menu item form submit

        var menu_frm = $('#add_menu_form');
        menu_frm.submit(function () {
            $.ajax({
                type: menu_frm.attr('method'),
                url: menu_frm.attr('action'),
                data: menu_frm.serialize(),
                success: function( data, textStatus, jQxhr ){
                    $('.modal-header .close').trigger('click');
                    //document.location = document.location;
                    $('.box-body .has-success label').text('Menu item successfully added');
                    $('.box-body .has-success').show();
                },
                 error: function( jqXhr, textStatus, errorThrown ){
                    console.log( errorThrown );
                }
            });
            return false;
        });





        // Add menu item form submit

        var section_frm = $('#add_section_form');
        section_frm.submit(function () {
            $.ajax({
                type: section_frm.attr('method'),
                url: section_frm.attr('action'),
                data: section_frm.serialize(),
                success: function( data, textStatus, jQxhr ){
                    $('.modal-header .close').trigger('click');
                    //document.location = document.location;
                    $('.box-body .has-success label').text('Section successfully added');
                    $('.box-body .has-success').show();
                },
                 error: function( jqXhr, textStatus, errorThrown ){
                    console.log( errorThrown );
                }
            });
            return false;
        });

        // Add menu Establishment Autocomplete



        $( "input#menuEstablishment" ).autocomplete({
          source: function( request, response ) {
            $.ajax({
                dataType: "json",
                type : 'Get',
                url: $("input#menuEstablishment").data('lookup-url') +'?q='+ $( "input#menuEstablishment" ).val() ,
                success: function(data) {
                  $('input#menuEstablishment').removeClass('ui-autocomplete-loading');
                  response( $.map( data.objs, function( item ) {
                    //console.log(data.name);
                    return {
                        label: item.name,
                        value: item.name,
                    }
                    }));
              },
              error: function(jqXhr, textStatus, errorThrown) {
                  console.log(errorThrown)
                  $('input#menuEstablishment').removeClass('ui-autocomplete-loading');  // hide loading image
              }
            });
          },
         minLength: 3,
         appendTo : '#show-suggestions',


        });





         
    });
    
    
    
   
})(jQuery);