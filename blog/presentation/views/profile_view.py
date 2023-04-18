from itertools import chain

from django.shortcuts import render

from blog.application.comment_service import CommentService

from blog.application.post_service import PostService
from blog.application.forms.profile_form_service import UpdateProfileInfoForm, UpdateProfilePictureForm
from blog.application.profile_service import ProfileService
from blog.application.forms.user_form_service import UpdateUserForm

from blog.domain.repository.tag_repository import TagRepository


class ProfileView:
    comment_service = CommentService()
    post_service = PostService()
    profile_service = ProfileService()
    tag_repo = TagRepository()

    @classmethod
    def user_profile(cls, request, user_name, activity_type='all'):
        if request.method == 'POST' and request.user.username == user_name:
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileInfoForm(request.POST, request.FILES, instance=request.user.profile)
            profile_picture_form = UpdateProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)

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

        profile = cls.profile_service.get_profile_by_username(user_name, beautify=True)
        tags = cls.tag_repo.get_all()

        comments = posts = []
        if activity_type in ['all', 'posts']:
            posts = cls.post_service.get_post_by_user(user=profile.user, order_by='-date', beautify=True)

        if activity_type in ['all', 'comments']:
            comments = cls.comment_service.get_comments_by_user(user=profile.user, order_by='-date', beautify=True)

        profile.user.history = list(chain(posts, comments))

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
            'profile': profile.user,
            'tags': tags,
            'user_form': user_form,
            'profile_form': profile_form,
            'profile_picture_form': profile_picture_form,
            'filters': filters,
        }

        return render(request, 'blog/userprofile.html', context)
