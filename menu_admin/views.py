from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from bson.objectid import ObjectId
from mongoengine.django.auth import User


@login_required(login_url=reverse_lazy('menu-login'))
def admin_user(request):
    if not request.user.is_superuser:
        raise Http404
    users = User.objects.all()
    paginator = Paginator(users, 5)

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
    return render(request, 'user_detail.html', {'user': user})
