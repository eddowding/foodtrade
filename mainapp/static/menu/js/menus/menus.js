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

       /* // dynamically add attribute to the inline form and its elements

         $(".add-dish").on('click' , function(){
            $("#sectionDish form").attr('id', 'addDishForm');
            $("#sectionDish form input").attr('name', 'name');
            $("#sectionDish form button.editable-submit").attr('type', 'button');
            $("#sectionDish form").attr('data-menu-section', $(this).data('menu-section'));
        });*/



        // dynamically set the menu id to the hidden menu-input in add section form

        $(".add-section").on('click' , function(){
            $("#add_section_form #menuId").attr('value', $(this).data('menu-id'));
        });



         // dynamically set the menu section id to the hidden menu-section input in add dish form

        $(".add-dish").on('click' , function(){
            $("#add_dish_form #menuSectionId").attr('value', $(this).data('menu-section-id'));
        });


        // dynamically set the dish id to the hidden dish input in add ingredients form

        $(".add-ingredients").on('click' , function(){
            $("#add_ingredients_form #dishId").attr('value', $(this).data('dish-id'));
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

        var dish_frm = $('#add_dish_form');
        $(document).on("submit","#add_dish_form",function (e) {
            e.preventDefault();
            $.ajax({
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                data: $(this).serialize(),
                dataType: 'json',
                success: function( data, textStatus, jQxhr ){
                    if (data.status == true ){
                        $('.modal-header .close').trigger('click');
                       // document.location = document.location;
                        $('.has-success label').text('Dish successfully added');
                        $('.has-success').show();
                    }

                },
                 error: function( jqXhr, textStatus, errorThrown ){
                    console.log( errorThrown );
                }
            });

        });

             //Autocomplete dish input

         $(document).on("keydown.autocomplete",'#dishName',function(e){
            $(this).autocomplete({
                source: function( request, response ) {
                    $.ajax({
                        dataType: "json",
                        type : 'Get',
                        url: $("#dishName").data('lookup-url') +'?q='+ $( "#dishName" ).val() ,
                        success: function(data) {
                          $('input#dishName').removeClass('ui-autocomplete-loading');
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

            })


         })




        // Submit add ingredients form

        $(document).on("submit","#add_ingredients_form",function (e) {
            e.preventDefault();
            $.ajax({
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                data: $(this).serialize(),
                dataType: 'json',
                success: function( data, textStatus, jQxhr ){
                    if (data.status == true ){
                        $('.modal-header .close').trigger('click');
                       // document.location = document.location;
                        $('.has-success label').text('Ingredients successfully added');
                        $('.has-success').show();
                    }

                },
                 error: function( jqXhr, textStatus, errorThrown ){
                    console.log( errorThrown );
                }
            });

        });


         
    });



    
   
})(jQuery);