from abc import abstractmethod, ABC

from django.db.models import QuerySet

from blog.domain.entities.profile import Profile
from blog.domain.entities.tag import Tag


class ITagRepository(ABC):

    @abstractmethod
    def create(self, name, colour: str = None, icon: str = None, icon_colour: str = None, link: str = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self, name, colour: str = None, icon: str = None, icon_colour: str = None, link: str = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all_profile(self, profile: Profile) -> Tag:
        raise NotImplementedError

    @abstractmethod
    def get_all_username(self, username: str) -> Tag:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, tag_id: int) -> Tag:
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, name: str) -> Tag:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> QuerySet:
        raise NotImplementedError
