from django.contrib.auth.models import User
from django.db.models import QuerySet

from blog.domain.entities.like import Like
from blog.domain.entities.profile import Profile


class LikeRepository:
    def get_by_id(self, like_id) -> Like:
        return Like.objects.get(id=like_id)

    def get_all(self) -> QuerySet:
        return Like.objects.all()

    def order_by(self, order: str) -> QuerySet:
        return Like.objects.order_by(order)

    def create(self, author: Profile, body: str) -> Like:
        like = Like(author=author, body=body)

        return self.save_like(like)

    def update(self, like_id: int, body):
        like = self.get_by_id(like_id)
        like.body = body

        return self.save_like(like)

    def delete(self, like_id: int) -> None:
        like = self.get_by_id(like_id)
        like.delete()

    def save_like(self, like: Like) -> Like:
        like.save()
        return like

    def get_count(self, post_id: int) -> int:
        return Like.objects.filter(post_id=post_id).count()

    def get_count_by_author(self, author_id: int) -> int:
        return Like.objects.filter(author_id=author_id).count()

    def did_user_like(self, user: User, post_id) -> bool:
        return True if Like.objects.filter(post_id=post_id, author=user.id) else False
