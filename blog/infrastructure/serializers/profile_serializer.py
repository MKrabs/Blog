from blog.domain.entities.profile import Profile


class ProfileSerializer:
    @classmethod
    def serialize(cls, profile: Profile):
        return {
            'id': profile.id,
            'username': profile.user.username,
            'email': profile.user.email or None,
            'picture': profile.picture.url or None,
            'bio': profile.bio or None,
            'location': profile.location or None,
            'date_joined': profile.user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        }
