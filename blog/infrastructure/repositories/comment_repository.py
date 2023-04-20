from profanity import profanity
from django.db.models import QuerySet
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from blog.domain.entities.comment import Comment
from blog.domain.repository.comment_repository import ICommentRepository
from blog.infrastructure.repositories.post_repository import PostRepository


class CommentRepository(ICommentRepository):

    @staticmethod
    @receiver(post_save, sender=Comment)
    def create(sender, instance, created, **kwargs) -> Comment | None:
        if created:
            return None

        return Comment.objects.create(
            author=instance.author,
            post=instance.post,
            body=instance.body
        )

    @staticmethod
    @receiver(pre_save, sender=Comment)
    def save(sender, instance, **kwargs) -> None:
        if profanity.contains_profanity(instance.body):
            instance.body = profanity.censor(instance.body)

    @staticmethod
    @receiver(post_save, sender=Comment)
    def delete(sender, instance, **kwargs) -> None:
        pass

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
        post = PostRepository().get_by_id(post_id=post_id)
        return Comment.objects.filter(post_id=post.id)

    def get_count_by_author(self, user_id: int) -> int:
        return self.get_all_by_author(user_id=user_id).count()

    def get_count_by_post(self, post_id: int) -> int:
        app = self.get_all_by_post(post_id=post_id)
        return app.count()
