from abc import ABC, abstractmethod

from django.db.models import QuerySet

from blog.domain.entities.profile import Profile


class IProfileRepository(ABC):

    @abstractmethod
    def create(self, sender, instance, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self, sender, instance, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, profile_id: int) -> Profile:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, user_name: str) -> Profile:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> QuerySet:
        raise NotImplementedError
