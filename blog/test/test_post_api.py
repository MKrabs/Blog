from unittest.mock import MagicMock

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.test import RequestFactory, TestCase

from blog.application.comment_service import CommentService
from blog.application.post_service import PostService
from blog.infrastructure.serializers.comment_serializer import CommentSerializer
from blog.infrastructure.serializers.post_serializer import PostSerializer
from blog.presentation.api.post_api import PostAPI


class TestPostAPI(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_latest_posts(self):
        # Create a user and mock the request
        user = User(username='testuser')
        request = self.factory.get('/posts/')
        request.user = user

        # Create mock data for the PostService
        mock_latest_posts = [MagicMock(id=1), MagicMock(id=2)]
        mock_paginator = MagicMock(number=1)
        mock_num_pages = 3

        # Mock the PostService methods
        PostAPI.post_service = MagicMock(spec=PostService)
        PostAPI.post_service.get_latest_posts.return_value = mock_latest_posts
        PostAPI.post_service.paginate_posts.return_value = (mock_paginator, mock_num_pages)

        # Mock the PostSerializer
        mock_serialized_posts = [{'id': 1}, {'id': 2}]
        PostSerializer.serialize = MagicMock(return_value=mock_serialized_posts)

        # print("Current Blog Posts:", mock_serialized_posts)

        # Make the request to the API
        response = PostAPI.get_latest_posts(request)

        # Assert the response
        expected_context = {
            'page': {
                'current': 1,
                'total': 3,
            },
            'latest_posts': mock_serialized_posts,
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, JsonResponse(expected_context).content)

    def test_get_post(self):
        # Create a user and mock the request
        user = User(username='testuser')
        request = self.factory.get('/posts/1/')
        request.user = user

        # Create mock data for the PostService
        mock_post = MagicMock(id=1)
        mock_serialized_post = {'id': 1}
        mock_comments = [MagicMock(id=1), MagicMock(id=2)]
        mock_serialized_comments = [{'id': 1}, {'id': 2}]

        # Mock the PostService methods
        PostAPI.post_service = MagicMock(spec=PostService)
        PostAPI.post_service.get_post_by_id.return_value = mock_post

        # Mock the CommentService methods
        PostAPI.comment_service = MagicMock(spec=CommentService)
        PostAPI.comment_service.get_comments_by_post_id.return_value = mock_comments

        # Mock the serializers
        PostSerializer.serialize = MagicMock(return_value=[mock_serialized_post])
        CommentSerializer.serialize = MagicMock(return_value=mock_serialized_comments)

        # Make the request to the API
        response = PostAPI.get_post(request, post_id=1)

        # Assert the response
        expected_context = {
            'post': mock_serialized_post,
            'comments': mock_serialized_comments,
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, JsonResponse(expected_context).content)