import json
from django.shortcuts import render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from bson.objectid import ObjectId
from mongoengine.django.auth import User
from menu.models import Payment, Establishment, Menu, Dish, Ingredient

# user admin views
@login_required(login_url=reverse_lazy('menu-login'))
def admin_user(request):
    # if not request.user.is_superuser:
    #     raise Http404
    users = User.objects.all()
    paginator = Paginator(users, 10)

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
    # if not request.user.is_superuser:
    #     raise Http404
    user = User.objects.get(pk=ObjectId(id))
    try:
        payment = Payment.objects.get(user=user)
    except Payment.DoesNotExist:
        payment = None
    menu_count = Menu.objects.filter(establishment__in=Establishment.objects.filter(user=request.user)).count()
    return render(request, 'user_detail.html', {'user': user, 'payment': payment, 'menu_count': menu_count})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_user_detail_update(request, id):
    # if not request.user.is_superuser:
    #     raise Http404
    update_dict = {}
    if request.POST.get('name') == 'email':
        update_dict['set__email'] = request.POST.get('value')
    if request.POST.get('name') == 'superuser':
        update_dict['set__is_superuser'] = True if request.POST.get('value') == 'true' else False
    if len(update_dict.keys()):
        User.objects.filter(pk=ObjectId(id)).update(**update_dict)
    return HttpResponse(json.dumps({'status': True}))


# dish admin views
@login_required(login_url=reverse_lazy('menu-login'))
def admin_dish(request):
    if not request.user.is_superuser:
        raise Http404
    dishes = Dish.objects.all()
    paginator = Paginator(dishes, 10)

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


# ingredient admin views
@login_required(login_url=reverse_lazy('menu-login'))
def admin_ingredient(request):
    if not request.user.is_superuser:
        raise Http404
    ingredients = Ingredient.objects.all()
    paginator = Paginator(ingredients, 10)

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
    if len(update_dict.keys()):
        Ingredient.objects.filter(pk=ObjectId(id)).update(**update_dict)
    return HttpResponse(json.dumps({'status': True}))


@login_required(login_url=reverse_lazy('menu-login'))
def admin_ingredient_detail_delete(request, id):
    if not request.user.is_superuser:
        raise Http404
    Ingredient.objects.filter(pk=ObjectId(id)).delete()
    return HttpResponseRedirect(reverse_lazy('menu_admin_ingredient'))
