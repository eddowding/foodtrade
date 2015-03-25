//jQuery.ajaxSetup({async:false});

$(document).ready(function() {
  analytics.identify(userId, {
    email: userEmail
  });
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

  $('#menuModal').keypress(function(e) {
    var key = e.which;
    if (key == 13) // the enter key code
    {
      $('#menuModal button.btn').click();
      return false;
    }
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

  // edit menu starts here
  editMenuId = null;
  editMenuBusinessId = null;
  editMenuBusinessName = null;

  $('#editMenuModal input#establishment').typeahead(null, {
    displayKey: 'name',
    name: 'establishment',
    source: establishments.ttAdapter()
  });

  $('#editMenuModal input#establishment').on('typeahead:selected', function(ev, establishment) {
    $('#editMenuModal input[name="establishment"]').val(establishment.value);
    establishmentSelected = true;
  });

  $(document).delegate('.menu-edit-btn', 'click', function(ev) {
    $('#editMenuModal input[name="name"]').val($(this).attr('data-menu-name'));
    $('#editMenuModal input[id="establishment"]').val($(this).attr('data-business'));
    editMenuBusinessName = $(this).attr('data-business');
    editMenuId = $(this).attr('data-id');
    editMenuBusinessId = $(this).attr('data-business-id');
    $('#editMenuModal').modal('show');
  });

  $('#editMenuModal').keypress(function(e) {
    var key = e.which;
    if (key == 13) // the enter key code
    {
      $('#editMenuModal button.btn').click();
      return false;
    }
  });

  $('#editMenuModal button.btn').click(function(ev) {
    var data = {
      'name': $('#editMenuModal input[name="name"]').val(),
      'id': editMenuId
    };
    if (establishmentSelected) {
      data.establishment = $('#editMenuModal input[name="establishment"]').val();
    } else {
      if ($('#editMenuModal input[id="establishment"]').val() == editMenuBusinessName) {
        data.establishment = editMenuBusinessId;
      } else {
        data.establishment = $('#editMenuModal input#establishment').val();
      }
      //data.establishment = $('#editMenuModal input#establishment').val();
    }

    $.ajax({
      url: '/edit/menu/' + '?_tmp=' + (new Date).getTime(),
      data: data,
      type: 'POST',
      dataType: 'JSON',
      success: function(data) {
        $('.menus').html(data.html);
        $('#editMenuModal input[name="establishment"]').val('');
        $('#editMenuModal input#establishment').val('');
        $('#editMenuModal input[name="name"]').val('');
        establishmentSelected = false;
        editMenuId = null;
        editMenuBusinessId = null;
        editMenuBusinessName = null;
      }
    });
  });

  // edit menu ends here

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


  /* Menu tree */


  var sortableFn = function() {
    $('.ingredient-item').removeAttr('style');
    $('.ingredient-item').removeClass('dragged');
    $('.ingredient-tree').sortable({
      itemSelector: 'li.ingredient-item',
      handle: '.handle',
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
          success: function(data) {
            console.log(data);
          }
        });

        _super($item, container);
      }
    });
  };

  //editable
  var editableFn = function(existing) {
    var existing = existing || false;
    if (existing) {
      var url = updateIngredientNameUrl;
    } else {
      var url = createIngredientUrl;
    }
    $('.ingredient-item-name').editable({
      type: 'text',
      url: url + '?_tmp=' + (new Date).getTime(),
      inputclass: 'ingredient-editable',
      emptytext: '',
      placeholder: 'Add ingredient here',
      params: function(params) {
        params.dish = $(this).attr('data-dish-id');
        params.name = params.value;
        params.parent = $(this).attr('data-parent-id');
        params.order = 1;
        params.pk = $(this).attr('data-pk');
        params.autoClass = $(this).attr('data-auto-class');
        params.autoId = $(this).attr('data-auto-id');
        return params;
      },
      success: function(response, newValue) {
        if (response.status === false) {
          return 'Cannot save empty string';
        }
        if (response.obj.is_allergen) {
          $(this).parents('li:first').find('div.mag-toggle').find('.btn-allergen').addClass('active');
          $(this).parents('li:first').find('div.mag-toggle').find('.btn-allergen').find('input').attr('checked', 'checked');
          $(this).parents('div.menuitem').find('div.menutitle').find('div.pull-right').find('span.allergen').addClass('active');
        }
        if (response.obj.is_meat) {
          $(this).parents('li:first').find('div.mag-toggle').find('.btn-meat').addClass('active');
          $(this).parents('li:first').find('div.mag-toggle').find('.btn-meat').find('input').attr('checked', 'checked');
          $(this).parents('div.menuitem').find('div.menutitle').find('div.pull-right').find('span.meat').addClass('active');
        }
        if (response.obj.is_gluten) {
          $(this).parents('li:first').find('div.mag-toggle').find('.btn-gluten').addClass('active');
          $(this).parents('li:first').find('div.mag-toggle').find('.btn-gluten').find('input').attr('checked', 'checked');
          $(this).parents('div.menuitem').find('div.menutitle').find('div.pull-right').find('span.gluten').addClass('active');
        }

        //final dish update
        if (response.dish && response.dish.is_allergen) {
          $(this).parents('div.menuitem').find('div.menutitle').find('div.pull-right').find('span.allergen').addClass('active');
        }
        if (response.dish && response.dish.is_meat) {
          $(this).parents('div.menuitem').find('div.menutitle').find('div.pull-right').find('span.meat').addClass('active');
        }
        if (response.dish && response.dish.is_gluten) {
          $(this).parents('div.menuitem').find('div.menutitle').find('div.pull-right').find('span.gluten').addClass('active');
        }

        if (response.obj.parent !== undefined) {
          var parentId = response.obj.parent.$oid;

          (function loop() {
            if (parentId !== null) {
              if (response.obj.is_allergen) {
                $('.ingredient-item-name[data-pk="' + parentId + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-allergen').addClass('active');
                $('.ingredient-item-name[data-pk="' + parentId + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-allergen').find('input').attr('checked', 'checked');
              }
              if (response.obj.is_meat) {
                $('.ingredient-item-name[data-pk="' + parentId + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-meat').addClass('active');
                $('.ingredient-item-name[data-pk="' + parentId + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-meat').find('input').attr('checked', 'checked');
              }
              if (response.obj.is_gluten) {
                $('.ingredient-item-name[data-pk="' + parentId + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-gluten').addClass('active');
                $('.ingredient-item-name[data-pk="' + parentId + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-gluten').find('input').attr('checked', 'checked');
              }
              $.ajax({
                url: updateIngredientUrl,
                data: {
                  id: $('.ingredient-item-name[data-pk="' + parentId + '"]').parents('li:first').attr('data-ingredient-id'),
                  is_allergen: response.obj.is_allergen,
                  is_meat: response.obj.is_meat,
                  is_gluten: response.obj.is_gluten
                },
                type: 'POST',
                dataType: 'JSON'
              });
              parentId = $('.ingredient-item-name[data-pk="' + parentId + '"]').attr('data-parent-id');
              if (parentId === undefined) {
                parentId = null;
              }
              loop();
            }
          }());

          $('a.add-sub-ingredients[data-dish-id="' + $(this).attr('data-pk') + '"]').attr('data-parent-id', response.obj.parent.$oid);
        }

        $(this).editable('option', 'name', newValue);
        $(this).editable('option', 'url', updateIngredientNameUrl);

        $(this).parents('.ingredient-item:first').find('.delete-btn').attr('data-name', newValue);
        $(this).parents('.ingredient-item:first').find('.delete-btn').attr('data-id', response.obj._id.$oid);
        $(this).parents('.ingredient-item:first').attr('data-ingredient-id', response.obj._id.$oid);
        if (response.html) {
          $(this).parents('.ingredient-item:first').find('ul:first').replaceWith(response.html);
          sortableFn();
          editableFn(true);
        }
        $(this).attr('data-pk', response.obj._id.$oid);
        $(this).attr('data-name', newValue);

        var htmlSaveFn = function() {
          var data = {
            pk: $('.ingredient-item[data-ingredient-id=' + response.obj._id.$oid + ']').attr('data-dish-id'),
            html: $('.ingredient-item[data-ingredient-id=' + response.obj._id.$oid + ']').parents('.ingredient-tree').parents('div.tree').html(),
            serialized: JSON.stringify($('.ingredient-item[data-ingredient-id=' + response.obj._id.$oid + ']').parents('.ingredient-tree').sortable("serialize").get()),
            is_allergen: response.obj.is_allergen,
            is_meat: response.obj.is_meat,
            is_gluten: response.obj.is_gluten
          };

          $.ajax({
            url: updateDishUrl + '?_tmp=' + (new Date).getTime(),
            data: data,
            type: 'POST',
            dataType: 'JSON',
            success: function(data) {
              if ($('.ingredient-item[data-ingredient-id=' + response.obj._id.$oid + ']').parents('li.ingredient-item').find('a.add-sub-ingredients:first').length) {
                $('.ingredient-item[data-ingredient-id=' + response.obj._id.$oid + ']').parents('li.ingredient-item').find('a.add-sub-ingredients:first').trigger('click');
              } else {
                $('.ingredient-item[data-ingredient-id=' + response.obj._id.$oid + ']').parents('.menuitem:first').find('.add-ingredients:first').trigger('click');
              }
            }
          });
        };
        setTimeout(htmlSaveFn, 1000);
      }
    });

    $('.ingredient-item-name').on('hidden', function(e, reason) {
      if ($(this).text().trim() === '') {
        $(this).parents('li.ingredient-item:first').remove();
      }
    });

    $('.ingredient-item-name:contains("Type Ingredient Here")').editable('toggle');

    $('.ingredient-editable').typeahead(null, {
      displayKey: 'name',
      name: 'ingredients',
      source: ingredients.ttAdapter()
    });

    var handleIngredientSelectFn = function(ingredient) {
      $(this).parents('span.ingredient:first').find('a.ingredient-item-name:first').attr('data-auto-class', ingredient.class).attr('data-auto-id', ingredient.id);
    };

    $('.ingredient-editable').on('typeahead:selected', function(ev, ingredient) {
      $(this).parents('span.ingredient:first').find('a.ingredient-item-name:first').attr('data-auto-class', ingredient.class).attr('data-auto-id', ingredient.id);
    });

    $('.ingredient-editable:contains("")').select();
  };

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

  /* $('#editDishModal input#name').typeahead(null, {
displayKey: 'name',
name: 'dish',
source: dishes.ttAdapter()
});*/

  var dishSelected = false;

  $('#dishModal input#name').on('typeahead:selected', function(ev, dish) {
    $('#dishModal input[name="name"]').val(dish.value);
    dishSelected = true;
  });

  $(document).delegate('.add-dish', 'click', function(ev) {
    $('#dishModal input[name="menu_section"]').val($(this).attr('data-menu-section-id'));
  });

  $('#dishModal').keypress(function(e) {
    var key = e.which;
    if (key == 13) // the enter key code
    {
      $('#dishModal button.btn').click();
      return false;
    }
  });

  $('#dishModal button.btn').click(function(ev) {
    var price = parseFloat(0.0);

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
        sortableFn();
        editableFn();
        $('#dishModal input[name="menu_section"]').val('');
        $('#dishModal input[name="price"]').val('');
        $('#dishModal input[name="description"]').val('');
        $('#dishModal input[name="name"]').val('');
        $('#dishModal input#name').val('');
        if (data.dish_id) {
          console.log(data.dish_id);
          var saveHtmlFn = function () {
            var update_data = {
              pk: data.dish_id,
              html: $(".tree[data-dish-id='" + data.dish_id + "'] > ul").parents('div.tree').html(),
              serialized: JSON.stringify($('.ingredient-tree[data-dish-id="' + data.dish_id + '"]').sortable("serialize").get())
            };

            $.ajax({
              url: updateDishUrl + '?_tmp=' + (new Date).getTime(),
              data: update_data,
              type: 'POST',
              dataType: 'JSON',
              success: function(result) {
                //console.log(result);
              }
            });
          };
          setTimeout(saveHtmlFn, 1000);
        }
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
      return Bloodhound.tokenizers.whitespace(ingredient.label);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace
  });

  ingredients.initialize();

  $('.ingredient-editable').on('typeahead:selected', function(ev, ingredient) {
    $(this).parents('span.ingredient:first').find('a.ingredient-item-name:first').attr('data-auto-class', ingredient.class).attr('data-auto-id', ingredient.id);
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

    sortableFn();
    editableFn();
    ev.stopPropagation();
    placeholder_li.find('.ingredient-item-name:last').editable('toggle');
    $('.ingredient-editable:last').focus().trigger('click');

    $('.ingredient-editable').typeahead(null, {
      displayKey: 'label',
      name: 'ingredients',
      source: ingredients.ttAdapter()
    });
    $('.ingredient-editable').on('typeahead:selected', function(ev, ingredient) {
      $(this).parents('span.ingredient:first').find('a.ingredient-item-name:first').attr('data-auto-class', ingredient.class).attr('data-auto-id', ingredient.id);
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
    ev.stopPropagation();
    placeholder_li.find('.ingredient-item-name:last').editable('toggle');
    $('.ingredient-editable:last').focus().trigger('click');

    $('.ingredient-editable').typeahead(null, {
      displayKey: 'name',
      name: 'ingredients',
      source: ingredients.ttAdapter()
    });
    $('.ingredient-editable').on('typeahead:selected', function(ev, ingredient) {
      $(this).parents('span.ingredient:first').find('a.ingredient-item-name:first').attr('data-auto-class', ingredient.class).attr('data-auto-id', ingredient.id);
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

  // edit section starts here
  editId = null;
  editName = null;
  editUrl = null;

  $(document).delegate('.section-edit-btn', 'click', function(ev) {
    editId = $(this).attr('data-id');
    editName = $(this).attr('data-name');
    editUrl = $(this).attr('data-url');
    $('#editSectionModal input[name="menu"]').val($(this).attr('data-section-menu-id'));
    $('#editSectionModal input[name="name"]').val(editName);
    $('#editSectionModal').modal('show');
    //$('#sectionModal button.btn').click();
    //deleteElement = $(this).parents('.ingredient-item:first');
  });

  $('#editSectionModal').keypress(function(e) {
    var key = e.which;
    if (key == 13) // the enter key code
    {
      $('#editSectionModal button.btn').click();
      return false;
    }
  });

  $('#editSectionModal button.btn').click(function(ev) {
    var data = {
      menu: $('#editSectionModal input[name="menu"]').val(),
      name: $('#editSectionModal input[name="name"]').val(),
      id: editId
    };

    $.ajax({
      url: '/edit/menu/section/' + '?_tmp=' + (new Date).getTime(),
      data: data,
      type: 'POST',
      dataType: 'JSON',
      success: function(data) {
        $('.menus').html(data.html);
        $('#editSectionModal input[name="menu"]').val('');
        $('#editSectionModal input[name="name"]').val('');
        editId = null;
        editName = null;
        editUrl = null;
      }
    });
  });

  // edit section ends here

  //edit dish starts here

  $(document).delegate('.edit-btn', 'click', function(ev) {
    editUrl = $(this).attr('data-url');
    editId = $(this).attr('data-id');
    editName = $(this).attr('data-name');
    $('#editDishModal input[name="menu_section"]').val($(this).attr('data-menu-section-id'));
    $('#editDishModal input[name="name"]').val($(this).attr('data-name'));
    if ($(this).attr('data-price'))
      $('#editDishModal input[name="price"]').val($(this).attr('data-price'));
    else
      $('#editDishModal input[name="price"]').val('');
    if ($(this).attr('data-description'))
      $('#editDishModal input[name="description"]').val($(this).attr('data-description'));
    else
      $('#editDishModal input[name="description"]').val('');
    dishSelected = true;
    //$('#confirmationModal').modal('show');
    //deleteElement = $(this).parents('.ingredient-item:first');
  });

  $('#editDishModal').keypress(function(e) {
    var key = e.which;
    if (key == 13) // the enter key code
    {
      $('#editDishModal button.btn').click();
      return false;
    }
  });

  $('#editDishModal button.btn').click(function(ev) {
    var price = parseFloat(0.0);

    if ($('#editDishModal input[name="price"]').val()) {
      price = $('#editDishModal input[name="price"]').val();
    }

    var data = {
      pk: editId,
      menu_section: $('#editDishModal input[name="menu_section"]').val(),
      price: price,
      description: $('#editDishModal input[name="description"]').val()
    };

    if (dishSelected) {
      data.name = $('#editDishModal input[name="name"]').val();
    } else {
      data.name = $('#editDishModal input#name').val();
    }

    $.ajax({
      url: updateDishUrl + '?_tmp=' + (new Date).getTime(),
      data: data,
      type: 'POST',
      dataType: 'JSON',
      success: function(data) {
        $('.menus').html(data.html);
        $('#editDishModal input[name="menu_section"]').val('');
        $('#editDishModal input[name="price"]').val('');
        $('#editDishModal input[name="description"]').val('');
        $('#editDishModal input[name="name"]').val('');
        $('#editDishModal input#name').val('');
        dishSelected = false;
      }
    });
  });
  // edit dish ends here



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
          if (deleteIngredientUrl == deleteUrl) {
            if (data.dish.is_allergen) {
              $('div.menuitem[data-pk="' + data.dish.id + '"]').find('div.menutitle').find('div.pull-right').find('span.allergen').addClass('active');
            } else {
              $('div.menuitem[data-pk="' + data.dish.id + '"]').find('div.menutitle').find('div.pull-right').find('span.allergen').removeClass('active');
            }
            if (data.dish.is_meat) {
              $('div.menuitem[data-pk="' + data.dish.id + '"]').find('div.menutitle').find('div.pull-right').find('span.meat').addClass('active');
            } else {
              $('div.menuitem[data-pk="' + data.dish.id + '"]').find('div.menutitle').find('div.pull-right').find('span.meat').removeClass('active');
            }
            if (data.dish.is_gluten) {
              $('div.menuitem[data-pk="' + data.dish.id + '"]').find('div.menutitle').find('div.pull-right').find('span.gluten').addClass('active');
            } else {
              $('div.menuitem[data-pk="' + data.dish.id + '"]').find('div.menutitle').find('div.pull-right').find('span.gluten').removeClass('active');
            }
            data.objs.forEach(function(value, index) {
              if (value.is_allergen) {
                $('.ingredient-item-name[data-pk="' + value.id + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-allergen').addClass('active');
                $('.ingredient-item-name[data-pk="' + value.id + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-allergen').find('input').attr('checked', 'checked');
              } else {
                $('.ingredient-item-name[data-pk="' + value.id + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-allergen').removeClass('active');
                $('.ingredient-item-name[data-pk="' + value.id + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-allergen').find('input').removeAttr('checked');
              }

              if (value.is_meat) {
                $('.ingredient-item-name[data-pk="' + value.id + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-meat').addClass('active');
                $('.ingredient-item-name[data-pk="' + value.id + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-meat').find('input').attr('checked', 'checked');
              } else {
                $('.ingredient-item-name[data-pk="' + value.id + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-meat').removeClass('active');
                $('.ingredient-item-name[data-pk="' + value.id + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-meat').find('input').removeAttr('checked');
              }

              if (value.is_gluten) {
                $('.ingredient-item-name[data-pk="' + value.id + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-gluten').addClass('active');
                $('.ingredient-item-name[data-pk="' + value.id + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-gluten').find('input').attr('checked', 'checked');
              } else {
                $('.ingredient-item-name[data-pk="' + value.id + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-gluten').removeClass('active');
                $('.ingredient-item-name[data-pk="' + value.id + '"]').parents('li:first').find('div.mag-toggle:first').find('.btn-gluten').find('input').removeAttr('checked');
              }
            });
          }
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

  // $(document).delegate('.ingredient-item', 'click', function(ev) {
  //     $(this).find('.ingredient-item-name:first').editable('toggle');
  // });


  $(document).delegate('.ingredient-editable', 'keydown', function(ev) {
    if (ev.ctrlKey && ev.keyCode == 13) {
      $(this).parents('div.menuitem').find('a.add-ingredients').trigger('click');
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
    $('.ingredient-editable').on('typeahead:selected', function(ev, ingredient) {
      $(this).parents('span.ingredient:first').find('a.ingredient-item-name:first').attr('data-auto-class', ingredient.class).attr('data-auto-id', ingredient.id);
    });
  });



  $.fn.editable.defaults.mode = 'inline';
  editableFn(true);

  //toggle
  $(document).delegate('div.mag-toggle input[type="checkbox"]', 'change', function(ev) {
    var oid = $(this).parents('.ingredient-item:first').attr('data-ingredient-id');
    var ingredient = {
      name: $(this).parents('.ingredient-item:first').find('.ingredient-item-name:first').attr('data-name')
    };
    if ($(this).parent().hasClass('btn-allergen')) {
      ingredient.is_allergen = $(this).is(':checked');
    }

    if ($(this).parent().hasClass('btn-meat')) {
      ingredient.is_meat = $(this).is(':checked');
    }

    if ($(this).parent().hasClass('btn-gluten')) {
      ingredient.is_gluten = $(this).is(':checked');
    }

    var data = {
      pk: $(this).parents('.ingredient-item:first').attr('data-dish-id'),
      ingredientId: $(this).parents('.ingredient-item:first').attr('data-ingredient-id'),
      serialized: JSON.stringify($(this).parents('.ingredient-item:first').parents('.ingredient-tree').sortable("serialize").get()),
      ingredient: JSON.stringify(ingredient)
    };
    var htmlSaveFn = function() {
      data.html = $('.ingredient-item[data-ingredient-id=' + oid + ']').parents('.ingredient-tree').parents('div.tree').html();

      $.ajax({
        url: saveModerationIngredientUrl,
        data: data,
        type: 'POST',
        dataType: 'JSON',
        success: function(data) {
          //console.info('Ingredient Toggle', data);
          // $('.menus').html(data.html);
          sortableFn();
          editableFn();

        }
      });
    };

    setTimeout(htmlSaveFn, 1000);
  });

});
//analytics
var shareAnalyticsFn = function(url) {
  analytics.track('Social Share', {
    url: url
  });
};
