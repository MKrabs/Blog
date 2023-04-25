from django.core import serializers
from blog.domain.entities.post import Post


class PostSerializer:
    @classmethod
    def serialize(cls, posts: list[Post]):
        ser_posts = []

        for post in posts:
            ser_posts.append({
                'id': post.id,
                'author': post.author.username,
                'title': post.title,
                'body': post.body,
                'date': post.date.strftime('%Y-%m-%d %H:%M:%S'),
                'image': post.image,
                'image_type': post.image_type,
            })

        return ser_posts
