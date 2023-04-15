from django.db.models import QuerySet

from blog.domain.entities.comment import Comment
from blog.domain.entities.profile import Profile


class CommentRepository:
    def get_by_id(self, comment_id) -> Comment:
        return Comment.objects.get(id=comment_id)

    def get_all(self) -> QuerySet:
        return Comment.objects.all()

    def order_by(self, order: str) -> QuerySet:
        return Comment.objects.order_by(order)

    def create(self, author: Profile, body: str) -> Comment:
        comment = Comment(author=author, body=body)

        return self.save_comment(comment)

    def update(self, comment_id: int, body):
        comment = self.get_by_id(comment_id)
        comment.body = body

        return self.save_comment(comment)

    def delete(self, comment_id: int) -> None:
        comment = self.get_by_id(comment_id)
        comment.delete()

    def save_comment(self, comment: Comment) -> Comment:
        comment.save()
        return comment

    def get_count(self, post_id: int) -> int:
        return Comment.objects.filter(post_id=post_id).count()
