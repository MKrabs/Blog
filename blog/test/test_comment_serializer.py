from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase
from unittest.mock import MagicMock

from blog.domain.entities.comment import Comment
from blog.domain.entities.post import Post
from blog.infrastructure.serializers.comment_serializer import CommentSerializer


class CommentSerializerTest(TestCase):
    def test_serialize(self):
        # Create a sample comment
        comment = Comment()
        comment.id = 1
        comment.author = User(username='Marc')
        comment.body = 'Sample comment'
        comment.date = datetime(2023, 5, 28, 12, 0, 0)

        # Create a mock Post instance
        post = Post(id=42)

        # Assign the mock Post instance to the comment
        comment.post = post

        # Create a QuerySet with the comment
        comments_qs = QuerySet(model=Comment)
        comments_qs._result_cache = [comment]  # Mock the cached results

        # Serialize the comments
        serialized_comments = CommentSerializer.serialize(comments_qs)

        # Assert the serialized output
        expected_result = [
            {
                'id': 1,
                'author': 'Marc',
                'body': 'Sample comment',
                'date': '2023-05-28 12:00:00',
                'post': 42,
            }
        ]

        print(serialized_comments)

        self.assertEqual(serialized_comments, expected_result)
