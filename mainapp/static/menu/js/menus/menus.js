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
                    $('.has-success label').text('Menu item successfully added');
                    $('.has-success').show();
                },
                 error: function( jqXhr, textStatus, errorThrown ){
                    console.log( errorThrown );
                }
            });
            return false;
        });

        // dynamically add attribute to the inline form and its elements

         $(".add-dish").on('click' , function(){
            $("#sectionDish form").attr('id', 'addDishForm');
            $("#sectionDish form input").attr('name', 'name');
            $("#sectionDish form button.editable-submit").attr('type', 'button');
            $("#sectionDish form").attr('data-menu-section', $(this).data('menu-section'));
        });



        // dynamically set the menu id to the hidden menu-input in add section form

        $(".add-section").on('click' , function(){
            $("#add_section_form #menuId").attr('value', $(this).data('menu-id'));
        });

        // Add Section form submit

        var section_frm = $('#add_section_form');
        section_frm.submit(function () {

            $.ajax({
                type: section_frm.attr('method'),
                url: section_frm.attr('action'),
                data: section_frm.serialize(),
                success: function( data, textStatus, jQxhr ){
                    $('.modal-header .close').trigger('click');
                    //document.location = document.location;
                    $('.has-success label').text('Section successfully added');
                    $('.has-success').show();
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

        //submit dish add form

        var dish_frm = $('#sectionDish form .editableform');
        $(document).on('click', '#sectionDish .editable-submit', function(){
                data = {'name' : $('#sectionDish form input').val() , 'menu_section' : $(this).parents('form').data('menu-section')};
                $.ajax({
                    type: 'post',
                    url: $('#sectionDish #item').data('url'),
                    data: data,
                    success: function( data, textStatus, jQxhr ){
                       alert('Dish successfully added !')
                       $('#sectionDish .editable-cancel').trigger('click');

                    },
                     error: function( jqXhr, textStatus, errorThrown ){
                        console.log( errorThrown );
                    }
                });
                return false;

         });


         //Autocomplete dish input

         $(document).on("keydown.autocomplete",'#sectionDish input[name="name"]',function(e){
            $(this).autocomplete({
                source: function( request, response ) {
                    $.ajax({
                        dataType: "json",
                        type : 'Get',
                        url: $("#sectionDish #item").data('lookup-url') +'?q='+ $( "#sectionDish input" ).val() ,
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
                 appendTo : '#sectionDish',

            })


         })


        $(document).on('mouseup' , '.editable-container',function (e){

                $(this).off('mouseup.editable-container');
        })


         
    });



    
   
})(jQuery);