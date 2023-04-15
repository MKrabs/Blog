from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        print('Configuring signals...')

        from django.contrib.auth.models import User
        from django.db.models.signals import post_save
        from blog.infrastructure.repositories.profile_repository import create_user_profile, save_user_profile

        post_save.connect(create_user_profile, sender=User)
        post_save.connect(save_user_profile, sender=User)
