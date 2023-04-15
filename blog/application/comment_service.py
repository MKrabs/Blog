from django.core.paginator import Paginator, EmptyPage

from blog.domain.entities.comment import Comment
from blog.domain.entities.like import Like
from blog.domain.entities.post import Post


class CommentService:
    @classmethod
    def get_comments_by_post_id(cls, post_id):
        return Comment.objects.filter(post_id=post_id).order_by('-date')

    @classmethod
    def get_comment_by_id(cls, comment_id):
        return Comment.objects.get(id=comment_id)

    @classmethod
    def create_comment(cls, post_id, author, body):
        return Comment.objects.create(post_id=post_id, author=author, body=body)

    @classmethod
    def delete_comment(cls, comment_id):
        Comment.objects.get(id=comment_id).delete()

    @classmethod
    def add_additional_fields(cls, comment):
        if comment.author:
            comment.author.total_posts = Post.objects.filter(author=comment.author).count()
            comment.author.total_comments = Comment.objects.filter(author=comment.author).count()
            comment.author.total_likes = Like.objects.filter(author=comment.author).count()

    @classmethod
    def paginate_posts(cls, comments, param: int = 4, page: int = 1) -> (Paginator, int):
        p = Paginator(comments, param)

        try:
            page_obj = p.get_page(page)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        return page_obj, p.num_pages
