from abc import ABC, abstractmethod

from django.contrib.auth.models import User
from django.db.models import QuerySet

from blog.domain.entities.post import Post


class IPostRepository(ABC):

    @abstractmethod
    def create(self, sender, instance, created, **kwargs) -> Post | None:
        raise NotImplementedError

    @abstractmethod
    def save(self, sender, instance, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, sender, instance, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, post_id) -> Post:
        raise NotImplementedError

    @abstractmethod
    def get_all_from_author(self, author: User, order_by: str = None) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, order_by: str = None) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_count(self, post_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_count_by_author(self, author_id: int) -> int:
        raise NotImplementedError
