from django import template
from bson.objectid import ObjectId
from menu.models import Dish
from menu.peer import IngredientWalk, IngredientWalkPrint


register = template.Library()

@register.simple_tag
def render_menu(dish_id):
    dish_id = ObjectId(dish_id)
    dish = Dish.objects.get(pk=dish_id)
    iw = IngredientWalk(str(dish.pk), dish.json)
    return iw.walk().render()
