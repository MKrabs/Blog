from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Report(models.Model):
    report_category = (
        ('spam', 'spam'),
        ('inappropriate', 'inappropriate'),
        ('other', 'other'),
    )

    report_severity = (
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', 'high'),
    )

    report_status = (
        ('open', 'open'),
        ('in_progress', 'in_progress'),
        ('resolved', 'resolved'),
        ('rejected', 'rejected'),
    )

    reporter = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None, null=True)
    comment = models.TextField(blank=False, null=False)
    category = models.CharField(max_length=20, choices=report_category, default='spam')
    severity = models.CharField(max_length=20, choices=report_severity, default='low')
    status = models.CharField(max_length=20, choices=report_status, default='open')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.severity}] ({self.category}) - {self.comment}'

