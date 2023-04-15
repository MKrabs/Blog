from itertools import chain

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from blog.application.post_service import PostService
from blog.application.profile_form_service import UpdateProfileInfoForm, UpdateProfilePictureForm
from blog.application.user_form_service import CreateUserForm, UpdateUserForm
from blog.domain.entities.comment import Comment
from blog.domain.entities.like import Like
from blog.domain.entities.post import Post
from blog.domain.entities.tag import Tag
from abstraction.markdown_processor import MarkdownProcessor as mp


class ViewsService:
    post_service = PostService()

    @classmethod
    def index(cls, request, page=1):
        latest_posts = cls.post_service.get_latest_posts(order_by='-date')
        p, num_pages = PostService.paginate_posts(latest_posts, param=4, page=page)

        context = {
            'page': {
                'current': p.number,
                'has_next': p.has_next(),
                'has_previous': p.has_previous(),
                'total': num_pages,
            },
            'latest_posts': p.object_list,
        }

        return render(request, 'blog/index.html', context)

    @classmethod
    def post(cls, request, post_id, page=1):
        blog_post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post_id=post_id).order_by('-date')

        if blog_post.author:
            blog_post.author.total_posts = Post.objects.filter(author=blog_post.author).count()
            blog_post.author.total_comments = Comment.objects.filter(author=blog_post.author).count()
            blog_post.author.total_likes = Like.objects.filter(author=blog_post.author).count()

        blog_post.likes = Like.objects.filter(post_id=blog_post.id).count()
        blog_post.liked = True if Like.objects.filter(post_id=blog_post.id, author=request.user.id) else False

        blog_post.body = mp.marker(blog_post.body)

        p = Paginator(comments, 5)

        try:
            page_obj = p.get_page(page)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        comments = page_obj.object_list

        for c in comments:
            c.body = mp.marker(c.body)
            if c.author:
                c.author.profile.bio = mp.marker(c.author.profile.bio)
                c.author.total_posts = Post.objects.filter(author=c.author).count()
                c.author.total_comments = Comment.objects.filter(author=c.author).count()
                c.author.total_likes = Like.objects.filter(author=c.author).count()

        context = {
            'post': blog_post,
            'comments': comments,
            'page': {
                'current': page_obj.number,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
                'total': p.num_pages,
            },
        }

        return render(request, 'blog/post.html', context)

    @classmethod
    def create_post(cls, request):
        return HttpResponse("You're looking to create a new post.")

    @classmethod
    def page_not_found(cls, request, pattern):
        context = {'broken': pattern}
        return render(request, 'blog/404.html', context)

    @classmethod
    def liked(cls, request, post_id):
        if request.user.is_authenticated:
            p = Post.objects.get(id=post_id)
            like = Like.objects.filter(author=request.user, post_id=p)
            if like.count() < 1:
                Like(author=request.user, post_id=p).save()
            else:
                like.delete()

        return redirect('post', post_id)

    @classmethod
    def comment(cls, request, post_id):
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

    @classmethod
    def comment_delete(cls, request, post_id, comm_id):
        if request.method == 'POST' and request.user.is_authenticated:
            comm = Comment.objects.get(id=comm_id)
            if request.user == comm.author:
                comm.delete()
                messages.info(request, f'Comment "{comm.body[:10]}..." was deleted.')
        else:
            messages.error(request, f'Comment n°{comm_id} could not be deleted.')

        return redirect(reverse('post', kwargs={'post_id': post_id}) + '#comments')

    @classmethod
    def user_profile(cls, request, user_name, activity_type='all'):
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

            if profile_picture_form.is_valid() and not profile_picture_form.fields['picture']:
                profile_picture_form.save(True)

        elif request.user.username == user_name:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileInfoForm(instance=request.user.profile)
            profile_picture_form = UpdateProfilePictureForm(instance=request.user.profile)
        else:
            user_form = UpdateUserForm()
            profile_form = UpdateProfileInfoForm()
            profile_picture_form = UpdateProfilePictureForm()

        profile = User.objects.get(username=user_name)
        profile.profile.bio = mp.marker(profile.profile.bio)
        tags = Tag.objects.all()

        posts = Post.objects.none()
        comments = Comment.objects.none()

        if activity_type in ['all', 'posts']:
            posts = Post.objects.filter(author=profile).order_by('-date')
            for c in posts:
                c.body = mp.marker(c.body)

        if activity_type in ['all', 'comments']:
            comments = Comment.objects.filter(author=profile).order_by('-date')
            for c in comments:
                c.body = mp.marker(c.body)

        profile.history = list(chain(posts, comments))

        filters = [
            {
                'name': 'all',
                'icon': 'bi-stack'
            },
            {
                'name': 'posts',
                'icon': 'bi-journal'
            },
            {
                'name': 'comments',
                'icon': 'bi-chat-left'
            }
        ]

        context = {
            'profile': profile,
            'tags': tags,
            'user_form': user_form,
            'profile_form': profile_form,
            'profile_picture_form': profile_picture_form,
            'filters': filters,
        }
        return render(request, 'blog/userprofile.html', context)
