from django.db.models import QuerySet


class CommentSerializer:
    @classmethod
    def serialize(cls, comments: QuerySet):
        serialized_comments = []

        for comment in comments:
            serialized_comments.append({
                'id': comment.id,
                'author': comment.author.username if comment.author else None,
                'body': comment.body,
                'date': comment.date.strftime('%Y-%m-%d %H:%M:%S'),
                'post': comment.post.id,
            })

        return serialized_comments
