from django.http import JsonResponse

from blog.application.comment_service import CommentService
from blog.application.post_service import PostService
from blog.application.profile_service import ProfileService
from blog.infrastructure.serializers.comment_serializer import CommentSerializer
from blog.infrastructure.serializers.post_serializer import PostSerializer
from blog.infrastructure.serializers.profile_serializer import ProfileSerializer


class PostAPI():
    post_service = PostService()
    profile_service = ProfileService()
    comment_service = CommentService()

    @classmethod
    def get_latest_posts(cls, request):
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
        profile = cls.profile_service.get_profile_by_username(user_name=user_name)
        posts = cls.post_service.get_post_by_user(profile.user)
        comments = cls.comment_service.get_comments_by_user(profile.user)

        profile = ProfileSerializer.serialize(profile)
        posts = PostSerializer.serialize(posts)
        comments = CommentSerializer.serialize(comments)

        context = {
            'user': profile,
            'posts': posts,
            'comments': comments,
        }

        return JsonResponse(context)


def get_param(request, param_name, default_value):
    try:
        param = int(request.GET.get(param_name))
    except:
        param = default_value

    return param
