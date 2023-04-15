from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

from abstraction.markdown_processor import MarkdownProcessor as mp
from blog.domain.entities.comment import Comment
from blog.domain.entities.like import Like
from blog.domain.entities.post import Post


class PostView:

    @classmethod
    def post(cls, request, post_id, page=1):
        blog_post = Post.objects.get(pk=post_id)
        comments = Comment.objects.filter(post_id=post_id).order_by('-date')

        if blog_post.author:
            blog_post.author.total_posts = Post.objects.filter(author=blog_post.author).count()
            blog_post.author.total_comments = Comment.objects.filter(author=blog_post.author).count()
            blog_post.author.total_likes = Like.objects.filter(author=blog_post.author).count()

        blog_post.likes = Like.objects.filter(post_id=blog_post.id).count()
        blog_post.liked = True if Like.objects.filter(post_id=blog_post.id, author=request.user.id) else False

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

