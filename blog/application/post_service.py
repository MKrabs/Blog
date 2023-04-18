from typing import Optional

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.db.models import QuerySet

from abstraction.markdown_processor import MarkdownProcessor as mp
from blog.application.profile_service import ProfileService
from blog.domain.entities.post import Post
from blog.domain.entities.profile import Profile
from blog.domain.repository.comment_repository import CommentRepository
from blog.domain.repository.like_repository import LikeRepository
from blog.infrastructure.repositories.post_repository import PostRepository


class PostService:
    def __init__(self):
        self.post_repo = PostRepository()
        self.likes_repo = LikeRepository()
        self.comments_repo = CommentRepository()
        self.profile_repo = ProfileService()

    def get_latest_posts(self, user: User, order_by: str = None) -> QuerySet:
        return self.post_repo.get_all(order_by=order_by)

    def get_post_by_id(self, post_id: int, beautify: bool = False) -> Optional[Post]:
        post = self.post_repo.get_by_id(post_id)

        if post and beautify:
            post.body = mp.marker(post.body)

        return post

    def get_post_by_user(self, user: User, order_by: str = None, beautify: bool = False) -> QuerySet:
        posts = self.post_repo.get_all_from_author(author=user, order_by=order_by)

        if posts and beautify:
            for post in posts:
                post.body = mp.marker(post.body)

        return posts

    def get_post_order_by(self, order: str) -> QuerySet:
        return self.post_repo.get_all(order_by=order)


    def delete_post(self, post_id: int) -> None:
        post = self.post_repo.get_by_id(post_id)

        if post:
            self.post_repo.delete(post_id)

    @classmethod
    def paginate_posts(cls, latest_posts, param: int = 4, page: int = 1) -> (Paginator, int):
        p = Paginator(latest_posts, param)

        try:
            page_obj = p.get_page(page)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        return page_obj, p.num_pages

    def add_additional_fields(self, entity, user: User) -> None:
        self.post_repo.add_additional_fields(entity, user)
        self.profile_repo.add_additional_fields(entity)
