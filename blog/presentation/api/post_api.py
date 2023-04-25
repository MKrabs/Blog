import json

from django.http import HttpResponse
from blog.application.post_service import PostService
from blog.infrastructure.serializers.post_serializer import PostSerializer


class PostAPI():
    post_service = PostService()

    @classmethod
    def get_latest_posts(cls, request):
        page = request.GET.get('page', 1)
        post_per_page = request.GET.get('post_per_page', 10)

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

        return HttpResponse(json.dumps(context))

    @classmethod
    def get_post(cls, request, post_id):
        post = cls.post_service.get_post_by_id(post_id=post_id, beautify=True)
        post = PostSerializer.serialize(post)

        context = {
            'post': post,
        }

        return json.dumps(context)

    @classmethod
    def get_user_profile(cls, request, user_name):
        user = cls.post_service.get_user_profile(user_name=user_name)
        user = PostSerializer.serialize(user)

        context = {
            'user': user,
        }

        return json.dumps(context)
