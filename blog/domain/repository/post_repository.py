from django.db.models import QuerySet

from blog.domain.entities.post import Post
from blog.domain.entities.profile import Profile


class PostRepository:
    def get_by_id(self, post_id) -> Post:
        return Post.objects.get(id=post_id)

    def get_all(self) -> QuerySet:
        return Post.objects.all()

    def order_by(self, order: str) -> QuerySet:
        return Post.objects.order_by(order)

    def create(self, author: Profile, title: str, short: str, body: str, image_type: str = None, image: str = None)\
            -> Post:
        post = Post(author=author, title=title, image_type=image_type, image=image, short=short, body=body)
        post = self.save_post(post)
        return post

    def update(self, post_id: int, title=None, image_type=None, image=None, short=None, body=None):
        post = self.get_by_id(post_id)
        if title:
            post.title = title
        if image_type:
            post.image_type = image_type
        if image:
            post.image = image
        if short:
            post.short = short
        if body:
            post.body = body
        self.save_post(post)
        return post

    def delete(self, post_id: int) -> None:
        post = self.get_by_id(post_id)
        post.delete()

    def save_post(self, post: Post) -> Post:
        post.save()
        return post
