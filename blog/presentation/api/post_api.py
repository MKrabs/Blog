from django.http import JsonResponse

from blog.application.comment_service import CommentService
from blog.application.post_service import PostService
from blog.application.profile_service import ProfileService
from blog.domain.entities.post import Post
from blog.infrastructure.repositories.post_repository import PostRepository
from blog.infrastructure.serializers.comment_serializer import CommentSerializer
from blog.infrastructure.serializers.post_serializer import PostSerializer


class PostAPI:
    post_service = PostService()
    post_repository = PostRepository()
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
    def create_post(cls, request):
        if request.method != 'POST':
            return JsonResponse({
                'code': '405',
                'note': 'Only post through secure channel! POST or nothing.'
            })

        if request.user.is_authenticated:
            return JsonResponse({
                'code': '403',
                'note': 'User not permitted to post!'
            })

        try:
            post = Post(
                title=request.POST['post_title'],
                author_id=request.user.id,
                image_type=request.POST['post_image_type'],
                image=request.POST['post_image'],
                short=request.POST['post_short'],
                body=request.POST['post_body'],
            )

            post.save()

            return JsonResponse({
                'code': '201',
                'note': 'Post created.',
                'post': {
                    'id': post.id,
                    'title': post.title,
                },
            })

        except Exception:
            return JsonResponse({
                'code': 'FAILURE',
                'note': 'Something when wrong! Make sure to include the following types',
                'required': ["title", "short", "body"],
                'optional': ["image_type", "image"],
            })


def get_param(request, param_name, default_value):
    try:
        param = int(request.GET.get(param_name))
    except (TypeError, ValueError):
        param = default_value

    return param
