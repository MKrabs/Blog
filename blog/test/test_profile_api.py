from unittest.mock import MagicMock

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.test import RequestFactory, TestCase

from blog.application.comment_service import CommentService
from blog.application.post_service import PostService
from blog.application.profile_service import ProfileService
from blog.domain.entities.profile import Profile
from blog.infrastructure.serializers.comment_serializer import CommentSerializer
from blog.infrastructure.serializers.post_serializer import PostSerializer
from blog.infrastructure.serializers.profile_serializer import ProfileSerializer
from blog.presentation.api.profile_api import ProfileAPI


class ProfileAPITest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_user_profile(self):
        # Create a user and mock the request
        user = User(username='testuser')
        request = self.factory.get('/profile/testuser/')
        request.user = user

        # Create mock data for the ProfileService
        mock_profile = MagicMock(spec=Profile, user=user)
        mock_serialized_profile = {'username': 'testuser'}
        mock_posts = [MagicMock(id=1), MagicMock(id=2)]
        mock_serialized_posts = [{'id': 1}, {'id': 2}]
        mock_comments = [MagicMock(id=1), MagicMock(id=2)]
        mock_serialized_comments = [{'id': 1}, {'id': 2}]

        # Mock the ProfileService methods
        ProfileAPI.profile_service = MagicMock(spec=ProfileService)
        ProfileAPI.profile_service.get_profile_by_username.return_value = mock_profile

        # Mock the PostService methods
        ProfileAPI.post_service = MagicMock(spec=PostService)
        ProfileAPI.post_service.get_post_by_user.return_value = mock_posts

        # Mock the CommentService methods
        ProfileAPI.comment_service = MagicMock(spec=CommentService)
        ProfileAPI.comment_service.get_comments_by_user.return_value = mock_comments

        # Mock the serializers
        ProfileSerializer.serialize = MagicMock(return_value=mock_serialized_profile)
        PostSerializer.serialize = MagicMock(return_value=mock_serialized_posts)
        CommentSerializer.serialize = MagicMock(return_value=mock_serialized_comments)

        # Make the request to the API
        response = ProfileAPI.get_user_profile(request, user_name='testuser')

        # Assert the response
        expected_context = {
            'profile': mock_serialized_profile,
            'posts': mock_serialized_posts,
            'comments': mock_serialized_comments,
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, JsonResponse(expected_context).content)
