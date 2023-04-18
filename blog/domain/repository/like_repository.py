from abc import ABC, abstractmethod

from django.contrib.auth.models import User

from blog.domain.entities.like import Like
from blog.domain.entities.post import Post
from blog.domain.entities.profile import Profile


class LikeRepository(ABC):

    @abstractmethod
    def create(self, author: Profile, post: Post) -> int:
        raise NotImplementedError

    @abstractmethod
    def save(self, author: Profile, post: Post) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, like_id: int) -> None:
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
