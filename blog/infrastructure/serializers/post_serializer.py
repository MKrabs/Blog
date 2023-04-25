from django.db.models import QuerySet


class PostSerializer:
    @classmethod
    def serialize(cls, posts: QuerySet):
        serialized_posts = []

        for post in posts:
            serialized_posts.append({
                'id': post.id,
                'author': post.author.username or None,
                'title': post.title,
                'body': post.body,
                'date': post.date.strftime('%Y-%m-%d %H:%M:%S'),
                'image': post.image,
                'image_type': post.image_type,
            })

        return serialized_posts
