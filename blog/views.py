from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.forms import UserCreationForm
from blog.forms import CreateUserForm

from .models import Post, Tag


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success!')
            return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'registration/register.html', context)


def index(request, page=1):
    tags = Tag.objects.all()
    latest_posts = Post.objects.order_by('-pub_date')
    p = Paginator(latest_posts, 3)

    try:
        page_obj = p.get_page(page)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    context = {
        'page': {
            'current': page_obj.number,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'total': p.num_pages,
        },
        'latest_posts': page_obj.object_list,
        'tags': tags,
    }

    return render(request, 'blog/index.html', context)


def post(request, post_id):
    post = Post.objects.get(post_id)

    context = {
        'page': {
            'current': page_obj.number,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'total': p.num_pages,
        },
        'latest_posts': page_obj.object_list,
        'tags': tags,
    }

    return render(request, 'blog/index.html', context)


def create_post(request):
    return HttpResponse("You're looking to create a new post.")
