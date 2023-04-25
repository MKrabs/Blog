from django.http import JsonResponse

from blog.application.comment_service import CommentService
from blog.application.post_service import PostService
from blog.application.profile_service import ProfileService
from blog.infrastructure.serializers.comment_serializer import CommentSerializer
from blog.infrastructure.serializers.post_serializer import PostSerializer
from blog.infrastructure.serializers.profile_serializer import ProfileSerializer


class ProfileAPI:
    comment_service = CommentService()
    post_service = PostService()
    profile_service = ProfileService()

    @classmethod
    def get_user_profile(cls, request, user_name):
        profile = cls.profile_service.get_profile_by_username(user_name=user_name)
        posts = cls.post_service.get_post_by_user(profile.user)
        comments = cls.comment_service.get_comments_by_user(profile.user)

        profile = ProfileSerializer.serialize(profile)
        posts = PostSerializer.serialize(posts)
        comments = CommentSerializer.serialize(comments)

        context = {
            'profile': profile,
            'posts': posts,
            'comments': comments,
        }

        return JsonResponse(context)
