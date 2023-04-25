from django.db.models import QuerySet


class PostSerializer:
    @classmethod
    def serialize(cls, posts: QuerySet):
        ser_posts = []

        for post in posts:
            ser_posts.append({
                'id': post.id,
                'author': post.author.username if post.author else None,
                'title': post.title,
                'body': post.body,
                'date': post.date.strftime('%Y-%m-%d %H:%M:%S'),
                'image': post.image,
                'image_type': post.image_type,
            })

        return ser_posts
