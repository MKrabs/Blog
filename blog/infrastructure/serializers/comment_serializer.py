from django.core import serializers
from blog.domain.entities.comment import Comment


class CommentSerializer:
    @classmethod
    def serialize(cls, comments: list[Comment]):
        ser_comms = []

        for comment in comments:
            ser_comms.append({
                'id': comment.id,
                'author': comment.author.username,
                'body': comment.body,
                'date': comment.date.strftime('%Y-%m-%d %H:%M:%S'),
                'post': comment.post.id,
            })

        return ser_comms
