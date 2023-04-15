from django.db.models import QuerySet

from blog.domain.entities.tag import Tag


class TagRepository:

    def get_by_id(self, tag_id: int) -> Tag:
        return Tag.objects.get(id=tag_id)

    def get_by_name(self, name: str) -> Tag:
        return Tag.objects.get(name=name)

    def get_all(self) -> QuerySet:
        return Tag.objects.all()

    def get_count(self) -> int:
        return Tag.objects.count()

    def get_by_color(self, color: str) -> Tag:
        return Tag.objects.get(color=color)
