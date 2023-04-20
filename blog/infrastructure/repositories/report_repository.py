import datetime

from django.db.models import QuerySet
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from blog.domain.entities.report import Report
from blog.domain.repository.report_repository import IReportRepository


class ReportRepository(IReportRepository):

    @staticmethod
    @receiver(post_save, sender=Report)
    def create(sender, instance, created, **kwargs) -> Report | None:
        if created:
            return None

        return

    @staticmethod
    @receiver(post_save, sender=Report)
    def save(sender, instance, **kwargs) -> None:
        pass

    @staticmethod
    @receiver(pre_delete, sender=Report)
    def delete(sender, instance, **kwargs) -> None:
        pass

    def get_all(self) -> QuerySet:
        return Report.objects.all()

    def get_by_id(self, report_id: int) -> Report | None:
        return Report.objects.filter(id=report_id).first()

    def get_all_of_post(self, post_id: int) -> QuerySet:
        return Report.objects.filter(content_type__model='post', object_id=post_id)

    def get_all_of_comment(self, comment_id: int) -> QuerySet:
        return Report.objects.filter(content_type__model='comment', object_id=comment_id)

    def get_all_by_author(self, author_id: int) -> QuerySet:
        return Report.objects.filter(content_object__author_id=author_id)

    def get_all_by_status(self, status: str) -> QuerySet:
        return Report.objects.filter(status=status)

    def get_all_by_severity(self, severity: str) -> QuerySet:
        return Report.objects.filter(severity=severity)

    def get_all_by_category(self, category: str) -> QuerySet:
        return Report.objects.filter(category=category)

    def get_all_by_reporter(self, reporter_id: int) -> QuerySet:
        return Report.objects.filter(reporter_id=reporter_id)

    def get_reports_between_dates(self, start_date: datetime, end_date: datetime) -> QuerySet:
        return Report.objects.filter(created_at__range=[start_date, end_date])
