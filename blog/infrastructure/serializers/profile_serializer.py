from django.core import serializers
from blog.domain.entities.profile import Profile


class ProfileSerializer:
    @classmethod
    def serialize(cls, profile: Profile):
        return {
            'id': profile.id,
            'username': profile.user.username,
            'email': profile.user.email,
            'picture': profile.picture.url,
            'bio': profile.bio,
            'location': profile.location,
            'date_joined': profile.user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        }
