$(document).ready(function() {
  //menu section
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
      url: createMenuUrl + '?_tmp=' + (new Date).getTime(),
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
      url: createSectionUrl + '?_tmp=' + (new Date).getTime(),
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
      url: dishLookupNameUrl + '?q=%QUERY' + '&_tmp=' + (new Date).getTime(),
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

    if ($('#dishModal input[name="price"]').val()) {
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
      url: createDishUrl + '?_tmp=' + (new Date).getTime(),
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
      url: ingredientLookupNameUrl + '?q=%QUERY' + '&_tmp=' + (new Date).getTime(),
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
    var dish = $(this).data('dishId');
    var tree_div = $(this).parents('div.menuitem').find('div.tree');
    if (!$(this).parents('div.menuitem').find('div.tree').find('ul.ingredient-tree').length) {
      tree_div.append('<ul class="ingredient-tree" data-dish-id="' + dish + '"></ul>');
    }
    var placeholder_li = $('.ingredient-item-new').clone();

    placeholder_li.removeClass('hidden ingredient-item-new');
    placeholder_li.attr('data-dish-id', dish);
    placeholder_li.find('.add-sub-ingredients').attr('data-dish-id', dish);
    placeholder_li.find('.ingredient-item-name').attr('data-dish-id', dish);
    $('.ingredient-tree[data-dish-id="' + dish + '"]').append(placeholder_li);

    editableFn();
    placeholder_li.find('.ingredient-item-name:last').editable('toggle');

    $('.ingredient-editable').typeahead(null, {
      displayKey: 'name',
      name: 'ingredients',
      source: ingredients.ttAdapter()
    });
  });

  $(document).delegate('.add-sub-ingredients', 'click', function(ev) {
    var dish = $(this).data('dishId');
    var target_ul = $(this).parents('li.ingredient-item:first').find('ul').first();
    var placeholder_li = $('.ingredient-item-new').clone();
    var parent = $(this).parents('li.ingredient-item:first').find('.ingredient-item-name:first').attr('data-pk');
    placeholder_li.removeClass('hidden ingredient-item-new');
    placeholder_li.attr('data-dish-id', dish);
    placeholder_li.find('.add-sub-ingredients').attr('data-dish-id', dish);
    placeholder_li.find('.ingredient-item-name').attr('data-dish-id', dish);
    placeholder_li.find('.ingredient-item-name').attr('data-parent-id', parent);
    target_ul.append(placeholder_li);

    editableFn();
    placeholder_li.find('.ingredient-item-name:last').editable('toggle');

    $('.ingredient-editable').typeahead(null, {
      displayKey: 'name',
      name: 'ingredients',
      source: ingredients.ttAdapter()
    });
  });

  $('#ingredientsModal button.btn').click(function(ev) {
    var data = {
      dish: $('#ingredientsModal input[name="dish"]').val(),
      name: $('#ingredientsModal input[name="name"]').val(),
      parent: null,
      order: 1
    };

    $.ajax({
      url: createIngredientUrl + '?_tmp=' + (new Date).getTime(),
      data: data,
      type: 'POST',
      dataType: 'JSON',
      success: function(data) {
        $('.menus').html(data.html);
        sortableFn();
        editableFn();
        $('#ingredientsModal input[name="name"]').val('');
        $('#ingredientsModal input[name="dish"]').val('');
      }
    });
  });



  /* Menu tree */


  var sortableFn = function() {
    $('.ingredient-item').removeAttr('style');
    $('.ingredient-item').removeClass('dragged');
    $('.ingredient-tree').sortable({
      onDrop: function($item, container, _super, event) {
        var data = {
          pk: $item.parents('.ingredient-tree').data('dishId'),
          html: $item.parents('.ingredient-tree').parents('div.tree').html(),
          serialized: JSON.stringify($item.parents('.ingredient-tree').sortable("serialize").get())
        };

        $.ajax({
          url: updateDishUrl + '?_tmp=' + (new Date).getTime(),
          data: data,
          type: 'POST',
          dataType: 'JSON',
          success: function(data) {}
        });

        _super($item, container);
      }
    });
  };

  sortableFn();

  // delete functionality

  var deleteUrl = null;
  var deleteId = null;
  var deleteName = null;

  var deleteElement = null;

  $(document).delegate('.delete-btn', 'click', function(ev) {
    deleteUrl = $(this).attr('data-url');
    deleteId = $(this).attr('data-id');
    deleteName = $(this).attr('data-name');
    $('#confirmationModal').modal('show');
    deleteElement = $(this).parents('.ingredient-item:first');
  });

  $('.delete-confirm-btn').click(function(ev) {
    var data = {
      id: deleteId,
      name: deleteName
    };

    var tree = deleteElement.parents('.ingredient-tree');

    deleteElement.remove();

    var dataDish = {
      pk: tree.attr('data-dish-id'),
      html: tree.parents('div.tree').html(),
      serialized: JSON.stringify(tree.sortable("serialize").get())
    };

    $.ajax({
      url: updateDishUrl + '?_tmp=' + (new Date).getTime(),
      data: dataDish,
      type: 'POST',
      dataType: 'JSON',
      success: function(data) {}
    });

    if (deleteId) {
      $.ajax({
        url: deleteUrl + '?_tmp=' + (new Date).getTime(),
        data: data,
        type: 'POST',
        dataType: 'JSON',
        success: function(data) {
          $('.menus').html(data.html);
          sortableFn();
          editableFn();
        }
      });
    }
  });

  $(document).delegate('.ingredient-item', 'mouseover', function(ev) {
    if ($(this).attr('data-ingredient-id')) {
      $(this).children('.del').children('.tools').removeClass('hidden');
    }
  });

  $(document).delegate('.ingredient-item', 'mouseout', function(ev) {
    if ($(this).attr('data-ingredient-id')) {
      $(this).children('.del').children('.tools').addClass('hidden');
    }
  });


  //editable
  var editableFn = function() {
    $('.ingredient-item-name').editable({
      type: 'text',
      url: createIngredientUrl + '?_tmp=' + (new Date).getTime(),
      inputclass: 'ingredient-editable',
      params: function(params) {
        params.dish = $(this).attr('data-dish-id');
        params.name = params.value;
        params.parent = $(this).attr('data-parent-id');
        params.order = 1;
        return params;
      },
      success: function(response, newValue) {
        if (response.obj.is_allergen) {
          $(this).parents('li').find('div.pull-right').find('span.allergen').addClass('active');
          $(this).parents('div.menuitem').find('div.menutitle').find('div.pull-right').find('span.allergen').addClass('active');
        }
        if (response.obj.is_meat) {
          $(this).parents('li').find('div.pull-right').find('span.meat').addClass('active');
          $(this).parents('div.menuitem').find('div.menutitle').find('div.pull-right').find('span.meat').addClass('active');
        }
        if (response.obj.is_gluten) {
          $(this).parents('li').find('div.pull-right').find('span.gluten').addClass('active');
          $(this).parents('div.menuitem').find('div.menutitle').find('div.pull-right').find('span.gluten').addClass('active');
        }
        if (response.obj.parent !== undefined) {
          $('a.add-sub-ingredients[data-dish-id="' + $(this).attr('data-pk') + '"]').attr('data-parent-id', response.obj.parent.$oid);
        }
        $(this).editable('option', 'name', newValue);
        $(this).editable('option', 'url', updateIngredientNameUrl);

        $(this).parents('.ingredient-item:first').find('.delete-btn').attr('data-name', newValue);
        $(this).parents('.ingredient-item:first').find('.delete-btn').attr('data-id', response.obj._id.$oid);
        $(this).parents('.ingredient-item:first').attr('data-ingredient-id', response.obj._id.$oid);
        $(this).attr('data-pk', response.obj._id.$oid);
        $(this).attr('data-name', newValue);

        var htmlSaveFn = function() {
          var data = {
            pk: $('.ingredient-item[data-ingredient-id=' + response.obj._id.$oid + ']').attr('data-dish-id'),
            html: $('.ingredient-item[data-ingredient-id=' + response.obj._id.$oid + ']').parents('.ingredient-tree').parents('div.tree').html(),
            serialized: JSON.stringify($('.ingredient-item[data-ingredient-id=' + response.obj._id.$oid + ']').parents('.ingredient-tree').sortable("serialize").get())
          };

          $.ajax({
            url: updateDishUrl + '?_tmp=' + (new Date).getTime(),
            data: data,
            type: 'POST',
            dataType: 'JSON',
            success: function(data) {}
          });
        };
        setTimeout(htmlSaveFn, 1000);
      }
    });

    $('.ingredient-item-name:contains("Type Ingredient Here")').editable('toggle');

    $('.ingredient-editable').typeahead(null, {
      displayKey: 'name',
      name: 'ingredients',
      source: ingredients.ttAdapter()
    });

    $('.ingredient-editable:contains("")').select();
  };

  $(document).delegate('.ingredient-editable', 'keydown', function(ev) {
    if (ev.ctrlKey && ev.keyCode == 13) {
      var data = {
        dish: $(this).parents('span.ingredient').find('a').attr('data-pk'),
        name: 'Type Ingredient Here',
        parent: null,
        order: 1
      };

      $.ajax({
        url: createIngredientUrl + '?_tmp=' + (new Date).getTime(),
        data: data,
        type: 'POST',
        dataType: 'JSON',
        success: function(data) {
          $('.menus').html(data.html);
          sortableFn();
          editableFn();
        }
      });
    }
  });

  //  $('.ingredient-item-name').on('shown', function(e, editable) {
  //    $('.ingredient-editable').typeahead(null, {
  //      displayKey: 'name',
  //      name: 'ingredients',
  //      source: ingredients.ttAdapter()
  //    });
  //  });

  $(document).delegate('.ingredient-item-name', 'click', function(e, editable) {
    $('.ingredient-editable').typeahead(null, {
      displayKey: 'name',
      name: 'ingredients',
      source: ingredients.ttAdapter()
    });
  });



  $.fn.editable.defaults.mode = 'inline';
  editableFn();
});
