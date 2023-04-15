from django.contrib.auth.models import User
from django.db.models import QuerySet

from blog.domain.entities.post import Post
from blog.domain.entities.profile import Profile
from blog.domain.repository.comment_repository import CommentRepository
from blog.domain.repository.like_repository import LikeRepository


class PostRepository:
    def __init__(self):
        self.likes_repo = LikeRepository()
        self.comments_repo = CommentRepository()

    def get_by_id(self, post_id) -> Post:
        return Post.objects.get(id=post_id)

    def get_by_author(self, author: User, order_by: str = None) -> QuerySet:
        return Post.objects.filter(author=author).order_by(order_by)

    def get_all(self, order_by: str = None) -> QuerySet:
        return Post.objects.all().order_by(order_by)

    def create(self, author: User, title: str, short: str, body: str, image_type: str = None, image: str = None) \
            -> Post:
        post = Post(author=author, title=title, image_type=image_type, image=image, short=short, body=body)
        self.save_post(post)
        return post

    def update(self, post_id: int, title=None, image_type=None, image=None, short=None, body=None):
        post = self.get_by_id(post_id)
        if title:
            post.title = title
        if image_type:
            post.image_type = image_type
        if image:
            post.image = image
        if short:
            post.short = short
        if body:
            post.body = body
        self.save_post(post)
        return post

    def delete(self, post_id: int) -> None:
        post = self.get_by_id(post_id)
        post.delete()

    def save_post(self, post: Post) -> Post:
        post.save()
        return post

    def get_count(self, post_id: int) -> int:
        return Post.objects.get(id=post_id).comments.count()

    def get_count_by_author(self, author_id: int) -> int:
        return Post.objects.filter(author_id=author_id).count()

    def add_additional_fields(self, post: Post, user: User) -> None:
        post.comments = self.comments_repo.get_count(post.id)
        post.likes = self.likes_repo.get_count(post.id)
        post.liked = self.likes_repo.did_user_like(user, post.id)
