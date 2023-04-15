from itertools import chain

from django.contrib.auth.models import User
from django.shortcuts import render

from blog.application.profile_form_service import UpdateProfileInfoForm, UpdateProfilePictureForm
from blog.application.user_form_service import UpdateUserForm

from abstraction.markdown_processor import MarkdownProcessor as mp
from blog.domain.entities.comment import Comment
from blog.domain.entities.post import Post
from blog.domain.entities.tag import Tag


class ProfileView():
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