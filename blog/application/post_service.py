from typing import Optional

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.db.models import QuerySet

from abstraction.markdown_processor import MarkdownProcessor
from blog.application.profile_service import ProfileService
from blog.domain.entities.post import Post
from blog.infrastructure.repositories.comment_repository import CommentRepository
from blog.infrastructure.repositories.like_repository import LikeRepository
from blog.infrastructure.repositories.post_repository import PostRepository


class PostService:
    def __init__(self):
        self.post_repo = PostRepository()
        self.likes_repo = LikeRepository()
        self.comments_repo = CommentRepository()
        self.profile_repo = ProfileService()

    def get_latest_posts(self, user: User, order_by: str = None, additional_fields: bool = False) -> QuerySet:
        posts = self.post_repo.get_all(order_by=order_by)

        if additional_fields:
            for post in posts:
                post.comments = self.comments_repo.get_count_by_post(post_id=post.id)
                post.likes = self.likes_repo.get_count_post(post_id=post.id)
                self.profile_repo.add_additional_fields(post.author)
                if user.is_authenticated:
                    post.liked = self.likes_repo.did_user_like(user_id=user.id,post_id=post.id)

        return posts

    def get_post_by_id(self, post_id: int, beautify: bool = False) -> Optional[Post]:
        post = self.post_repo.get_by_id(post_id)

        if post and beautify:
            post.body = MarkdownProcessor.marker(post.body)

        return post

    def get_post_by_user(self, user: User, order_by: str = None, beautify: bool = False) -> QuerySet:
        posts = self.post_repo.get_all_from_user(user_id=user.id, order_by=order_by)

        if posts and beautify:
            for post in posts:
                post.body = MarkdownProcessor.marker(post.body)

        return posts

    # TODO - put pagination into abstraction layer
    @classmethod
    def paginate_posts(cls, latest_posts, param: int = 4, page: int = 1) -> (Paginator, int):
        p = Paginator(latest_posts, param)

        try:
            page_obj = p.get_page(page)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        return page_obj, p.num_pages

    def add_additional_fields(self, entity) -> None:
        self.profile_repo.add_additional_fields(entity.author)
        self.post_repo.add_additional_fields(entity)
