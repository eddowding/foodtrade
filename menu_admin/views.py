import json
from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from bson.objectid import ObjectId
from mongoengine.django.auth import User
from menu.models import Payment, Establishment, Menu, Dish, Ingredient, ModerationIngredient, Meat, Allergen, Gluten

# user admin views


@login_required(login_url=reverse_lazy('menu-login'))
def admin_user(request):
    if not request.user.is_superuser:
        raise Http404
    if request.GET.get('query'):
        users = User.objects.filter(username__icontains=request.GET.get('query'))
    else:
        users = User.objects.all()
    paginator = Paginator(users, settings.ADMIN_LISTING_LIMIT)

    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'user.html', {'users': users})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_user_detail(request, id):
    if not request.user.is_superuser:
        raise Http404
    user = User.objects.get(pk=ObjectId(id))
    try:
        payment = Payment.objects.get(user=user)
    except Payment.DoesNotExist:
        payment = None
    menu_count = Menu.objects.filter(establishment__in=Establishment.objects.filter(user=request.user)).count()
    return render(request, 'user_detail.html', {'user': user, 'payment': payment, 'menu_count': menu_count})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_user_detail_update(request, id):
    if not request.user.is_superuser:
        raise Http404
    update_dict = {}
    if request.POST.get('name') == 'email':
        update_dict['set__email'] = request.POST.get('value')
    if request.POST.get('name') == 'superuser':
        update_dict['set__is_superuser'] = True if request.POST.get('value') == 'true' else False
    if len(update_dict.keys()):
        User.objects.filter(pk=ObjectId(id)).update(**update_dict)
    return HttpResponse(json.dumps({'status': True}))


@login_required(login_url=reverse_lazy('menu-login'))
def admin_user_delete(request, id):
    if not request.user.is_superuser:
        raise Http404
    User.objects.filter(pk=ObjectId(id)).delete()
    return HttpResponseRedirect(reverse_lazy('menu_admin_user'))


# dish admin views
@login_required(login_url=reverse_lazy('menu-login'))
def admin_dish(request):
    if not request.user.is_superuser:
        raise Http404
    if request.GET.get('query'):
        dishes = Dish.objects.filter(name__icontains=request.GET.get('query'))
    else:
        dishes = Dish.objects.all()
    paginator = Paginator(dishes, settings.ADMIN_LISTING_LIMIT)

    page = request.GET.get('page')
    try:
        dishes = paginator.page(page)
    except PageNotAnInteger:
        dishes = paginator.page(1)
    except EmptyPage:
        dishes = paginator.page(paginator.num_pages)

    return render(request, 'dish.html', {'dishes': dishes})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_dish_detail(request, id):
    if not request.user.is_superuser:
        raise Http404
    dish = Dish.objects.get(pk=ObjectId(id))
    return render(request, 'dish_detail.html', {'dish': dish})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_dish_detail_update(request, id):
    if not request.user.is_superuser:
        raise Http404
    update_dict = {}
    if request.POST.get('name') == 'name':
        update_dict['set__name'] = request.POST.get('value')
    if request.POST.get('name') == 'public':
        update_dict['set__is_public'] = True if request.POST.get('value') == 'true' else False
    if len(update_dict.keys()):
        Dish.objects.filter(pk=ObjectId(id)).update(**update_dict)
    return HttpResponse(json.dumps({'status': True}))


@login_required(login_url=reverse_lazy('menu-login'))
def admin_dish_delete(request, id):
    if not request.user.is_superuser:
        raise Http404
    Dish.objects.filter(pk=ObjectId(id)).delete()
    return HttpResponseRedirect(reverse_lazy('menu_admin_dish'))


# ingredient admin views
@login_required(login_url=reverse_lazy('menu-login'))
def admin_ingredient(request):
    if not request.user.is_superuser:
        raise Http404
    if request.GET.get('query'):
        ingredients = Ingredient.objects.filter(name__icontains=request.GET.get('query'))
    else:
        ingredients = Ingredient.objects.all()
    paginator = Paginator(ingredients, settings.ADMIN_LISTING_LIMIT)

    page = request.GET.get('page')
    try:
        ingredients = paginator.page(page)
    except PageNotAnInteger:
        ingredients = paginator.page(1)
    except EmptyPage:
        ingredients = paginator.page(paginator.num_pages)

    return render(request, 'ingredient.html', {'ingredients': ingredients})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_ingredient_detail(request, id):
    if not request.user.is_superuser:
        raise Http404
    ingredient = Ingredient.objects.get(pk=ObjectId(id))
    return render(request, 'ingredient_detail.html', {'ingredient': ingredient})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_ingredient_detail_update(request, id):
    if not request.user.is_superuser:
        raise Http404
    update_dict = {}
    if request.POST.get('name') == 'ingredient_name':
        update_dict['set__name'] = request.POST.get('value')
    if request.POST.get('name') == 'is_in_ac':
        update_dict['set__is_in_ac'] = True if request.POST.get('value') == 'true' else False
    if len(update_dict.keys()):
        Ingredient.objects.filter(pk=ObjectId(id)).update(**update_dict)
    return HttpResponse(json.dumps({'status': True}))


@login_required(login_url=reverse_lazy('menu-login'))
def admin_ingredient_detail_delete(request, id):
    if not request.user.is_superuser:
        raise Http404
    Ingredient.objects.filter(pk=ObjectId(id)).delete()
    return HttpResponseRedirect(reverse_lazy('menu_admin_ingredient'))

# establishment admin views


@login_required(login_url=reverse_lazy('menu-login'))
def admin_establishment(request):
    if not request.user.is_superuser:
        raise Http404
    if request.GET.get('query'):
        establishments = Establishment.objects.filter(BusinessName__icontains=request.GET.get('query'))
    else:
        establishments = Establishment.objects.all()
    paginator = Paginator(establishments, settings.ADMIN_LISTING_LIMIT)

    page = request.GET.get('page')
    try:
        establishments = paginator.page(page)
    except PageNotAnInteger:
        establishments = paginator.page(1)
    except EmptyPage:
        establishments = paginator.page(paginator.num_pages)

    return render(request, 'establishment.html', {'establishments': establishments})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_establishment_detail(request, id):
    if not request.user.is_superuser:
        raise Http404
    establishment = Establishment.objects.get(pk=ObjectId(id))
    users = User.objects.all()
    return render(request, 'establishment_detail.html', {'establishment': establishment, 'users': users})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_establishment_detail_update(request, id):
    if not request.user.is_superuser:
        raise Http404
    update_dict = {}
    if request.POST.get('name') == 'user':
        update_dict['set__user'] = ObjectId(request.POST.get('value'))
    if len(update_dict.keys()):
        Establishment.objects.filter(pk=ObjectId(id)).update(**update_dict)
    return HttpResponse(json.dumps({'status': True}))


@login_required(login_url=reverse_lazy('menu-login'))
def admin_establishment_delete(request, id):
    if not request.user.is_superuser:
        raise Http404
    Establishment.objects.filter(pk=ObjectId(id)).delete()
    return HttpResponseRedirect(reverse_lazy('menu_admin_establishment'))


# meat admin views
@login_required(login_url=reverse_lazy('menu-login'))
def admin_meat(request):
    if not request.user.is_superuser:
        raise Http404
    if request.GET.get('query'):
        meats = Meat.objects.filter(name__icontains=request.GET.get('query'))
    else:
        meats = Meat.objects.all()
    paginator = Paginator(meats, settings.ADMIN_LISTING_LIMIT)

    page = request.GET.get('page')
    try:
        meats = paginator.page(page)
    except PageNotAnInteger:
        meats = paginator.page(1)
    except EmptyPage:
        meats = paginator.page(paginator.num_pages)

    return render(request, 'meat.html', {'meats': meats})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_meat_detail(request, id):
    if not request.user.is_superuser:
        raise Http404
    meat = Meat.objects.get(pk=ObjectId(id))
    return render(request, 'meat_detail.html', {'meat': meat})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_meat_delete(request, id):
    if not request.user.is_superuser:
        raise Http404
    Meat.objects.filter(pk=ObjectId(id)).delete()
    return HttpResponseRedirect(reverse_lazy('menu_admin_meat'))


@login_required(login_url=reverse_lazy('menu-login'))
def admin_meat_detail_update(request, id):
    if not request.user.is_superuser:
        raise Http404
    update_dict = {}
    if request.POST.get('name') == 'name':
        update_dict['set__name'] = request.POST.get('value')
    if len(update_dict.keys()):
        Meat.objects.filter(pk=ObjectId(id)).update(**update_dict)
    return HttpResponse(json.dumps({'status': True}))


# Allergen admin views
@login_required(login_url=reverse_lazy('menu-login'))
def admin_allergen(request):
    if not request.user.is_superuser:
        raise Http404
    if request.GET.get('query'):
        allergens = Allergen.objects.filter(name__icontains=request.GET.get('query'))
    else:
        allergens = Allergen.objects.all()
    paginator = Paginator(allergens, settings.ADMIN_LISTING_LIMIT)

    page = request.GET.get('page')
    try:
        allergens = paginator.page(page)
    except PageNotAnInteger:
        allergens = paginator.page(1)
    except EmptyPage:
        allergens = paginator.page(paginator.num_pages)

    return render(request, 'allergen.html', {'allergens': allergens})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_allergen_detail(request, id):
    if not request.user.is_superuser:
        raise Http404
    allergen = Allergen.objects.get(pk=ObjectId(id))
    return render(request, 'allergen_detail.html', {'allergen': allergen})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_allergen_delete(request, id):
    if not request.user.is_superuser:
        raise Http404
    Allergen.objects.filter(pk=ObjectId(id)).delete()
    return HttpResponseRedirect(reverse_lazy('menu_admin_allergen'))


@login_required(login_url=reverse_lazy('menu-login'))
def admin_allergen_detail_update(request, id):
    if not request.user.is_superuser:
        raise Http404
    update_dict = {}
    if request.POST.get('name') == 'name':
        update_dict['set__name'] = request.POST.get('value')
    if len(update_dict.keys()):
        Allergen.objects.filter(pk=ObjectId(id)).update(**update_dict)
    return HttpResponse(json.dumps({'status': True}))


# Gluten admin views
@login_required(login_url=reverse_lazy('menu-login'))
def admin_gluten(request):
    if not request.user.is_superuser:
        raise Http404
    if request.GET.get('query'):
        glutens = Gluten.objects.filter(name__icontains=request.GET.get('query'))
    else:
        glutens = Gluten.objects.all()
    paginator = Paginator(glutens, settings.ADMIN_LISTING_LIMIT)

    page = request.GET.get('page')
    try:
        glutens = paginator.page(page)
    except PageNotAnInteger:
        glutens = paginator.page(1)
    except EmptyPage:
        glutens = paginator.page(paginator.num_pages)

    return render(request, 'gluten.html', {'glutens': glutens})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_gluten_detail(request, id):
    if not request.user.is_superuser:
        raise Http404
    gluten = Gluten.objects.get(pk=ObjectId(id))
    return render(request, 'gluten_detail.html', {'gluten': gluten})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_gluten_delete(request, id):
    if not request.user.is_superuser:
        raise Http404
    Gluten.objects.filter(pk=ObjectId(id)).delete()
    return HttpResponseRedirect(reverse_lazy('menu_admin_gluten'))


@login_required(login_url=reverse_lazy('menu-login'))
def admin_gluten_detail_update(request, id):
    if not request.user.is_superuser:
        raise Http404
    update_dict = {}
    if request.POST.get('name') == 'name':
        update_dict['set__name'] = request.POST.get('value')
    if len(update_dict.keys()):
        Gluten.objects.filter(pk=ObjectId(id)).update(**update_dict)
    return HttpResponse(json.dumps({'status': True}))


@login_required(login_url=reverse_lazy('menu-login'))
def admin_bulk_delete(request, type):
    ids = []
    type = int(type)
    for id in request.POST.getlist('ids[]'):
        ids.append(ObjectId(id))
    if type == 1:
        Ingredient.objects.filter(pk__in=ids).delete()
    if type == 2:
        Dish.objects.filter(pk__in=ids).delete()
    if type == 3:
        ModerationIngredient.objects.filter(pk__in=ids).delete()
    if type == 4:
        Meat.objects.filter(pk__in=ids).delete()
    if type == 5:
        Allergen.objects.filter(pk__in=ids).delete()
    if type == 6:
        Gluten.objects.filter(pk__in=ids).delete()
    return HttpResponse(json.dumps({'status': True}))
