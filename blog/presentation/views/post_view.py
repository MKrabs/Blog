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
    def delete_post(cls, request, post_id):
        return HttpResponse("You're looking to delete post %s." % post_id)

