from django.contrib.auth.models import User

from abstraction.image_processor import ImageProcessor
from abstraction.markdown_processor import MarkdownProcessor as mp

from blog.domain.entities.profile import Profile
from blog.domain.repository.comment_repository import CommentRepository
from blog.domain.repository.like_repository import LikeRepository
from blog.domain.repository.post_repository import PostRepository
from blog.domain.repository.profile_repository import ProfileRepository


class ProfileService:
    def __init__(self):
        self.profile_repo = ProfileRepository()
        self.image_processor = ImageProcessor()
        self.post_repo = PostRepository()
        self.likes_repo = LikeRepository()
        self.comments_repo = CommentRepository()


    def get_profile_by_id(self, profile_id: int) -> Profile:
        profile = self.profile_repo.get_by_id(profile_id)

        if profile:
            profile.bio = mp.marker(profile.bio)

        return profile

    def get_profile_by_username(self, user_name: str, beautify: bool = False) -> Profile:
        profile = self.profile_repo.get_by_username(user_name)

        if profile and beautify:
            profile.bio = mp.marker(profile.bio)

        return profile

    def save_profile(self, profile: Profile, new_image=False):

        if new_image:
            processed_image_path = self.image_processor.process(profile.picture.path)
            profile.picture = processed_image_path

        profile.save()

    def add_additional_fields(self, entity) -> None:
        if entity.author:
            entity.author.profile.bio = mp.marker(entity.author.profile.bio)
            entity.author.total_posts = self.post_repo.get_count_by_author(entity.author.id)
            entity.author.total_comments = self.comments_repo.get_count_by_author(entity.author.id)
            entity.author.total_likes = self.likes_repo.get_count_by_author(entity.author.id)
