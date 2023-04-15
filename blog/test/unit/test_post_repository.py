from django.contrib.auth.models import User
from django.test import TestCase

from blog.domain.entities.post import Post
from blog.domain.repository.post_repository import PostRepository


class TestPostRepository(TestCase):
    def setUp(self):
        self.post_repo = PostRepository()
        self.author = User.objects.create_user(username="test_user")

    def test_get_by_id(self):
        post = Post.objects.create(
            author=self.author, title="test post", short="test", body="test body"
        )
        retrieved_post = self.post_repo.get_by_id(post.id)
        self.assertEqual(retrieved_post, post)

    def test_get_all(self):
        Post.objects.create(
            author=self.author, title="test post 1", short="test", body="test body"
        )
        Post.objects.create(
            author=self.author, title="test post 2", short="test", body="test body"
        )
        all_posts = self.post_repo.get_all()
        self.assertEqual(len(all_posts), 2)

    def test_order_by(self):
        Post.objects.create(
            author=self.author, title="test post 1", short="test", body="test body"
        )
        Post.objects.create(
            author=self.author, title="test post 2", short="test", body="test body"
        )
        ordered_posts = self.post_repo.order_by('title')
        self.assertEqual(ordered_posts[0].title, "test post 1")

    def test_create(self):
        post = self.post_repo.create(
            author=self.author,
            title="test post",
            short="test",
            body="test body",
            image_type="iFrame",
            image="test.jpg"
        )
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.title, "test post")
        self.assertEqual(post.short, "test")
        self.assertEqual(post.body, "test body")
        self.assertEqual(post.image_type, "iFrame")
        self.assertEqual(post.image, "test.jpg")
