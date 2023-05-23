from django.contrib.auth.models import User
from django.test import TestCase

from abstraction.markdown_processor import MarkdownProcessor
from blog.application.post_service import PostService
from blog.domain.entities.post import Post
from blog.infrastructure.repositories.post_repository import PostRepository


class TestPostService(TestCase):
    def setUp(self):
        self.post_service = PostService()
        self.post_repo = PostRepository()
        self.user, self.created = User.objects.get_or_create(username='test_user')

    def tearDown(self):
        posts = self.post_service.get_post_by_user(user=self.user)
        for post in posts:
            post.delete()
        self.user.delete()

    def create_post(self, title: str = "Test Post"):
        post = Post(
            author=self.user,
            title=title,
            image_type='jpg',
            image='test_image.jpg',
            short='Short description',
            body='Post **body**'
        )

        post.save()
        return post

    def test_get_post_by_id(self):
        post = self.create_post()
        result = self.post_service.get_post_by_id(post.id, beautify=True)

        self.assertIsNotNone(result)
        self.assertEqual(result.body, MarkdownProcessor.marker(post.body))

    def test_get_post_by_user(self):
        post = self.create_post()
        results = self.post_service.get_post_by_user(user=self.user, beautify=True)

        self.assertIsNotNone(results.count(), 1)
        self.assertEqual(results[0].body, MarkdownProcessor.marker(post.body))
