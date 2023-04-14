from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.domain.entities.post import Post


@receiver(post_save, sender=Post)
def save_post(sender, instance, **kwargs):
    instance.save()


@receiver(post_save, sender=Post)
def create_post(sender, instance, created, **kwargs):
    if created:
        Post.objects.create(
            author=instance.author,
            title=instance.title,
            image_type=instance.image_type,
            image=instance.image,
            short=instance.short,
            body=instance.body
        )
