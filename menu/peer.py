from itertools import izip_longest
from datetime import datetime
from bson.objectid import ObjectId
from dominate.tags import *
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from mailchimp import Mailchimp, ListAlreadySubscribedError
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
            if parent:
                Ingredient.objects.filter(dish=ObjectId(ingredient['dishId']), pk=ObjectId(ingredient['ingredientId'])) \
                                                                                    .update(set__parent=ObjectId(parent))
            else:
                Ingredient.objects.filter(dish=ObjectId(ingredient['dishId']), pk=ObjectId(ingredient['ingredientId'])) \
                                                                                    .update(set__parent=None)

            ingredient_walk(ingredient['children'], ingredient['ingredientId'])
        else:
            if parent:
                Ingredient.objects.filter(dish=ObjectId(ingredient['dishId']), pk=ObjectId(ingredient['ingredientId'])) \
                                                                                    .update(set__parent=ObjectId(parent))
            else:
                Ingredient.objects.filter(dish=ObjectId(ingredient['dishId']), pk=ObjectId(ingredient['ingredientId'])) \
                                                                                    .update(set__parent=None)


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
            self.ingredients_dict[str(i.pk)] = {'name': i.name, 'is_allergen': i.is_allergen, 'is_meat': i.is_meat,
                                                'is_gluten': i.is_gluten, 'parent': str(i.parent.id) if i.parent else None}

    def _generate_li(self, ingredient_id):
        dish_id = self.dish_id
        ingredient_dict = self.ingredients_dict.get(ingredient_id)
        ingredient_name = ingredient_dict.get('name')
        ret_li = li(data_dish_id=dish_id, data_ingredient_id=ingredient_id, cls="ingredient-item")
        tmp_span_1 = ret_li.add(span(cls='handle'))
        tmp_span_1.add(i(cls='fa fa-navicon'))
        tmp_span_2 = ret_li.add(span(cls='ingredient'))
        tmp_span_2.add(a(ingredient_name, cls='ingredient-item-name', data_pk=ingredient_id, data_name=ingredient_name,
                        data_parent_id=ingredient_dict.get('parent')))
        tmp_div_1_1 = ret_li.add(span(cls='tools'))
        tmp_div_1_1_a_1 = tmp_div_1_1.add(a(data_id=ingredient_id, data_url=reverse_lazy('menu_delete_ingredient'),
                    data_name=ingredient_name, cls='delete-btn', data_toggle='tooltip', title='Remove this ingredient'))
        tmp_div_1_1_a_1.add(i(cls='fa fa-trash-o'))
        tmp_div_1_1_a_2 = tmp_div_1_1.add(a(title='Add nutrition info', data_toggle='modal', data_target='#nutrition', cls='nutrition'))
        tmp_div_1_1_a_2.add(i(cls='fa fa-heart'))
        tmp_div_1_1_a_3 = tmp_div_1_1.add(a(data_dish_id=dish_id, cls='add-sub-ingredients', title='Add sub-ingredient'))
        tmp_div_1_1_a_3.add(i(cls='fa fa-plus-circle'))
        tmp_div_2 = ret_li.add(div(cls='mag btn-group btn-group-sm pull-right mag-toggle', data_toggle='buttons'))
        if ingredient_dict.get('is_allergen'):
            tmp_div_2_label_1 = tmp_div_2.add(label('Allergen', cls='btn btn-allergen active'))
            tmp_div_2_label_1.add(input(type='checkbox', autocomplete='off', checked='checked'))
        else:
            tmp_div_2_label_1 = tmp_div_2.add(label('Allergen', cls='btn btn-allergen'))
            tmp_div_2_label_1.add(input(type='checkbox', autocomplete='off'))

        if ingredient_dict.get('is_meat'):
            tmp_div_2_label_2 = tmp_div_2.add(label('Meat', cls='btn btn-meat active'))
            tmp_div_2_label_2.add(input(type='checkbox', autocomplete='off', checked='checked'))
        else:
            tmp_div_2_label_2 = tmp_div_2.add(label('Meat', cls='btn btn-meat'))
            tmp_div_2_label_2.add(input(type='checkbox', autocomplete='off'))

        if ingredient_dict.get('is_gluten'):
            tmp_div_2_label_3 = tmp_div_2.add(label('Gluten', cls='btn btn-gluten active'))
            tmp_div_2_label_3.add(input(type='checkbox', autocomplete='off', checked='checked'))
        else:
            tmp_div_2_label_3 = tmp_div_2.add(label('Gluten', cls='btn btn-gluten'))
            tmp_div_2_label_3.add(input(type='checkbox', autocomplete='off'))
        return ret_li

    def _walk(self, ingredients, parent=None, parent_li_ul=None):
        for ingredient in ingredients:
            if isinstance(ingredient, list):
                self._walk(ingredient, parent, parent_li_ul)
            elif isinstance(ingredient, dict) and len(ingredient['children'][0]):
                if parent:
                    try:
                        parent_li = self.parent_li_ul_ref[parent].add(self._generate_li(ingredient_id=ingredient['ingredientId']))
                    except AttributeError:
                        continue
                else:
                    try:
                        parent_li = self.html.add(self._generate_li(ingredient_id=ingredient['ingredientId']))
                    except AttributeError:
                        continue

                parent_li_ul = parent_li.add(ul())

                if not ingredient['ingredientId'] in self.parent_li_ul_ref:
                    self.parent_li_ul_ref[ingredient['ingredientId']] = parent_li_ul
                self._walk(ingredient['children'], ingredient['ingredientId'], parent_li_ul)
            else:
                if parent:
                    try:
                        parent_li = self.parent_li_ul_ref[parent].add(self._generate_li(ingredient_id=ingredient['ingredientId']))
                    except AttributeError:
                        continue
                else:
                    try:
                        parent_li = self.html.add(self._generate_li(ingredient_id=ingredient['ingredientId']))
                    except AttributeError:
                        continue
                parent_li.add(ul())

    def walk(self):
        self._get_ingredients_dict()
        self._walk(self.dish_tree)
        return self.html


class IngredientWalkPrint(object):
    def __init__(self, dish_id, dish_tree):
        self.dish_id = dish_id
        self.dish_tree = dish_tree
        self.html = span(cls='allergen_detail')
        self.parent_span_div_ref = {}
        self.ingredients_dict = {}

    def _get_ingredients_dict(self):
        dish_id = ObjectId(self.dish_id)
        for i in Ingredient.objects.filter(dish=dish_id):
            self.ingredients_dict[str(i.pk)] = {'name': i.name, 'is_allergen': i.is_allergen, 'is_meat': i.is_meat, 'is_gluten': i.is_gluten}

    def _generate_span(self, ingredient_id, parent=None):
        dish_id = self.dish_id
        ingredient_dict = self.ingredients_dict.get(ingredient_id)
        ingredient_name = ingredient_dict.get('name')
        cls = ['ingredient']
        if ingredient_dict.get('is_allergen'):
            cls.append('strong')
        if parent:
            cls.append('ingredient_child')
        else:
            cls.append('ingredient_parent')
        ret_span = span(ingredient_name, cls=' '.join(cls))
        return ret_span

    def _walk(self, ingredients, parent=None, parent_span_div=None):
        for ingredient in ingredients:
            if isinstance(ingredient, list):
                self._walk(ingredient, parent, parent_span_div)
            elif isinstance(ingredient, dict) and len(ingredient['children'][0]):
                if parent:
                    try:
                        parent_span = self.parent_span_div_ref[parent].add(self._generate_span(ingredient_id=ingredient['ingredientId'], parent=True))
                    except AttributeError:
                        continue
                else:
                    try:
                        parent_span = self.html.add(self._generate_span(ingredient_id=ingredient['ingredientId']))
                    except AttributeError:
                        continue

                parent_span_div = parent_span.add(span(cls='has_children'))

                if not ingredient['ingredientId'] in self.parent_span_div_ref:
                    self.parent_span_div_ref[ingredient['ingredientId']] = parent_span_div
                self._walk(ingredient['children'], ingredient['ingredientId'], parent_span_div)
            else:
                if parent:
                    try:
                        parent_span = self.parent_span_div_ref[parent].add(self._generate_span(ingredient_id=ingredient['ingredientId'], parent=True))
                    except AttributeError:
                        continue
                else:
                    try:
                        parent_span = self.html.add(self._generate_span(ingredient_id=ingredient['ingredientId']))
                    except AttributeError:
                        continue
                parent_span_div = parent_span.add(span(cls='has_children'))

    def walk(self):
        self._get_ingredients_dict()
        self._walk(self.dish_tree)
        return self.html


class CloneDishWalk(IngredientWalk):
    def _get_ingredients_mapping(self):
        self.ingredient_mapping = {}
        dish_id = ObjectId(self.dish_id)
        original_dish_id = ObjectId(self.dish_tree[0][0]['dishId'])
        tmp_dict = {}
        for i in Ingredient.objects.filter(dish=dish_id):
            tmp_dict[i.name] = str(i.pk)
        for i in Ingredient.objects.filter(dish=original_dish_id):
            try:
                self.ingredient_mapping[str(i.pk)] = tmp_dict[i.name]
            except KeyError:
                continue

    def _walk(self, ingredients, parent=None, parent_li_ul=None):
        for ingredient in ingredients:
            if isinstance(ingredient, list):
                self._walk(ingredient, parent, parent_li_ul)
            elif isinstance(ingredient, dict) and len(ingredient['children'][0]):
                if parent:
                    try:
                        parent_li = self.parent_li_ul_ref[parent].add(self._generate_li(ingredient_id=self.ingredient_mapping[ingredient['ingredientId']]))
                    except AttributeError:
                        continue
                else:
                    try:
                        parent_li = self.html.add(self._generate_li(ingredient_id=self.ingredient_mapping[ingredient['ingredientId']]))
                    except AttributeError:
                        continue

                parent_li_ul = parent_li.add(ul())

                if not ingredient['ingredientId'] in self.parent_li_ul_ref:
                    self.parent_li_ul_ref[ingredient['ingredientId']] = parent_li_ul
                self._walk(ingredient['children'], ingredient['ingredientId'], parent_li_ul)
            else:
                if parent:
                    try:
                        parent_li = self.parent_li_ul_ref[parent].add(self._generate_li(ingredient_id=self.ingredient_mapping[ingredient['ingredientId']]))
                    except AttributeError:
                        continue
                else:
                    try:
                        parent_li = self.html.add(self._generate_li(ingredient_id=self.ingredient_mapping[ingredient['ingredientId']]))
                    except AttributeError:
                        continue
                parent_li.add(ul())

    def walk(self):
        self._get_ingredients_mapping()
        return super(CloneDishWalk, self).walk()


def mail_chimp_subscribe_email(email):
    api = Mailchimp(settings.MAIL_CHIMP_API_KEY)
    try:
        api.lists.subscribe(settings.MAIL_CHIMP_SIGNUP_LIST, {'email': email}, double_optin=True)
    except ListAlreadySubscribedError:
        pass
    return True


class CloneIngredientWalk(CloneDishWalk):
    def __init__(self, dish_id, dish_tree):
        self.dish_id = dish_id
        self.dish_tree = dish_tree
        self.html = ul()
        self.parent_li_ul_ref = {}
        self.ingredients_dict = {}

    def _save_ingredients(self, ingredients, parent=None):
        for ingredient in ingredients:
            if isinstance(ingredient, list):
                self._save_ingredients(ingredient, parent)
            elif isinstance(ingredient, dict) and len(ingredient['children'][0]):
                original = Ingredient.objects.get(dish=ObjectId(ingredient['dishId']), pk=ObjectId(ingredient['ingredientId']))
                clone = Ingredient.objects.create(dish=ObjectId(self.dish_id),
                                                  name=original.name,
                                                  parent=ObjectId(parent) if parent else None,
                                                  order=original.order,
                                                  is_allergen=original.is_allergen,
                                                  is_meat=original.is_meat,
                                                  is_gluten=original.is_gluten,
                                                  added_on=datetime.now())
                self._save_ingredients(ingredient['children'], str(clone.id))
            else:
                original = Ingredient.objects.get(dish=ObjectId(ingredient['dishId']), pk=ObjectId(ingredient['ingredientId']))
                clone = Ingredient.objects.create(dish=ObjectId(self.dish_id),
                                                  name=original.name,
                                                  parent=ObjectId(parent) if parent else None,
                                                  order=original.order,
                                                  is_allergen=original.is_allergen,
                                                  is_meat=original.is_meat,
                                                  is_gluten=original.is_gluten,
                                                  added_on=datetime.now())

    def walk(self):
        self._save_ingredients(self.dish_tree, parent=None)
        return super(CloneIngredientWalk, self).walk()
