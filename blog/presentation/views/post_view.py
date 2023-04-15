from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

from abstraction.markdown_processor import MarkdownProcessor as mp
from blog.application.post_service import PostService
from blog.application.profile_service import ProfileService

from blog.domain.entities.comment import Comment
from blog.domain.entities.like import Like
from blog.domain.entities.post import Post
from blog.application.comment_service import CommentService


class PostView:

    post_service = PostService()
    comment_service = CommentService()
    profile_service = ProfileService()

    @classmethod
    def post(cls, request, post_id, page=1):
        blog_post = cls.post_service.get_post_by_id(post_id=post_id)
        comments = cls.comment_service.get_comments_by_post_id(post_id=post_id)

        for comment in comments:
            # add additional fields to comment
            cls.profile_service.add_additional_fields(entity=comment)

        cls.post_service.add_additional_fields(entity=blog_post, user=request.user)

        blog_post.body = mp.marker(blog_post.body)
        p, num_pages = CommentService.paginate_posts(comments, param=5, page=page)
        comments = p.object_list

        for comment in comments:
            comment.body = mp.marker(comment.body)
            cls.comment_service.add_additional_fields(comment)

        context = {
            'post': blog_post,
            'comments': comments,
            'page': {
                'current': p.number,
                'has_next': p.has_next(),
                'has_previous': p.has_previous(),
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

