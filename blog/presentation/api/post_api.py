import json

from django.http import HttpResponse, JsonResponse

from blog.application.comment_service import CommentService
from blog.application.post_service import PostService
from blog.application.profile_service import ProfileService

from blog.infrastructure.serializers.post_serializer import PostSerializer
from blog.infrastructure.serializers.comment_serializer import CommentSerializer


class PostAPI():
    post_service = PostService()
    profile_service = ProfileService()
    comment_service = CommentService()

    @classmethod
    def get_latest_posts(cls, request):
        # Get the page and post_per_page from the request
        # If the page or post_per_page is not in the request or not an int, set the default value

        page = get_param(request, 'page', 1)
        post_per_page = get_param(request, 'post_per_page', 10)

        latest_posts = cls.post_service.get_latest_posts(user=request.user, order_by='-date', additional_fields=True)
        p, num_pages = cls.post_service.paginate_posts(latest_posts, param=post_per_page, page=page)

        posts = PostSerializer.serialize(p.object_list)

        context = {
            'page': {
                'current': p.number,
                'total': num_pages,
                },
            'latest_posts': posts,
        }

        return JsonResponse(context)

    @classmethod
    def get_post(cls, request, post_id):
        post = cls.post_service.get_post_by_id(post_id=post_id)
        post = PostSerializer.serialize([post])[0]

        comments = cls.comment_service.get_comments_by_post_id(post_id=post_id)
        comments = CommentSerializer.serialize(comments)

        context = {
            'post': post,
            'comments': comments,
        }

        return JsonResponse(context)

    @classmethod
    def get_user_profile(cls, request, user_name):
        user = cls.profile_service.get_profile_by_username(user_name=user_name)
        user = PostSerializer.serialize(user)

        posts = cls.post_service.get_posts_by_author_id(user.id)
        posts = PostSerializer.serialize(posts)

        comments = cls.comment_service.get_comments_by_author_id(user.id)
        comments = CommentSerializer.serialize(comments)

        context = {
            'user': user,
            'posts': posts,
            'comments': comments,
        }

        return JsonResponse(context)

def get_param(request, param_name, default_value):
    try:
        param = int(request.GET.get(param_name))
    except ValueError:
        param = default_value

    return param
