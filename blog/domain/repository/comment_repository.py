from abc import ABC, abstractmethod

from django.db.models import QuerySet

from blog.domain.entities.comment import Comment
from blog.domain.entities.profile import Profile


class CommentRepository(ABC):

    @abstractmethod
    def create(self, author: Profile, body: str) -> Comment:
        raise NotImplementedError

    @abstractmethod
    def delete(self, comment_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_comment(self, comment: Comment) -> Comment:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, comment_id) -> Comment:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def order_by(self, order: str) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_count(self, post_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_count_by_author(self, author_id: int) -> int:
        raise NotImplementedError
