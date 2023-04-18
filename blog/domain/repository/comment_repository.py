from abc import ABC, abstractmethod

from django.db.models import QuerySet

from blog.domain.entities.comment import Comment
from blog.domain.entities.post import Post
from blog.domain.entities.profile import Profile


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
    def get_count(self, post: Post) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_all_by_author(self, author: Profile) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_all_by_post(self, post: Post) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_count_by_author(self, author: Profile) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_count_by_post(self, post: Post) -> int:
        raise NotImplementedError
