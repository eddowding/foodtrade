from itertools import izip_longest
from bson.objectid import ObjectId
from dominate.tags import *
from django.core.urlresolvers import reverse_lazy
from menu.models import Ingredient


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def ingredient_walk(ingredients, parent=None):
    for ingredient in ingredients:
        if isinstance(ingredient, list):
            ingredient_walk(ingredient, parent)
        elif isinstance(ingredient, dict) and len(ingredient['children'][0]):
            Ingredient.objects.filter(dish=ObjectId(ingredient['dishId']), pk=ObjectId(ingredient['ingredientId'])) \
                                                                                .update(set__parent=ObjectId(parent))
            ingredient_walk(ingredient['children'], ingredient['ingredientId'])
        else:
            Ingredient.objects.filter(dish=ObjectId(ingredient['dishId']), pk=ObjectId(ingredient['ingredientId'])) \
                                                                                .update(set__parent=ObjectId(parent))


class IngredientWalk(object):
    def __init__(self, dish_id, dish_tree):
        self.dish_id = dish_id
        self.dish_tree = dish_tree
        self.html = ul(cls='ingredient-tree', data_dish_id=self.dish_id)
        self.parent_li_ul_ref = {}
        self.ingredients_dict = {}

    def _get_ingredients_dict(self):
        dish_id = ObjectId(self.dish_id)
        for i in Ingredient.objects.filter(dish=dish_id):
            self.ingredients_dict[str(i.pk)] = {'name': i.name, 'is_allergen': i.is_allergen, 'is_meat': i.is_meat, 'is_gluten': i.is_gluten}

    def _generate_li(self, ingredient_id):
        dish_id = self.dish_id
        ingredient_name = self.ingredients_dict.get(ingredient_id).get('name')
        ret_li = li(data_dish_id=dish_id, data_ingredient_id=ingredient_id, cls="ingredient-item")
        tmp_span_1 = ret_li.add(span(cls='handle'))
        tmp_span_1.add(i(cls='fa fa-ellipsis-v'))
        tmp_span_1.add(i(cls='fa fa-ellipsis-v'))
        tmp_span_2 = ret_li.add(span(cls='ingredient'))
        tmp_span_2.add(a(ingredient_name, cls='ingredient-item-name', data_pk=ingredient_id, data_name=ingredient_name))
        tmp_div_1 = ret_li.add(div(cls='del'))
        tmp_div_1_1 = tmp_div_1.add(div(cls='tools hidden'))
        tmp_div_1_1_span_1 = tmp_div_1_1.add(span())
        tmp_div_1_1_span_1.add(a('Add sub-ingredient', data_dish_id=dish_id, cls='add-sub-ingredients'))
        tmp_div_1_1.add(a('Delete', data_id=ingredient_id, data_url=reverse_lazy('menu_delete_ingredient'), data_name=ingredient_name, cls='delete-btn'))
        tmp_div_2 = ret_li.add(div(cls='btn-group btn-group-sm pull-right mag-toggle', data_toggle='buttons'))
        tmp_div_2_label_1 = tmp_div_2.add(label('Allergen', cls='btn btn-allergen'))
        tmp_div_2_label_1.add(input(type='checkbox', autocomplete='off'))
        tmp_div_2_label_2 = tmp_div_2.add(label('Meat', cls='btn btn-meat'))
        tmp_div_2_label_2.add(input(type='checkbox', autocomplete='off'))
        tmp_div_2_label_3 = tmp_div_2.add(label('Gluten', cls='btn btn-gluten'))
        tmp_div_2_label_3.add(input(type='checkbox', autocomplete='off'))
        return ret_li

    def _walk(self, ingredients, parent=None, parent_li_ul=None):
        for ingredient in ingredients:
            if isinstance(ingredient, list):
                self._walk(ingredient, parent, parent_li_ul)
            elif isinstance(ingredient, dict) and len(ingredient['children'][0]):
                if parent:
                    parent_li = self.parent_li_ul_ref[parent].add(self._generate_li(ingredient_id=ingredient['ingredientId']))
                else:
                    parent_li = self.html.add(self._generate_li(ingredient_id=ingredient['ingredientId']))

                parent_li_ul = parent_li.add(ul())

                if not ingredient['ingredientId'] in self.parent_li_ul_ref:
                    self.parent_li_ul_ref[ingredient['ingredientId']] = parent_li_ul
                self._walk(ingredient['children'], ingredient['ingredientId'], parent_li_ul)
            else:
                if parent:
                    parent_li = self.parent_li_ul_ref[parent].add(self._generate_li(ingredient_id=ingredient['ingredientId']))
                else:
                    parent_li = self.html.add(self._generate_li(ingredient_id=ingredient['ingredientId']))
                parent_li.add(ul())

    def walk(self):
        self._get_ingredients_dict()
        self._walk(self.dish_tree)
        return self.html
