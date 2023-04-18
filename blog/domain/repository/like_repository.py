from abc import ABC, abstractmethod

from django.contrib.auth.models import User

from blog.domain.entities.like import Like
from blog.domain.entities.post import Post


class ILikeRepository(ABC):

    @staticmethod
    @abstractmethod
    def create(sender, instance, created, **kwargs) -> Like | None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def save(sender, instance, **kwargs) -> Like | None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def delete(sender, instance, **kwargs) -> Like | None:
        raise NotImplementedError

    @abstractmethod
    def get_count_post(self, post_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_count_author(self, author_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def did_user_like(self, user: User, post: Post) -> bool:
        raise NotImplementedError
