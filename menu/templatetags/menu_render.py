import json
from django import template
from bson.objectid import ObjectId
from menu.models import Dish
from menu.peer import IngredientWalk, IngredientWalkPrint


register = template.Library()

@register.simple_tag
def render_menu(dish):
    try:
        iw = IngredientWalk(str(dish.pk), json.loads(dish.json))
    except ValueError:
        return ''
    return iw.walk().render()


@register.simple_tag
def render_menu_print(dish):
    try:
        iwp = IngredientWalkPrint(str(dish.pk), json.loads(dish.json))
    except ValueError:
        return ''
    return iwp.walk().render()
