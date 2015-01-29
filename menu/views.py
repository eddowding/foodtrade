import json, re
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
from menu.models import Establishment, Menu, MenuSection, Dish, Allergen, Meat, Gluten, Connection, Ingredient, ModerationIngredient
from menu.peer import ingredient_walk, IngredientWalkPrint, CloneDishWalk


"""
Common views.
"""
@login_required(login_url=reverse_lazy('menu-login'))
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url=reverse_lazy('menu-login'))
def paymentSuccess(request):
    '''
    On payment success
    '''
    return render(request, 'payment_success.html')


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
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if bool(re.match(pattern, request.POST.get('username'))):
            user.email = request.POST.get('username')
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
    establishments = Establishment.objects.filter(**query)[:10]
    for obj in establishments:
        name = '<strong>%s</strong> <span class="est_type">%s</span> <span class="est_addr">%s</span>' % (obj.BusinessName, obj.BusinessType, obj.full_address())
        ret_list.append({'name': name, 'value': str(obj.pk), 'type': 1})
    return HttpResponse(json.dumps({'status': True, 'objs': ret_list}))


@login_required(login_url=reverse_lazy('menu-login'))
def establishment_lookup_search(request):
    #query = {'$or':[{'BusinessName__icontains': request.GET.get('q')}, {'full_address__icontains': request.GET.get('q')}]}
    ret_list = []
    establishments = Establishment.objects(Q(BusinessName__icontains=request.GET.get('q'))\
                                            | Q(AddressLine1__icontains=request.GET.get('q')) \
                                            | Q(AddressLine2__icontains=request.GET.get('q'))\
                                            | Q(AddressLine3__icontains=request.GET.get('q'))\
                                            | Q(AddressLine4__icontains=request.GET.get('q')))[:10]
    for obj in establishments:
        name = '<strong>%s</strong> <span class="est_type">%s</span> <span class="est_addr">( %s )</span>'  % (obj.BusinessName, obj.BusinessType, obj.full_address())
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
    for dish in Dish.objects.filter(**query):
        name = '%s (%s)' % (dish.name, ", ".join(dish.get_ingredient_names().values_list('name'))[:80])
        tmp_dict = {'name': name, 'value': str(dish.pk), 'html': dish.html}
        ret_list.append(tmp_dict)
    return HttpResponse(json.dumps({'status': True, 'objs': ret_list}))


@login_required(login_url=reverse_lazy('menu-login'))
def create_dish(request):
    html = ''
    insert_dict = deepcopy(request.POST.dict())
    insert_dict['menu_section'] = ObjectId(insert_dict['menu_section'])
    insert_dict['added_on'] = datetime.now()
    try:
        dish = Dish.objects.get(pk=ObjectId(insert_dict['name']))
        insert_dict['name'] = dish.name
        insert_dict.update({'is_allergen':dish.is_allergen,
                            'is_meat':dish.is_meat,
                            'is_gluten':dish.is_gluten})
        ingredient_objs = dish.get_ingredient_names()
    except InvalidId, DoesNotExist:
        pass

    new_dish = Dish.objects.create(**insert_dict)
    # create ingredient objs
    try:
        for ingredient in ingredient_objs:
            ind = Ingredient.objects.create(**ingredient.to_mongo())
            ind.dish = new_dish # making sure dish reference is always right
            ind.save()
    except UnboundLocalError:
        pass
    try:
        cdw = CloneDishWalk(str(new_dish.pk), json.loads(dish.json))
        new_dish.html = cdw.walk().render()
        new_dish.save()
    except UnboundLocalError:
        pass
    except ValueError:
        pass

    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user), 'dish_id':str(new_dish.pk) if new_dish.html else ''
                                    }, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def update_dish(request):
    pk = ObjectId(request.POST.get('pk'))
    html = request.POST.get('html')
    if html:
        serialized = json.loads(request.POST.get('serialized')) if request.POST.get('serialized') else ''
        if not serialized:
            dish = Dish.objects.get(pk=ObjectId(pk))
            serialized = dish.json
        ingredient_walk(serialized)
        iwp = IngredientWalkPrint(request.POST.get('pk'), serialized)
        print_html = iwp.walk().render()
        Dish.objects.filter(pk=pk).update(set__html=html, set__json=request.POST.get('serialized'), set__print_html=print_html)
        return HttpResponse(json.dumps({'status': True}))
    else:
        Dish.objects.filter(pk=pk).update(set__name=request.POST.get('name'),
                                                 set__description = request.POST.get('description'),
                                                 set__price = request.POST.get('price'),
                                                 set__modified_on = datetime.now())
        return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def delete_dish(request):
    Dish.objects.filter(pk=ObjectId(request.POST.get('id'))).delete()
    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def change_ingredient_html(request):
    '''
    '''
    dish = Dish.objects.get(pk=ObjectId(request.POST['dish_id']))
    ingredient = Ingredient.objects.get(pk=ObjectId(request.POST['ingredient_id']))
    new_ingredient = Ingredient.objects.get(dish=dish, name=ingredient.name)
    return HttpResponse(json.dumps({'status':True, 'ingredient_id':str(new_ingredient.id)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def create_ingredient(request):
    if request.POST.get('name') == '':
        return HttpResponse(json.dumps({'status': False}, default=json_util.default), content_type="application/json")
    insert_dict = {}
    insert_dict['dish'] = ObjectId(request.POST.get('dish'))
    insert_dict['name'] = request.POST.get('name')
    insert_dict['parent'] = ObjectId(request.POST.get('parent')) if request.POST.get('parent') else None
    insert_dict['order'] = int(request.POST.get('order')) if request.POST.get('order') else 1
    insert_dict['is_allergen'] = True if Allergen.objects.filter(name__iexact=insert_dict['name']).count() else False
    insert_dict['is_meat'] = True if Meat.objects.filter(name__iexact=insert_dict['name']).count() else False
    insert_dict['is_gluten'] = True if Gluten.objects.filter(name__iexact=insert_dict['name']).count() else False
    insert_dict['added_on'] = datetime.now()
    ingredient = Ingredient.objects.create(**insert_dict)
    
    # update dish as it is now allergen, meat or gluten
    dish = Dish.objects.get(pk=ObjectId(request.POST.get('dish')))
    if insert_dict['is_allergen']:
        dish.is_allergen = True
    if insert_dict['is_meat']:
        dish.is_meat = True
    if insert_dict['is_gluten']:
        dish.is_gluten = True
    dish.save()
    return HttpResponse(json.dumps({'status': True, 'obj': ingredient.to_mongo()}, default=json_util.default), content_type="application/json")


@login_required(login_url=reverse_lazy('menu-login'))
def update_ingredient(request):
    dish = request.POST.get('dish')
    insert_dict = deepcopy(request.POST.dict())
    del insert_dict['dish']
    #TODO: cache this to save query
    insert_dict['is_allergen'] = True if Allergen.objects.filter(name__iexact=insert_dict['name']).count() else False
    insert_dict['is_meat'] = True if Meat.objects.filter(name__iexact=insert_dict['name']).count() else False
    insert_dict['is_gluten'] = True if Gluten.objects.filter(name__iexact=insert_dict['name']).count() else False
    dish_is_allergen = False
    dish_is_meat = False
    dish_is_gluten = False
    prev_parent = None
    for ingredient in Dish.objects.get(pk=ObjectId(dish)).ingredients:
        if ingredient.name == 'Type Ingredient Here':
            continue
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
            if ingredient.name == 'Type Ingredient Here':
                continue
            if parent == ingredient.name:
                Dish.objects.filter(pk=ObjectId(dish), ingredients__name=parent).update(**parent_update_dict)
                dish_obj = Dish.objects.get(pk=ObjectId(dish))
                parent = ingredient.parent

    while prev_parent:
        prev_parent_update_dict = {'set__ingredients__S__is_allergen': False,
                                   'set__ingredients__S__is_meat': False,
                                   'set__ingredients__S__is_gluten': False}
        for ingredient in dish_obj.ingredients:
            if ingredient.name == 'Type Ingredient Here':
                continue
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
def update_ingredient_name(request):
    insert_dict = {}
    insert_dict['set__name'] = request.POST.get('value')
    insert_dict['set__is_allergen'] = True if Allergen.objects.filter(name__iexact=request.POST.get('value')).count() else False
    insert_dict['set__is_meat'] = True if Meat.objects.filter(name__iexact=request.POST.get('value')).count() else False
    insert_dict['set__is_gluten'] = True if Gluten.objects.filter(name__iexact=request.POST.get('value')).count() else False
    Ingredient.objects.filter(pk=ObjectId(request.POST.get('pk'))).update(**insert_dict)
    ingredient = Ingredient.objects.get(pk=ObjectId(request.POST.get('pk')))
    return HttpResponse(json.dumps({'status': True, obj: Ingredient}, default=json_util.default), content_type="application/json")


@login_required(login_url=reverse_lazy('menu-login'))
def delete_ingredient(request):
    Ingredient.objects.filter(pk=ObjectId(request.POST.get('id'))).delete()
    return HttpResponse(json.dumps({'status': True}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def ingredient_lookup_name(request):
    ''' Lookup ingredient with nme of ingredients '''
    keyword = request.GET.get('q')
    query2 = {'name__icontains': keyword}
    tmp_dict = {}
    tmp_list = []
    klass_list = [Gluten, Allergen, Meat]
    for klass in klass_list:
        for obj in klass.objects.filter(**query2):
            if keyword.lower() in obj.name.lower():
                tmp_list.append(obj.name)
    tmp_list = list(set(tmp_list))
    return HttpResponse(json.dumps({'status': True, 'objs': [{'name': n} for n in tmp_list]}))



@login_required(login_url=reverse_lazy('menu-login'))
def print_preview_menu(request , id):
    '''Print Preview for menu'''
    menu = Menu.objects.get(pk=ObjectId(id))
    return render(request, 'menu/menu-print-preview.html', {'menu' : menu})


@login_required(login_url=reverse_lazy('menu-login'))
def save_moderation_ingredient(request):
    pk = ObjectId(request.POST.get('pk'))
    html = request.POST.get('html')
    serialized = json.loads(request.POST.get('serialized'))
    iwp = IngredientWalkPrint(request.POST.get('pk'), serialized)
    print_html = iwp.walk().render()
    ingredient_walk(serialized)
    ingredient = json.loads(request.POST.get('ingredient'))
    ingredient['user'] = request.user
    ingredient['added_on'] = datetime.now()

    Dish.objects.filter(pk=pk).update(set__html=html, set__json=request.POST.get('serialized'), set__print_html=print_html)
    ModerationIngredient.objects.create(**ingredient)

    #ing  = Ingredient.objects.filter(name__iexact=ingredient['name'])
    #updt_dish = {}
    #for i in ing:
    #if ingredient.get('is_meat'):
    #    Dish.objects.filter(pk=pk).update(set__is_meat=True)
    #elif ingredient.get('is_allergen'):
    #    Dish.objects.filter(pk=pk).update(set__is_allergen=True)
    #elif ingredient.get('is_gluten'):
    #    Dish.objects.filter(pk=pk).update(set__is_gluten=True)
    #Dish.objects.filter(pk=pk).update(updt_dish)
    #return HttpResponse(json.dumps({'status': True}, default=json_util.default), content_type="application/json")
    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default),
                        content_type="application/json")


@login_required(login_url=reverse_lazy('menu-login'))
def update_moderation_ingredient(request):
    establishments = Establishment.objects.filter(user=request.user)
    menus = Menu.objects.filter(establishment__in=establishments)
    menu_sections = MenuSection.objects.filter(menu__in=menus)
    dishes = Dish.objects.filter(menu_section__in= menu_sections)
    ingredients = Ingredient.objects.filter(dish__in=dishes, is_applied=False)
    objs = []
    for ingredient in ingredients:
        objs.append({'pk': ingredient.pk, 'is_allergen': ingredient.is_allergen,
                    'is_meat': ingredient.is_meat, 'is_gluten': ingredient.is_gluten})
    Ingredient.objects.filter(dish__in=dishes, is_applied=False).update(set__is_applied=True)
    return HttpResponse(json.dumps({'status': True, 'objs': objs}, default=json_util.default), content_type="application/json")


def update_moderation_ingredient_status(request):
    '''
    updates the status of ModerationIngredient
    '''
    if request.method == 'GET':
        moderation_ingredients_objs = ModerationIngredient.objects.filter(status=1)
        return render(request, 'moderation_ingredients.html', {'objs': moderation_ingredients_objs})
    else:
        moderation_obj = ModerationIngredient.objects.get(pk=ObjectId(request.POST.get('pk')))
        moderation_obj.status = int(request.POST.get('status'))
        moderation_obj.save()
        return HttpResponse(json.dumps({'status':True}, default=json_util.default), content_type="application/json")

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
