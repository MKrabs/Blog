from django.contrib.auth.models import User
from django.db.models import QuerySet

from blog.domain.entities.like import Like
from blog.infrastructure.repositories.like_repository import LikeRepository
from blog.infrastructure.repositories.post_repository import PostRepository


class LikeService:

    like_repository = LikeRepository()
    post_repository = PostRepository()

    @classmethod
    def create_like(cls, post_id, author):
        post = cls.post_repository.get_by_id(post_id=post_id)
        return Like.objects.create(post=post, author=author)

    @classmethod
    def delete_like(cls, like_id):
        Like.objects.get(id=like_id).delete()

    @classmethod
    def did_user_like(cls, user_id: int, post_id: int) -> bool:
        return cls.like_repository.did_user_like(user_id=user_id, post_id=post_id)

    @classmethod
    def toggle_like(cls, post_id, author_id) -> None:
        if cls.did_user_like(user_id=author_id.id, post_id=post_id):
            like = cls.get_like_by_post_and_author(post_id=post_id, author_id=author_id)
            cls.delete_like(like_id=like.id)
        else:
            cls.create_like(post_id=post_id, author=author_id)

        return

    @classmethod
    def get_like_count_by_post_id(cls, post_id: int) -> int:
        return cls.like_repository.get_count_post(post_id=post_id)

    @classmethod
    def get_like_count_by_author(cls, author: User) -> int:
        return cls.like_repository.get_count_author(author_id=author.id)

    @classmethod
    def get_like_by_post_and_author(cls, post_id, author_id) -> Like:
        return cls.like_repository.get_like_by_post_and_author(post_id=post_id, author_id=author_id)
