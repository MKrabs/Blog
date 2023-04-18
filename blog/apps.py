from django.apps import AppConfig
from django.db.models.signals import pre_delete


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        print('Configuring signals...')

        from django.contrib.auth.models import User
        from django.db.models.signals import post_save
        from blog.domain.entities.comment import Comment
        from blog.domain.entities.post import Post
        from blog.domain.entities.like import Like

        from blog.infrastructure.repositories.profile_repository import ProfileRepository
        from blog.infrastructure.repositories.post_repository import PostRepository
        from blog.infrastructure.repositories.comment_repository import CommentRepository
        from blog.infrastructure.repositories.like_repository import LikeRepository

        post_save.connect(ProfileRepository.create, sender=User)
        post_save.connect(ProfileRepository.save, sender=User)

        post_save.connect(PostRepository.create, sender=Post)
        post_save.connect(PostRepository.save, sender=Post)
        pre_delete.connect(PostRepository.delete, sender=Post)

        post_save.connect(CommentRepository.create, sender=Comment)
        post_save.connect(CommentRepository.save, sender=Comment)
        pre_delete.connect(CommentRepository.delete, sender=Comment)

        post_save.connect(LikeRepository.create, sender=Like)
        post_save.connect(LikeRepository.save, sender=Like)
        pre_delete.connect(LikeRepository.delete, sender=Like)


