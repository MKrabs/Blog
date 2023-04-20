import datetime
from abc import ABC, abstractmethod

from django.db.models import QuerySet

from blog.domain.entities.report import Report


class IReportRepository(ABC):

    @abstractmethod
    def create(sender, instance, created, **kwargs) -> Report | None:
        raise NotImplementedError

    @abstractmethod
    def save(sender, instance, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(sender, instance, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, report_id: int) -> Report | None:
        raise NotImplementedError

    @abstractmethod
    def get_all_of_post(self, post_id: int) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_all_of_comment(self, comment_id: int) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_all_by_author(self, author_id: int) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_all_by_status(self, status: str) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_all_by_severity(self, severity: str) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_all_by_category(self, category: str) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_all_by_reporter(self, reporter_id: int) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    def get_reports_between_dates(self, start_date: datetime, end_date: datetime) -> QuerySet:
        raise NotImplementedError
