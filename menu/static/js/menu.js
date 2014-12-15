$(document).ready(function() {
    //menu section
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

    //section section
    $(document).delegate('.add-section', 'click', function(ev) {
        $('#sectionModal input[name="menu"]').val($(this).attr('data-menu-id'));
    });

    $('#sectionModal button.btn').click(function(ev) {
        var data = {
            menu: $('#sectionModal input[name="menu"]').val(),
            name: $('#sectionModal input[name="name"]').val()
        };

        $.ajax({
            url: createSectionUrl,
            data: data,
            type: 'POST',
            dataType: 'JSON',
            success: function(data) {
                $('.menus').html(data.html);
                $('#sectionModal input[name="menu"]').val('');
                $('#sectionModal input[name="name"]').val('');
            }
        });
    });


    //dish section
    var dishes = new Bloodhound({
        remote: {
            url: dishLookupNameUrl + '?q=%QUERY',
            filter: function(dishes) {
                return dishes.objs;
            }

        },
        datumTokenizer: function(dish) {
            return Bloodhound.tokenizers.whitespace(dish.name);
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace
    });

    dishes.initialize();

    $('#dishModal input#name').typeahead(null, {
        displayKey: 'name',
        name: 'dish',
        source: dishes.ttAdapter()
    });

    var dishSelected = false;

    $('#dishModal input#name').on('typeahead:selected', function(ev, dish) {
        $('#dishModal input[name="name"]').val(dish.value);
        dishSelected = true;
    });

    $(document).delegate('.add-dish', 'click', function(ev) {
        $('#dishModal input[name="menu_section"]').val($(this).attr('data-menu-section-id'));
    });

    $('#dishModal button.btn').click(function(ev) {
        var price = parseFloat(0.0)

        if( $('#dishModal input[name="price"]').val() ) {
            price = $('#dishModal input[name="price"]').val();
        }

        var data = {
            menu_section: $('#dishModal input[name="menu_section"]').val(),
            price: price,
            description: $('#dishModal input[name="description"]').val()
        };

        if (dishSelected) {
            data.name = $('#dishModal input[name="name"]').val();
        } else {
            data.name = $('#dishModal input#name').val();
        }

        $.ajax({
            url: createDishUrl,
            data: data,
            type: 'POST',
            dataType: 'JSON',
            success: function(data) {
                $('.menus').html(data.html);
                $('#dishModal input[name="menu_section"]').val('');
                $('#dishModal input[name="price"]').val('');
                $('#dishModal input[name="description"]').val('');
                $('#dishModal input[name="name"]').val('');
                $('#dishModal input#name').val('');
                dishSelected = false;
            }
        });
    });

    //ingredient section

     // Ingredients autocomplete

    var ingredients = new Bloodhound({
        remote: {
            url: ingredientLookupNameUrl + '?q=%QUERY',
            filter: function(ingredients) {
                return ingredients.objs;
            }

        },
        datumTokenizer: function(ingredient) {
            return Bloodhound.tokenizers.whitespace(ingredient.name);
        },
        queryTokenizer: Bloodhound.tokenizers.whitespace
    });

    ingredients.initialize();

    $('#ingredientsModal input#name').typeahead(null, {
        displayKey: 'name',
        name: 'ingredients',
        source: ingredients.ttAdapter(),
    });


    $('#ingredientsModal input#name').on('typeahead:selected', function(ev, ingredient) {
        $('#ingredientsModal input[name="name"]').val(ingredient.name);
        $('#ingredientsModal button.btn').trigger('click');
    });


    $(document).delegate('.add-ingredients', 'click', function(ev) {
        $('#ingredientsModal input[name="dish"]').val($(this).attr('data-dish-id'));
    });

    $('#ingredientsModal button.btn').click(function(ev) {
        var data = {
            dish: $('#ingredientsModal input[name="dish"]').val(),
            name: $('#ingredientsModal input[name="name"]').val(),
            parent: null,
            order: 1
        };

        $.ajax({
            url: createIngredientUrl,
            data: data,
            type: 'POST',
            dataType: 'JSON',
            success: function(data) {
                $('.menus').html(data.html);
                sortableFn();
                $('#ingredientsModal input[name="name"]').val('');
                $('#ingredientsModal input[name="dish"]').val('');
            }
        });
    });



  /* Menu tree */


    var sortableFn = function() {
        $('.ingredient-tree').sortable({
            onDrop: function($item, container, _super, event) {
                var data = {
                    dish: $item.attr('data-dish-id'),
                    name: $item.attr('data-ingredient-name'),
                    parent: null,
                    order: $item.prevAll().length + 1
                };
                if ($item.parents('li').attr('data-ingredient-name') !== undefined) {
                    data.parent = $item.parents('li').attr('data-ingredient-name');
                }
                $.ajax({
                    url: updateIngredientUrl,
                    data: data,
                    type: 'POST',
                    dataType: 'JSON',
                    success: function(data) {}
                });

                _super($item, container);
            },
            isValidTarget: function($item, container) {
                if ($item.is('.child-li')) {
                    return false;
                } else {
                    return true;
                }
            }
        });
    };

    sortableFn();
});