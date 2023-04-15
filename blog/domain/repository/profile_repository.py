from django.contrib.auth.models import User
from django.db.models import QuerySet

from blog.domain.entities.profile import Profile
from blog.domain.repository.comment_repository import CommentRepository
from blog.domain.repository.like_repository import LikeRepository
from blog.domain.repository.post_repository import PostRepository


class ProfileRepository:
    def __init__(self):
        self.post_repo = PostRepository()
        self.comments_repo = CommentRepository()
        self.likes_repo = LikeRepository()

    def get_by_id(self, profile_id: int) -> Profile:
        return Profile.objects.get(id=profile_id)

    def get_by_username(self, user_name: str) -> Profile:
        return Profile.objects.get(user__username=user_name)

    def get_all(self) -> QuerySet:
        return Profile.objects.all()

    def save(self, profile: Profile) -> None:
        profile.save()

    def add_additional_fields(self, profile: Profile) -> None:
        profile.posts = self.post_repo.get_count_by_author(profile.id)
        profile.comments = self.comments_repo.get_count_by_author(profile.id)
        profile.likes = self.likes_repo.get_count_by_author(profile.id)
