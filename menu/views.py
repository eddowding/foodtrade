import json
from datetime import datetime
from copy import deepcopy
from bson.objectid import ObjectId, InvalidId
from mongoengine.queryset import Q
from bson import json_util
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from mongoengine.django.auth import User
from menu.models import Establishment, Menu, MenuSection, Dish, Allergen, Meat, Gluten, Connection


"""
Common views.
"""
@login_required(login_url=reverse_lazy('menu-login'))
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url=reverse_lazy('menu-login'))
def menu(request):
    ''' Get list of menus '''
    establishments = Establishment.objects.filter(user=request.user)
    menus = Menu.objects.filter(establishment__in=establishments).order_by('-added_on')
    return render(request, 'menu/menus.html', {'menus' : menus})


def register(request):
    ''' User Registration in menu '''
    if request.method == 'POST':
        user = User.create_user(username=request.POST.get('username'), password=request.POST.get('password'))
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            if user.is_active:
                auth_login(request, user)
        return HttpResponseRedirect(reverse_lazy('menu'))
    else:
        return render(request, 'menu/register.html')


def login(request):
    ''' User login in menu '''
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse_lazy('menu_dashboard'))
            else:
                return render(request, 'menu/login.html', {'failure': True})
        else:
            return render(request, 'menu/login.html', {'failure': True})
    else:
        return render(request, 'menu/login.html', {'failure': False})


def user_lookup_count(request):
    query = {}
    for k, v in request.GET.items():
        query[k] = v
        return HttpResponse(json.dumps({'status': True, 'count': User.objects.filter(**query).count()}))


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse_lazy('menu-login'))


"""
Menu views.
"""
@login_required(login_url=reverse_lazy('menu-login'))
def establishment_lookup_name(request):
    query = {'BusinessName__icontains': request.GET.get('q')}
    ret_list = []
    establishments = Establishment.objects.filter(**query)
    for obj in establishments:
        name = '%s | %s | %s' % (obj.BusinessName, obj.BusinessType, obj.full_address())
        ret_list.append({'name': name, 'value': str(obj.pk), 'type': 1})
    return HttpResponse(json.dumps({'status': True, 'objs': ret_list}))


def menu_render(user):
    establishments = Establishment.objects.filter(user=user)
    menus = Menu.objects.filter(establishment__in=establishments).order_by('-added_on')
    return render_to_string('includes/_menu.html', {'menus': menus})


@login_required(login_url=reverse_lazy('menu-login'))
def create_menu(request):
    establishment = request.POST.get('establishment')
    name = request.POST.get('name')
    try:
        Establishment.objects.filter(pk=ObjectId(establishment)).update(set__user=request.user)
        Menu.objects.create(establishment=ObjectId(establishment), name=name, added_on=datetime.now())
    except InvalidId:
        establishment = Establishment.objects.create(user=request.user, BusinessName=establishment, added_on=datetime.now())
        Menu.objects.create(establishment=establishment.pk, name=name, added_on=datetime.now())
    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def delete_menu(request):
    Menu.objects.filter(pk=ObjectId(request.POST.get('id'))).delete()
    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def create_menu_section(request):
    insert_dict = deepcopy(request.POST.dict())
    insert_dict['menu'] = ObjectId(insert_dict['menu'])
    insert_dict['added_on'] = datetime.now()
    MenuSection.objects.create(**insert_dict)
    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def delete_menu_section(request):
    MenuSection.objects.filter(pk=ObjectId(request.POST.get('id'))).delete()
    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def dish_lookup_name(request):
    query = {'name__icontains': request.GET.get('q')}
    ret_list = []
    ingredients_list = []
    for dish in Dish.objects.filter(**query):
        for ingredient in dish.ingredients:
            ingredients_list.append(str(ingredient.name))
        name = '%s (%s)' % (dish.name, ", ".join(ingredients_list))
        tmp_dict = {'name': name, 'value': str(dish.pk)}
        tmp_dict['ingredients'] = dish.get_ingredient_tree()
        ret_list.append(tmp_dict)
    return HttpResponse(json.dumps({'status': True, 'objs': ret_list}))


@login_required(login_url=reverse_lazy('menu-login'))
def create_dish(request):
    insert_dict = deepcopy(request.POST.dict())
    insert_dict['menu_section'] = ObjectId(insert_dict['menu_section'])
    insert_dict['added_on'] = datetime.now()
    try:
        dish = Dish.objects.get(pk=ObjectId(insert_dict['name']))
        insert_dict['name'] = dish.name
        insert_dict['ingredients'] = dish.ingredients
    except InvalidId:
        pass

    Dish.objects.create(**insert_dict)
    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def delete_dish(request):
    Dish.objects.filter(pk=ObjectId(request.POST.get('id'))).delete()
    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))



@login_required(login_url=reverse_lazy('menu-login'))
def create_ingredient(request):
    ingredient_list = []
    dish = request.POST.get('dish')
    insert_dict = deepcopy(request.POST.dict())
    del insert_dict['dish']
    ingredient_input = insert_dict['name'].split('(')
    insert_dict['name'] = ingredient_input[0]
    ingredient_list.append(insert_dict)
    if len(ingredient_input)>1:
        child_ingredient = ingredient_input[1].replace(')','')
        child_ingredient = child_ingredient.split(',')
        for child in child_ingredient:  
            child_name = child
            ingredient_list.append({'name':child_name, 'parent':ingredient_input[0]})
    #TODO: cache this to save query
    dish_is_allergen = False
    dish_is_meat = False
    dish_is_gluten = False
    dish_obj = Dish.objects.get(pk=ObjectId(dish))
    for ingredient in dish_obj.ingredients:
        if ingredient.is_allergen:
            dish_is_allergen = True
        if ingredient.is_meat:
            dish_is_meat = True
        if ingredient.is_gluten:
            dish_is_gluten = True
    for data_to_insert in ingredient_list:
        data_to_insert['is_allergen'] = True if Allergen.objects.filter(name=insert_dict['name']).count() else False
        data_to_insert['is_meat'] = True if Meat.objects.filter(name=insert_dict['name']).count() else False
        data_to_insert['is_gluten'] = True if Gluten.objects.filter(name=insert_dict['name']).count() else False
        if data_to_insert['is_allergen']:
            dish_is_allergen = True
        if data_to_insert['is_meat']:
            dish_is_meat = True
        if data_to_insert['is_gluten']:
            dish_is_gluten = True
        Dish.objects.filter(pk=ObjectId(dish)).update(set__is_allergen=dish_is_allergen,
                                                      set__is_meat=dish_is_meat,
                                                      set__is_gluten=dish_is_gluten,
                                                      push__ingredients=data_to_insert)


    dish_obj = Dish.objects.get(pk=ObjectId(dish))
    parent = insert_dict.get('parent')
    parent_update_dict = {}
    if insert_dict['is_allergen']:
        parent_update_dict['set__ingredients__S__is_allergen'] = True
    if insert_dict['is_meat']:
        parent_update_dict['set__ingredients__S__is_meat'] = True
    if insert_dict['is_gluten']:
        parent_update_dict['set__ingredients__S__is_gluten'] = True
    while parent:
        for ingredient in dish_obj.ingredients:
            if parent == ingredient.name:
                Dish.objects.filter(pk=ObjectId(dish), ingredients__name=parent).update(**parent_update_dict)
                dish_obj = Dish.objects.get(pk=ObjectId(dish))
                parent = ingredient.parent
    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def update_ingredient(request):
    dish = request.POST.get('dish')
    insert_dict = deepcopy(request.POST.dict())
    del insert_dict['dish']
    #TODO: cache this to save query
    insert_dict['is_allergen'] = True if Allergen.objects.filter(name=insert_dict['name']).count() else False
    insert_dict['is_meat'] = True if Meat.objects.filter(name=insert_dict['name']).count() else False
    insert_dict['is_gluten'] = True if Gluten.objects.filter(name=insert_dict['name']).count() else False
    dish_is_allergen = False
    dish_is_meat = False
    dish_is_gluten = False
    prev_parent = None
    for ingredient in Dish.objects.get(pk=ObjectId(dish)).ingredients:
        if not insert_dict.get('parent'):
            if insert_dict['name'] == ingredient.name:
                prev_parent = ingredient.parent
        if ingredient.is_allergen:
            dish_is_allergen = True
        if ingredient.is_meat:
            dish_is_meat = True
        if ingredient.is_gluten:
            dish_is_gluten = True
    if insert_dict['is_allergen']:
        dish_is_allergen = True
    if insert_dict['is_meat']:
        dish_is_meat = True
    if insert_dict['is_gluten']:
        dish_is_gluten = True
    dish_obj = Dish.objects.filter(pk=ObjectId(dish), ingredients__name=insert_dict['name']) \
                                                    .update(set__is_allergen=dish_is_allergen,
                                                            set__is_meat=dish_is_meat,
                                                            set__is_gluten=dish_is_gluten,
                                                            set__ingredients__S__parent=insert_dict['parent'],
                                                            set__ingredients__S__order=insert_dict['order'],
                                                            set__ingredients__S__is_allergen=insert_dict['is_allergen'],
                                                            set__ingredients__S__is_meat=insert_dict['is_meat'],
                                                            set__ingredients__S__is_gluten=insert_dict['is_gluten'])

    dish_obj = Dish.objects.get(pk=ObjectId(dish))
    parent = insert_dict.get('parent')
    parent_update_dict = {}
    if insert_dict['is_allergen']:
        parent_update_dict['set__ingredients__S__is_allergen'] = True
    if insert_dict['is_meat']:
        parent_update_dict['set__ingredients__S__is_meat'] = True
    if insert_dict['is_gluten']:
        parent_update_dict['set__ingredients__S__is_gluten'] = True
    while parent:
        for ingredient in dish_obj.ingredients:
            if parent == ingredient.name:
                Dish.objects.filter(pk=ObjectId(dish), ingredients__name=parent).update(**parent_update_dict)
                dish_obj = Dish.objects.get(pk=ObjectId(dish))
                parent = ingredient.parent

    while prev_parent:
        prev_parent_update_dict = {'set__ingredients__S__is_allergen': False,
                                   'set__ingredients__S__is_meat': False,
                                   'set__ingredients__S__is_gluten': False}
        for ingredient in dish_obj.ingredients:
            if prev_parent == ingredient.name:
                tmp_parent = ingredient.parent
            if prev_parent == ingredient.parent:
                if ingredient.is_allergen:
                    prev_parent_update_dict['set__ingredients__S__is_allergen'] = True
                if ingredient.is_meat:
                    prev_parent_update_dict['set__ingredients__S__is_meat'] = True
                if ingredient.is_gluten:
                    prev_parent_update_dict['set__ingredients__S__is_gluten'] = True
        Dish.objects.filter(pk=ObjectId(dish), ingredients__name=prev_parent).update(**prev_parent_update_dict)
        prev_parent = tmp_parent

    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def delete_ingredient(request):
    prev_parent = None
    for ingredient in Dish.objects.get(pk=ObjectId(request.POST.get('id'))).ingredients:
        if request.POST.get('name') == ingredient.name:
            prev_parent = ingredient.parent

    Dish.objects.filter(pk=ObjectId(request.POST.get('id'))) \
                                    .update(pull__ingredients__name=request.POST.get('name'))
    dish_is_allergen = False
    dish_is_meat = False
    dish_is_gluten = False
    for ingredient in Dish.objects.get(pk=ObjectId(request.POST.get('id'))).ingredients:
        if ingredient.is_allergen:
            dish_is_allergen = True
        if ingredient.is_meat:
            dish_is_meat = True
        if ingredient.is_gluten:
            dish_is_gluten = True
    Dish.objects.filter(pk=ObjectId(request.POST.get('id'))) \
                                    .update(set__is_allergen=dish_is_allergen,
                                            set__is_meat=dish_is_meat,
                                            set__is_gluten=dish_is_gluten)

    dish_obj = Dish.objects.get(pk=ObjectId(request.POST.get('id')))
    while prev_parent:
        prev_parent_update_dict = {'set__ingredients__S__is_allergen': False,
                                   'set__ingredients__S__is_meat': False,
                                   'set__ingredients__S__is_gluten': False}
        for ingredient in dish_obj.ingredients:
            if prev_parent == ingredient.name:
                tmp_parent = ingredient.parent
            if prev_parent == ingredient.parent:
                if ingredient.is_allergen:
                    prev_parent_update_dict['set__ingredients__S__is_allergen'] = True
                if ingredient.is_meat:
                    prev_parent_update_dict['set__ingredients__S__is_meat'] = True
                if ingredient.is_gluten:
                    prev_parent_update_dict['set__ingredients__S__is_gluten'] = True
        Dish.objects.filter(pk=ObjectId(request.POST.get('id')), ingredients__name=prev_parent).update(**prev_parent_update_dict)
        prev_parent = tmp_parent

    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def ingredient_lookup_name(request):
    ''' Lookup ingredient with nme of ingredients '''
    keyword = request.GET.get('q')
    query1 = ( Q(ingredients__name__icontains = keyword) |\
               Q(ingredients__parent__icontains = keyword), )
    query2 = {'name__icontains': keyword}
    tmp_dict = {}
    tmp_list = []
    klass_list = [Gluten, Allergen, Meat]
    for dish in Dish.objects.filter(*query1):
        for ingredient in dish.ingredients:
            if keyword in ingredient.parent:
                if not tmp_dict.has_key(ingredient.parent):
                    tmp_dict[ingredient.parent] = []
                tmp_dict[ingredient.parent].append(ingredient.name)
            if keyword in ingredient.name:
                if not tmp_dict.has_key(ingredient.name):
                    tmp_dict[ingredient.name] = []
    for suggestion, children in tmp_dict.items():
        if len(children) > 0:
            suggestion = '%s (%s)' % (suggestion, ", ".join(children))
        tmp_list.append(suggestion)
    for klass in klass_list:
        for obj in klass.objects.filter(**query2):
            if keyword in obj.name:
                tmp_list.append(obj.name)
    tmp_list = list(set(tmp_list))
    return HttpResponse(json.dumps({'status': True, 'objs': [{'name': n} for n in tmp_list]}))



@login_required(login_url=reverse_lazy('menu-login'))
def print_preview_menu(request , id):
    '''Print Preview for menu'''
    menu = Menu.objects.get(pk=ObjectId(id))
    return render(request, 'menu/menu-print-preview.html', {'menu' : menu})



"""
Connection views.
"""
def connection(request):
    buyers = Connection.objects.filter(user=request.user, connection_type=2)
    sellers = Connection.objects.filter(user=request.user, connection_type=1)
    return render(request, 'connection.html', {'buyers': buyers, 'sellers': sellers})

def create_connection(request):
    klass_lookup = {1: Establishment}
    klass = klass_lookup.get(int(request.POST.get('object_type')))
    insert_dict = {}
    insert_dict['user'] = request.user
    insert_dict['connection'] = klass.objects.get(pk=ObjectId(request.POST.get('connection_id')))
    insert_dict['connection_type'] = int(request.POST.get('connection_type'))
    insert_dict['added_on'] = datetime.now()
    Connection.objects.create(**insert_dict)
    buyers = Connection.objects.filter(user=request.user, connection_type=2)
    sellers = Connection.objects.filter(user=request.user, connection_type=1)
    html = {'buyers': render_to_string('includes/_connection_table_buyer.html', {'buyers': buyers}),
            'sellers': render_to_string('includes/_connection_table_seller.html', {'sellers': sellers})}
    return HttpResponse(json.dumps({'success': True, 'obj': html}))
