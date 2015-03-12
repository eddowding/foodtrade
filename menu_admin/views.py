import json
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from bson.objectid import ObjectId
from mongoengine.django.auth import User
from menu.models import Payment


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
    return render(request, 'user_detail.html', {'user': user, 'payment': payment})


@login_required(login_url=reverse_lazy('menu-login'))
def admin_user_detail_update(request, id):
    update_dict = {}
    if request.POST.get('name') == 'email':
        update_dict['set__email'] = request.POST.get('value')
    if request.POST.get('name') == 'superuser':
        update_dict['set__is_superuser'] = True if request.POST.get('value') == 'true' else False
    if len(update_dict.keys()):
        User.objects.filter(pk=ObjectId(id)).update(**update_dict)
    return HttpResponse(json.dumps({'status': True}))
