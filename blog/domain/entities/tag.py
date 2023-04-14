from django.db import models


class Tag(models.Model):
    colour_choices = (
        ("primary", "primary"),
        ("secondary", "secondary"),
        ("success", "success"),
        ("danger", "danger"),
        ("warning", "warning"),
        ("info", "info"),
        ("light", "light"),
        ("dark", "dark"),
    )

    name = models.CharField(
        max_length=50
    )
    color = models.CharField(
        max_length=10,
        choices=colour_choices,
        default="dark"
    )
    icon = models.CharField(
        max_length=20,
        null=True
    )
    icon_colour = models.CharField(
        max_length=6,
        default="000000"
    )
    link = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
