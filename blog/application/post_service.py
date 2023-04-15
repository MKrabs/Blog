from typing import List, Optional

from django.core.paginator import Paginator, EmptyPage
from django.db.models import QuerySet

from blog.domain.entities.post import Post
from blog.domain.entities.profile import Profile
from blog.domain.repository.post_repository import PostRepository


class PostService:
    def __init__(self):
        self.post_repo = PostRepository()

    def get_latest_posts(self, order_by: str = None) -> QuerySet:
        if order_by:
            return self.post_repo.order_by(order_by)

        return self.post_repo.get_all()

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        return self.post_repo.get_by_id(post_id)

    def get_post_order_by(self, order: str) -> QuerySet:
        return self.post_repo.order_by(order)

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
            self.post_repo.delete(post)

    @classmethod
    def paginate_posts(cls, latest_posts, param: int = 4, page: int = 1) -> (Paginator, int):
        p = Paginator(latest_posts, param)

        try:
            page_obj = p.get_page(page)
        except EmptyPage:
            page_obj = p.page(p.num_pages)

        return page_obj, p.num_pages
