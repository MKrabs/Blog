from abc import ABC, abstractmethod

from blog.domain.entities.like import Like


class ILikeRepository(ABC):

    @abstractmethod
    def create(sender, instance, created, **kwargs) -> Like | None:
        raise NotImplementedError

    @abstractmethod
    def save(sender, instance, **kwargs) -> Like | None:
        raise NotImplementedError

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
    def did_user_like(self, user_id: int, post_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_like_by_post_and_author(self, post_id: int, author: int) -> Like:
        raise NotImplementedError
