import markdown
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.forms import UserCreationForm
from blog.forms import CreateUserForm
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
    tags = Tag.objects.all()
    latest_posts = Post.objects.order_by('-pub_date')

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
        'tags': tags,
    }

    return render(request, 'blog/index.html', context)


def post(request, post_id):
    blog_post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post_id=post_id)

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
    if request.method == 'POST':
        comm = Comment()
        comm.author = request.user if request.user.is_authenticated and not request.POST.get('anonymous') else None
        comm.post_id = Post.objects.get(id=post_id)
        comm.body = request.POST['commentBody']
        comm.save()

    return redirect('post', post_id)


def comment_delete(request, post_id, comm_id):
    if request.method == 'POST' and request.user.is_authenticated:
        Comment.objects.get(id=comm_id).delete()
    return redirect('post', post_id)
