from django.db.models import QuerySet


class CommentSerializer:
    @classmethod
    def serialize(cls, comments: QuerySet):
        ser_comms = []

        for comment in comments:
            ser_comms.append({
                'id': comment.id,
                'author': comment.author.username if comment.author else None,
                'body': comment.body,
                'date': comment.date.strftime('%Y-%m-%d %H:%M:%S'),
                'post': comment.post.id,
            })

        return ser_comms
