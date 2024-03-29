from django.http import HttpResponse
from django.shortcuts import render

from blog.application.comment_service import CommentService
from blog.application.post_service import PostService
from blog.application.profile_service import ProfileService


class PostView:

    post_service = PostService()
    comment_service = CommentService()
    profile_service = ProfileService()

    @classmethod
    def post(cls, request, post_id, page=1, beautify=True):
        blog_post = cls.post_service.get_post_by_id(post_id=post_id, beautify=beautify)
        cls.post_service.add_additional_fields(entity=blog_post)

        comments = cls.comment_service.get_comments_by_post_id(post_id=post_id, beautify=beautify)
        p, num_pages = CommentService.paginate_posts(comments, param=5, page=page)
        comments = p.object_list

        context = {
            'post': blog_post,
            'comments': comments,
            'page': {
                'current': p.number,
                'total': num_pages,
            },
        }

        return render(request, 'blog/post.html', context)

    @classmethod
    def create_post(cls, request):
        return HttpResponse("You're looking to create a new post.")

    @classmethod
    def delete_post(cls, request, post_id):
        return HttpResponse("You're looking to delete post %s." % post_id)

