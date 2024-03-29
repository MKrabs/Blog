from abc import ABC, abstractmethod

from django.db.models import QuerySet

from blog.domain.entities.comment import Comment


class ICommentRepository(ABC):

    @abstractmethod
    def create(sender, instance, **kwargs) -> Comment:
        raise NotImplementedError

    @abstractmethod
    def save(self, sender, instance, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, comment_id: int) -> None:
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
    def get_all_by_author(self, user_id: int) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_all_by_post(self, post_id: int) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_count_by_author(self, user_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_count_by_post(self, post_id: int) -> int:
        raise NotImplementedError
