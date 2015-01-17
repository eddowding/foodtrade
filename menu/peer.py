from itertools import izip_longest
from bson.objectid import ObjectId
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
