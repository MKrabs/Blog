from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        print('Configuring signals...')

        from django.contrib.auth.models import User
        from django.db.models.signals import post_save
        from blog.infrastructure.repositories.profile_repository import ProfileRepository

        post_save.connect(ProfileRepository.create, sender=User)
        post_save.connect(ProfileRepository.save, sender=User)
