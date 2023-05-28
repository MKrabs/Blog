from unittest import TestCase
from unittest.mock import patch

from blog.domain.entities.comment import Comment
from blog.infrastructure.repositories.comment_repository import CommentRepository


class TestCommentRepository(TestCase):
    @patch('blog.infrastructure.repositories.comment_repository.profanity')
    def test_save(self, mock_profanity):
        # Mock the profanity module to control its behavior
        mock_profanity.contains_profanity.return_value = True
        mock_profanity.censor.return_value = '*** comment'

        # Create a comment instance
        comment = Comment()
        comment.body = 'Profane comment'

        # Call the save method of CommentRepository
        CommentRepository.save(Comment, comment)

        # Check if the comment body has been censored
        self.assertEqual(comment.body, '*** comment')
