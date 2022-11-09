from itertools import chain
from operator import attrgetter

import markdown
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

from blog.forms import CreateUserForm, UpdateUserForm, UpdateProfileInfoForm, UpdateProfilePictureForm
import bleach
from .models import Post, Tag, Comment, Like


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
    latest_posts = Post.objects.order_by('-date')

    for p in latest_posts:
        p.comments = Comment.objects.filter(post_id=p.id).count()
        p.likes = Like.objects.filter(post_id=p.id).count()
        p.liked = True if Like.objects.filter(post_id=p.id, author=request.user.id) else False

    p = Paginator(latest_posts, 4)

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
    }

    return render(request, 'blog/index.html', context)


def post(request, post_id):
    blog_post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post_id=post_id).order_by('-date')

    blog_post.likes = Like.objects.filter(post_id=blog_post.id).count()
    blog_post.liked = True if Like.objects.filter(post_id=blog_post.id, author=request.user.id) else False

    blog_post.body = marker(blog_post.body)

    for c in comments:
        c.body = marker(c.body)

    context = {
        'post': blog_post,
        'comments': comments,
    }

    return render(request, 'blog/post.html', context)


def create_post(request):
    return HttpResponse("You're looking to create a new post.")


def page_not_found(request, pattern):
    context = {'broken': pattern}
    return render(request, 'blog/404.html', context)


def marker(text):
    return markdown.markdown(
        bleacher(text),
        extensions=['tables']
    )


def bleacher(text):
    return bleach.clean(
        text,
        tags=['b', 'img', 'iframe'],
        attributes=['class', 'href', 'src', 'style', 'width', 'height']
    )


def liked(request, post_id):
    if request.user.is_authenticated:
        p = Post.objects.get(id=post_id)
        like = Like.objects.filter(author=request.user, post_id=p)
        if like.count() < 1:
            Like(author=request.user, post_id=p).save()
        else:
            like.delete()

    return redirect('post', post_id)


def comment(request, post_id):
    if request.method == 'POST' and len(request.POST['commentBody']) > 0:
        comm = Comment()
        comm.author = request.user if request.user.is_authenticated and not request.POST.get('anonymous') else None
        comm.post_id = Post.objects.get(id=post_id)
        comm.body = request.POST['commentBody']
        comm.save()
        messages.success(request, f'Comment "{comm.body[:10]}..." was posted.')
    else:
        messages.warning(request, 'Warning: Message can not be empty.')

    return redirect(reverse('post', kwargs={'post_id': post_id}) + '#comments')


def comment_delete(request, post_id, comm_id):
    if request.method == 'POST' and request.user.is_authenticated:
        comm = Comment.objects.get(id=comm_id)
        if request.user == comm.author:
            comm.delete()
            messages.info(request, f'Comment "{comm.body[:10]}..." was deleted.')
    else:
        messages.error(request, f'Comment n°{comm_id} could not be deleted.')

    return redirect(reverse('post', kwargs={'post_id': post_id}) + '#comments')


def user_profile(request, user_name):
    if request.method == 'POST' and request.user.username == user_name:
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileInfoForm(request.POST, request.FILES, instance=request.user.profile)
        profile_picture_form = UpdateProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)

        print(user_form.is_valid())
        print(profile_form.is_valid())
        print(profile_picture_form.is_valid())

        if user_form.is_valid():
            user_form.save()

        if profile_form.is_valid():
            profile_form.save()

        if profile_picture_form.is_valid():
            profile_picture_form.save()

    else:
        user_form = UpdateUserForm()
        profile_form = UpdateProfileInfoForm()
        profile_picture_form = UpdateProfilePictureForm()

    profile = User.objects.get(username=user_name)
    profile.profile.bio = marker(profile.profile.bio)
    tags = Tag.objects.all()

    posts = Post.objects.filter(author=profile).order_by('-date')
    comments = Comment.objects.filter(author=profile).order_by('-date')

    for c in comments:
        c.body = marker(c.body)

    for c in posts:
        c.body = marker(c.body)

    profile.history = list(chain(posts, comments))

    context = {
        'profile': profile,
        'tags': tags,
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_picture_form': profile_picture_form,
    }
    return render(request, 'blog/userprofile.html', context)
