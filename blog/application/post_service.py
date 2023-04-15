from typing import List, Optional

from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.db.models import QuerySet

from blog.domain.entities.post import Post
from blog.domain.entities.profile import Profile
from blog.domain.repository.comment_repository import CommentRepository
from blog.domain.repository.like_repository import LikeRepository
from blog.domain.repository.post_repository import PostRepository


class PostService:
    def __init__(self):
        self.post_repo = PostRepository()
        self.likes_repo = LikeRepository()
        self.comments_repo = CommentRepository()

    def get_latest_posts(self, user: User, order_by: str = None) -> QuerySet:
        posts = self.post_repo.get_all(order_by=order_by)

        for post in posts:
            post.comments = self.comments_repo.get_count(post.id)
            post.likes = self.likes_repo.get_count(post.id)
            post.liked = self.likes_repo.did_user_like(user, post.id)

        return posts

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        return self.post_repo.get_by_id(post_id)

    def get_post_order_by(self, order: str) -> QuerySet:
        return self.post_repo.get_all(order_by=order)

    def create_post(self, author: Profile, title: str, image_type: str, image: str, short: str, body: str) -> Post:
        post = self.post_repo.create(
            author=author,
            title=title,
            image_type=image_type,
            image=image,
            short=short,
            body=body
        )

        return self.post_repo.save_post(post)

    def update_post(self, post_id: int, title: str, image_type: str, image: str, short: str, body: str)\
            -> Optional[Post]:
        post = self.post_repo.get_by_id(post_id)

        if not post:
            raise Exception('Post not found')

        self.post_repo.update(post_id, title=title, image_type=image_type, image=image, short=short, body=body)

        return self.post_repo.save_post(post)

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
