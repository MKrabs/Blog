from unittest import TestCase
from django.contrib.auth.models import User
from blog.domain.entities.post import Post
from blog.infrastructure.repositories.post_repository import PostRepository


class TestPostRepository(TestCase):

    def setUp(self):
        self.post_repo = PostRepository()
        self.user, self.created = User.objects.get_or_create(username='test_user')

    def tearDown(self):
        posts = self.post_repo.get_all_from_user(user_id=self.user.id)
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
            body='Post body'
        )

        post.save()
        return post

    def test_create(self):
        self.create_post()
        posts_by_testuser = self.post_repo.get_all_from_user(user_id=self.user.id)
        self.assertEqual(posts_by_testuser.count(), 1)

    def test_get_count_by_author(self):
        for i in range(3):
            self.create_post(title=f"Title {i}")

        posts_by_testuser = self.post_repo.get_count_by_author(user_id=self.user.id)
        self.assertEqual(posts_by_testuser, 3)

    def test_get_all_from_user(self):
        post = self.create_post()

        posts_by_testuser = self.post_repo.get_all_from_user(user_id=self.user.id)

        # I do this because I want a QuerySet
        filtered_posts = posts_by_testuser.filter(id=post.id)

        self.assertEqual(filtered_posts.count(), 1)
        self.assertEqual(filtered_posts.first(), post)

