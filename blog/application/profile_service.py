from abstraction.image_processor import ImageProcessor
from abstraction.markdown_processor import MarkdownProcessor as mp

from blog.domain.entities.profile import Profile
from blog.domain.repository.comment_repository import CommentRepository
from blog.domain.repository.like_repository import LikeRepository
from blog.domain.repository.post_repository import PostRepository


class ProfileService:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.post_repo = PostRepository()
        self.likes_repo = LikeRepository()
        self.comments_repo = CommentRepository()

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
