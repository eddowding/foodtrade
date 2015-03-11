import json
import re
import analytics
import stripe
from datetime import datetime, timedelta
from copy import deepcopy
from bson.objectid import ObjectId, InvalidId
from bson.dbref import DBRef
from mongoengine.queryset import Q
from bson import json_util
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.conf import settings
from mongoengine.django.auth import User
from menu.models import Establishment, Menu, MenuSection, Dish, Allergen, Meat, Gluten, Connection, Ingredient, ModerationIngredient, Payment
from menu.peer import ingredient_walk, IngredientWalkPrint, CloneDishWalk, mail_chimp_subscribe_email, CloneIngredientWalk

analytics.write_key = 'FVQBpRqubj7q6USVKrGrPeLG08SmADaC'


"""
Common views.
"""
@login_required(login_url=reverse_lazy('menu-login'))
def dashboard(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'payments': payments})


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
    has_payment = True if Payment.objects.filter(user=request.user).count() else False
    return render(request, 'menu/menus.html', {'menus': menus, 'settings': settings, 'has_payment': has_payment})


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
        mail_chimp_subscribe_email(user.email)
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            if user.is_active:
                auth_login(request, user)
        '''
        after register , the user will be redirected to the dashboard not to menu page
        '''
        return HttpResponseRedirect(reverse_lazy('menu_dashboard'))
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
    has_payment = True if Payment.objects.filter(user=request.user).count() else False
    return render_to_string('includes/_menu.html', {'menus': menus, 'has_payment': has_payment})


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
    analytics.track(request.user.email, 'Menu Created', {
        'name': name
    })
    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def delete_menu(request):
    Menu.objects.filter(pk=ObjectId(request.POST.get('id'))).delete()
    return HttpResponse(json.dumps({'status': True, 'html': menu_render(request.user)}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def edit_menu(request):
    establishment = request.POST.get('establishment')
    name = request.POST.get('name')
    menu_id = request.POST.get('id')
    try:
        Establishment.objects.filter(pk=ObjectId(establishment)).update(set__user=request.user)
        Menu.objects.filter(pk=ObjectId(menu_id), establishment=ObjectId(establishment)).update(set__name=name)
    except InvalidId:
        establishment = Establishment.objects.create(user=request.user, BusinessName=establishment, added_on=datetime.now())
        Menu.objects.filter(pk=ObjectId(menu_id)).update(set__establishment=establishment.pk, set__name=name)
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
def edit_menu_section(request):
    MenuSection.objects.filter(pk=ObjectId(request.POST.get('id'))).update(set__name=request.POST.get('name'))
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
        update_dict = {'set__html': html}
        serialized = json.loads(request.POST.get('serialized')) if request.POST.get('serialized') else ''
        if not serialized:
            dish = Dish.objects.get(pk=ObjectId(pk))
            serialized = json.loads(dish.json)
        else:
            update_dict['set__json'] = request.POST.get('serialized')

        try:
            ingredient_walk(serialized)
        except Exception as exc:
            print exc
            pass

        try:
            iwp = IngredientWalkPrint(request.POST.get('pk'), serialized)
            print_html = iwp.walk().render()
            update_dict['set__print_html'] = print_html
        except Exception as exc:
            print exc
            pass

        Dish.objects.filter(pk=pk).update(**update_dict)
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
    if request.POST.get('autoClass') == 'Ingredient':
        clone_ingredient = Ingredient.objects.get(id=ObjectId(request.POST.get('autoId')))
        insert_dict['is_allergen'] = True if Allergen.objects.filter(name__iexact=insert_dict['name']).count() else clone_ingredient.is_allergen
        insert_dict['is_meat'] = True if Meat.objects.filter(name__iexact=insert_dict['name']).count() else clone_ingredient.is_meat
        insert_dict['is_gluten'] = True if Gluten.objects.filter(name__iexact=insert_dict['name']).count() else clone_ingredient.is_gluten
    else:
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
    found_clone_match = False
    dish_is_allergen = False
    dish_is_meat = False
    dish_is_gluten = False
    if request.POST.get('autoClass') == 'Ingredient':
        clone_dish = clone_ingredient.dish
        if hasattr(clone_dish, 'json'):
            clone_ingredients = json.loads(clone_dish.json)
            for i in clone_ingredients[0]:
                if i['ingredientId'] == request.POST.get('autoId') and len(i['children']):
                    ciw = CloneIngredientWalk(request.POST.get('dish'), i['children'])
                    found_clone_match = True

            if found_clone_match:
                dish = Dish.objects.get(id=ObjectId(request.POST.get('dish')))
                if clone_ingredient.is_allergen:
                    dish_is_allergen = True
                if clone_ingredient.is_meat:
                    dish_is_meat = True
                if clone_ingredient.is_gluten:
                    dish_is_gluten = True
                Dish.objects.filter(id=ObjectId(request.POST.get('dish'))).update(set__is_allergen=dish_is_allergen,
                                                                                  set__is_meat=dish_is_meat,
                                                                                  set__is_gluten=dish_is_gluten)
    return HttpResponse(json.dumps({'status': True, 'obj': ingredient.to_mongo(),
                                    'html': ciw.walk().render() if found_clone_match else None,
                                    'dish': {'id': request.POST.get('dish'),
                                             'is_allergen': dish_is_allergen,
                                             'is_meat': dish_is_meat,
                                             'is_gluten': dish_is_gluten}},
                                    default=json_util.default), content_type="application/json")


@login_required(login_url=reverse_lazy('menu-login'))
def update_ingredient(request):
    id = ObjectId(request.POST.get('id'))
    update_dict = {}
    if request.POST.get('is_allergen') == 'true':
        update_dict['set__is_allergen'] = True
    if request.POST.get('is_meat') == 'true':
        update_dict['set__is_meat'] = True
    if request.POST.get('is_gluten') == 'true':
        update_dict['set__is_gluten'] = True
    if len(update_dict.keys()):
        Ingredient.objects.filter(pk=id).update(**update_dict)
    return HttpResponse(json.dumps({'status': True}, default=json_util.default))


@login_required(login_url=reverse_lazy('menu-login'))
def update_ingredient_name(request):
    insert_dict = {}
    insert_dict['set__name'] = request.POST.get('value')
    insert_dict['set__is_allergen'] = True if Allergen.objects.filter(name__iexact=request.POST.get('value')).count() else False
    insert_dict['set__is_meat'] = True if Meat.objects.filter(name__iexact=request.POST.get('value')).count() else False
    insert_dict['set__is_gluten'] = True if Gluten.objects.filter(name__iexact=request.POST.get('value')).count() else False
    Ingredient.objects.filter(pk=ObjectId(request.POST.get('pk'))).update(**insert_dict)
    ingredient = Ingredient.objects.get(pk=ObjectId(request.POST.get('pk')))
    return HttpResponse(json.dumps({'status': True, 'obj': ingredient.to_mongo()}, default=json_util.default), content_type="application/json")


@login_required(login_url=reverse_lazy('menu-login'))
def delete_ingredient(request):
    ingredient = Ingredient.objects.get(pk=ObjectId(request.POST.get('id')))
    dish = ingredient.dish
    parent = ingredient.parent
    ingredient.delete()

    ret_list = []
    while parent:
        if isinstance(parent, DBRef):
            break
        is_allergen = True if Allergen.objects.filter(name__iexact=parent.name).count() else False
        is_meat = True if Meat.objects.filter(name__iexact=parent.name).count() else False
        is_gluten = True if Gluten.objects.filter(name__iexact=parent.name).count() else False

        for i in Ingredient.objects.filter(parent=parent):
            if i.is_allergen:
                is_allergen = True
            if i.is_meat:
                is_meat = True
            if i.is_gluten:
                is_gluten = True

        update_dict = {}

        update_dict['set__is_allergen'] = is_allergen
        update_dict['set__is_meat'] = is_meat
        update_dict['set__is_gluten'] = is_gluten

        Ingredient.objects.filter(id=parent.id).update(**update_dict)

        ret_list.append({'id': str(parent.id), 'is_allergen': is_allergen, 'is_meat': is_meat, 'is_gluten': is_gluten})

        parent = parent.parent
        if isinstance(parent, DBRef):
            break

    is_allergen = False
    is_meat = False
    is_gluten = False
    dish_update_dict = {'set__is_allergen': False, 'set__is_meat': False, 'set__is_gluten': False}
    for i in Ingredient.objects.filter(dish=dish):
        if i.is_allergen:
            dish_update_dict['set__is_allergen'] = True
        if i.is_meat:
            dish_update_dict['set__is_meat'] = True
        if i.is_gluten:
            dish_update_dict['set__is_gluten'] = True
    Dish.objects.filter(id=dish.id).update(**dish_update_dict)
    ret_dict = {'id': str(dish.id), 'is_allergen': dish_update_dict['set__is_allergen'],
                'is_meat': dish_update_dict['set__is_meat'], 'is_gluten': dish_update_dict['set__is_gluten']}
    return HttpResponse(json.dumps({'status': True, 'objs': ret_list, 'dish': ret_dict}, default=json_util.default))


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
            tmp_list.append({'class': str(klass.__name__), 'id': str(obj.id), 'name': obj.name, 'label': obj.name})
    for i in Ingredient.objects.filter(name__icontains=keyword, parent=None)[0:10]:
        name = i.name
        # c_list = []
        # for c in i.get_children()[0:3]:
        #     c_list.append(c.name)
        # if len(c_list):
        #     name = '%s (%s)' % (name, ', '.join(c_list))
        tmp_list.append({'class': str(Ingredient.__name__), 'id': str(i.id), 'name': i.name, 'label': name})
    return HttpResponse(json.dumps({'status': True, 'objs': tmp_list[0:10]}))


def print_preview_menu(request, id):
    '''Print Preview for menu'''
    menu = Menu.objects.get(pk=ObjectId(id))
    return render(request, 'menu/menu-print-preview.html', {'menu': menu})


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

    update_dict = {}
    if ingredient.get('is_allergen'):
        update_dict['set__is_allergen'] = True
    if ingredient.get('is_meat'):
        update_dict['set__is_meat'] = True
    if ingredient.get('is_gluten'):
        update_dict['set__is_gluten'] = True
    if len(update_dict.keys()):
        Ingredient.objects.filter(pk=ObjectId(request.POST.get('ingredientId'))).update(**update_dict)
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



"""
Dashboard Backend
"""

def backend_dashboard(request):
    '''
    '''
    menus = Menu.objects.count()
    ingredients = Ingredient.objects.count()
    if request.GET.get('from_date') and request.GET.get('to_date'):
        to_dt = datetime.strptime(request.GET.get('to_date'), "%Y-%m-%d") + timedelta(days=1)
        from_dt = datetime.strptime(request.GET.get('from_date'), "%Y-%m-%d")
        total_signups_today = User.objects.filter(date_joined__gte=from_dt,
                                                  date_joined__lte=to_dt).count()
        total_logins_today = User.objects.filter(date_joined__gte=from_dt,
                                                  date_joined__lte=to_dt).count()
    else:
        todaydt = datetime.now() - timedelta(hours=datetime.now().hour,
                                             minutes=datetime.now().minute,
                                             seconds=datetime.now().second)
        total_signups_today = User.objects.filter(date_joined__gte=todaydt, ).count()
        total_logins_today = User.objects.filter(last_login__gte=todaydt).count()

    number_of_visitors = 0
    return render(request, 'backend_dashboard.html', locals())


"""
Stripe
"""

stripe.api_key = settings.STRIPE_SECRET_KEY


def stripe_card_token(request):
    stripe_token = request.POST.get('id')
    stripe_coupon = request.POST.get('coupon')
    stripe_customer = stripe.Customer.create(description="Customer for %s" % request.user.email, source=stripe_token)
    stripe_subscription = stripe_customer.subscriptions.create(plan=settings.FTM_STRIPE_PLAN_DEFAULT, coupon=stripe_coupon)
    Payment.objects.create(user=request.user, cust_id=stripe_customer.id,
                            token=stripe_token, added_on=datetime.now(),
                            plan=settings.FTM_STRIPE_PLAN_DEFAULT, coupon=stripe_coupon,
                            expiry=datetime.fromtimestamp(stripe_subscription.current_period_end))
    return HttpResponse(json.dumps({'success': True}))
