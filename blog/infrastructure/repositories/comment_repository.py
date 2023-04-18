from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.domain.entities.comment import Comment
from blog.domain.entities.post import Post
from blog.domain.entities.profile import Profile
from blog.domain.repository.comment_repository import ICommentRepository


class CommentRepository(ICommentRepository):

    @staticmethod
    @receiver(post_save, sender=Comment)
    def create(sender, instance, created, **kwargs) -> Comment | None:
        if not created:
            return None

        return Comment.objects.create(
            author=instance.author,
            title=instance.title,
            image_type=instance.image_type,
            image=instance.image,
            short=instance.short,
            body=instance.body
        )

    @staticmethod
    @receiver(post_save, sender=Comment)
    def save(sender, instance, **kwargs) -> None:
        instance.save()

    @staticmethod
    @receiver(post_save, sender=Comment)
    def delete(sender, instance, **kwargs) -> None:
        instance.delete()

    def get_by_id(self, comment_id) -> Comment:
        return Comment.objects.get(id=comment_id)

    def get_all(self) -> QuerySet:
        return Comment.objects.all()

    def order_by(self, order: str) -> QuerySet:
        return self.get_all().order_by(order)

    def get_count(self, post_id: int) -> int:
        return self.get_all().count()

    def get_all_by_author(self, user_id: int) -> QuerySet:
        return Comment.objects.filter(author=user_id)

    def get_all_by_post(self, post_id: int) -> QuerySet:
        return Comment.objects.filter(post=post_id)

    def get_count_by_author(self, user_id: int) -> int:
        return self.get_all_by_author(user_id=user_id).count()

    def get_count_by_post(self, post_id: int) -> int:
        return self.get_all_by_post(post_id=post_id).count()
