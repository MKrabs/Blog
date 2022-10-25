from tempfile import template

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Post, Tag


# Create your views here.
# https://docs.djangoproject.com/en/3.2/intro/tutorial03/


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def post(request, post_id):
    latest_posts = Post.objects.order_by('-pub_date')[:post_id]
    tags = Tag.objects.all()

    context = {
        'latest_posts': latest_posts,
        'tags': tags,
    }

    return render(request, 'blog/index.html', context)


def create_post(request):
    response = "You're looking to create a new post."
    return HttpResponse(response)
